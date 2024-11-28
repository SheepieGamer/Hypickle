import discord
from discord import app_commands
from discord.ext import commands
import logging
import utils
import settings
import json
from typing import List
from PIL import Image, ImageDraw, ImageFont
import io
import aiohttp
from functools import partial
import asyncio
from io import BytesIO

class Hypixel(commands.Cog):
    """Hypixel-related commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger('HypickleBot.Hypixel')
        # Load fonts when the cog is initialized
        try:
            self.title_font = ImageFont.truetype("arial.ttf", 42)  # Title text
            self.stats_font = ImageFont.truetype("arial.ttf", 32)  # Stats text
            self.stats_font_bold = ImageFont.truetype("arialbd.ttf", 32)  # Bold stats text
            self.combat_font = ImageFont.truetype("arial.ttf", 28)  # Combat stats
        except Exception as e:
            self.logger.error(f"Failed to load fonts: {e}")
            # Fallback to default font
            self.title_font = ImageFont.load_default()
            self.stats_font = ImageFont.load_default()
            self.stats_font_bold = ImageFont.load_default()
            self.combat_font = ImageFont.load_default()

    def create_duels_image(self, username: str, stats: dict, ratios: dict, gamemode: str = "overall", 
                          player_image=None, title: str = "Rookie", prestige: str = "", 
                          title_color: str = "#808080", is_bold: bool = False):
        """
        Creates a formatted image displaying Hypixel Duels statistics.
        """
        # Create base image with dark theme colors
        width, height = 1000, 600
        image = Image.new('RGB', (width, height), color='#2C2F33')  # Discord dark theme color
        draw = ImageDraw.Draw(image)

        # Define section heights and paddings
        player_section_height = height//2  # Top section (player model + stats)
        winstreak_section_height = height//4  # Middle section (winstreaks)
        combat_section_height = height//4  # Bottom section (combat stats)
        
        padding = 15  # Consistent padding for all sections

        # Draw borders and sections
        draw.rectangle([0, 0, width-1, height-1], outline='#99AAB5', width=2)  # Main border
        draw.line([width//2, 0, width//2, player_section_height], fill='#99AAB5', width=2)  # Vertical divider
        draw.line([0, player_section_height, width, player_section_height], fill='#99AAB5', width=2)  # First horizontal divider
        draw.line([0, player_section_height + winstreak_section_height, width, player_section_height + winstreak_section_height], fill='#99AAB5', width=2)  # Second horizontal divider

        # Left side - Player model and username
        if player_image:
            try:
                model = Image.open(BytesIO(player_image))
                # Calculate size while maintaining aspect ratio
                max_height = player_section_height - padding*6  # Leave space for username and title
                max_width = width//2 - padding*2
                
                # Calculate scaling factor while maintaining aspect ratio
                width_ratio = max_width / model.width
                height_ratio = max_height / model.height
                scale_factor = min(width_ratio, height_ratio)
                
                new_width = int(model.width * scale_factor)
                new_height = int(model.height * scale_factor)
                
                model = model.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Center the resized model
                x_pos = (width//2 - new_width) // 2
                y_pos = (player_section_height - new_height - padding*5) // 2  # Leave space for username and title
                image.paste(model, (x_pos, y_pos), model if 'A' in model.getbands() else None)
            except Exception as e:
                self.logger.error(f"Failed to paste player model: {e}")

        # Draw username and title
        username_y = player_section_height - padding*5
        title_y = player_section_height - padding*3
        draw.text((width//4, username_y), username, fill='#FFFFFF', font=self.title_font, anchor="mm")
        full_title = f"{title} {prestige}" if prestige else title
        font = self.stats_font_bold if is_bold else self.stats_font
        draw.text((width//4, title_y), full_title, fill=title_color, font=font, anchor="mm")

        # Right side - Stats
        x_offset = width//2 + padding*2
        y_start = padding*2
        available_height = player_section_height - padding*4
        stats_spacing = available_height // 4  # Evenly space 4 stats

        # Format stats with commas for readability
        stats_text = [
            (f"Coins: {stats.get('coins', 0):,}"),
            (f"Bow Shots: {stats.get('bow_shots', 0):,}"),
            (f"Blocks Placed: {stats.get('blocks_placed', 0):,}"),
            (f"Ping Range: {stats.get('ping', 'Unknown')}")
        ]

        for i, text in enumerate(stats_text):
            draw.text((x_offset, y_start + i*stats_spacing), text, fill='#FFFFFF', font=self.stats_font)

        # Winstreak section
        winstreak_y = player_section_height + padding*2
        draw.text((padding*2, winstreak_y), f"Winstreak: {stats.get('current_winstreak', 0):,}", 
                 fill='#FFFFFF', font=self.stats_font)
        draw.text((padding*2, winstreak_y + winstreak_section_height//2), 
                 f"Best Winstreak: {stats.get('best_overall_winstreak', 0):,}", 
                 fill='#FFFFFF', font=self.stats_font)

        # Combat stats section
        combat_y = player_section_height + winstreak_section_height + padding*2
        section_title_y = combat_y
        draw.text((width//2, section_title_y), "Combat Stats", fill='#FFFFFF', 
                 font=self.title_font, anchor="mm")

        # Calculate spacing for combat stats
        combat_stats = [
            (f"Kills: {stats.get('kills', 0):,}", f"Deaths: {stats.get('deaths', 0):,}"),
            (f"Wins: {stats.get('wins', 0):,}", f"Losses: {stats.get('losses', 0):,}"),
            (f"K/D: {ratios.get('kdr', 0):.2f}", f"W/L: {ratios.get('wlr', 0):.2f}")
        ]

        stats_y = section_title_y + padding*3
        available_height = combat_section_height - padding*5
        combat_spacing = available_height // 3  # Evenly space 3 pairs of stats

        for i, (left, right) in enumerate(combat_stats):
            current_y = stats_y + i*combat_spacing
            draw.text((width//4, current_y), left, fill='#FFFFFF', font=self.combat_font, anchor="mm")
            draw.text((3*width//4, current_y), right, fill='#FFFFFF', font=self.combat_font, anchor="mm")

        # Convert to bytes for Discord upload
        img_bytes = BytesIO()
        image.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        return img_bytes

    @app_commands.command()
    @app_commands.describe(username="Player to get stats for", gamemode="Gamemode to get stats for")
    @app_commands.choices(gamemode=[
        app_commands.Choice(name="Overall", value="overall"),
        app_commands.Choice(name="UHC", value="uhc"),
        app_commands.Choice(name="OP", value="op"),
        app_commands.Choice(name="SkyWars", value="skywars"),
        app_commands.Choice(name="Classic", value="classic"),
        app_commands.Choice(name="Sumo", value="sumo"),
        app_commands.Choice(name="Bridge", value="bridge"),
        app_commands.Choice(name="NoDebuff", value="nodebuff"),
        app_commands.Choice(name="Combo", value="combo"),
        app_commands.Choice(name="Boxing", value="boxing"),
        app_commands.Choice(name="MegaWalls", value="megawalls"),
        app_commands.Choice(name="Bowspleef", value="bowspleef"),
        app_commands.Choice(name="Parkour", value="parkour"),
        app_commands.Choice(name="Arena", value="arena")
    ])
    async def duels(self, interaction: discord.Interaction, username: str, gamemode: str = "overall"):
        """
        Displays Hypixel Duels statistics for a player in a beautifully formatted image.
        
        Args:
            interaction (discord.Interaction): Discord interaction context
            username (str): Minecraft username to look up
            gamemode (str, optional): Specific duels gamemode to show stats for. Defaults to "overall"
        """
        await interaction.response.defer()
        
        username, uuid = await utils.get_pretty_username(username, bedwars=False)
        if not uuid or not username:
            await interaction.followup.send("❌ Could not find that player!")
            return

        print(f"Duels CMD: uuid {uuid}")
        
        # Get player image
        player_image = None
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(await utils.get_3d_body(uuid)) as resp:
                    if resp.status == 200:
                        player_image = await resp.read()
        except Exception as e:
            self.logger.error(f"Failed to fetch player image: {e}")

        # Get player title
        prestige, title, title_color, is_bold = await utils.get_duels_title(uuid, gamemode)
        if prestige == 0:
            prestige = "None"

        if gamemode == "combo":
            gamemode = "combo_duel"
        elif gamemode == "arena":
            gamemode = "duel_arena"
        elif gamemode == "parkour":
            gamemode = "parkour_eight"
        elif gamemode == "bowspleef":
            gamemode = "bowspleef_duel"
        elif gamemode == "megawalls":
            gamemode = "mw_duel"
        elif gamemode == "boxing":
            gamemode = "boxing_duel"
        elif gamemode == "nodebuff":
            gamemode = "potion_duel"
        elif gamemode == "sumo":
            gamemode = "sumo_duel"
        elif gamemode == "classic":
            gamemode = "classic_duel"
        elif gamemode == "uhc":
            gamemode = "uhc_duel"
        elif gamemode == "op":
            gamemode = "op_duel"
        elif gamemode == "skywars":
            gamemode = "sw_duel"
        # elif gamemode == "bridge":
        #     gamemode = "bridge_duel_bridge"


        stats = {
            'kills': await utils.get_duels_kills(uuid, gamemode),
            'deaths': await utils.get_duels_deaths(uuid, gamemode),
            'wins': await utils.get_duels_wins(uuid, gamemode),
            'losses': await utils.get_duels_losses(uuid, gamemode),
            'coins': await utils.get_duels_coins(uuid),
            'blocks_placed': await utils.get_duels_blocks(uuid),
            'bow_shots': await utils.get_duels_shots(uuid),
            'ping': await utils.get_duels_ping(uuid),
            'current_winstreak': await utils.get_duels_current_winstreak(uuid, gamemode),
            'best_overall_winstreak': await utils.get_duels_best_winstreak(uuid, gamemode),
            'melee_swings': await utils.get_duels_swings(uuid)
        }

        kdr = await utils.get_duels_kdr(uuid, gamemode)
        wlr = await utils.get_duels_wlr(uuid, gamemode)

        # Calculate all ratios
        ratios = {
            'kdr': kdr,
            'wlr': wlr,
        }

        # Create and send image
        img_bytes = self.create_duels_image(username, stats, ratios, gamemode, player_image,
                                          title=title, prestige=prestige, title_color=title_color,
                                          is_bold=is_bold)

        await interaction.followup.send(file=discord.File(img_bytes, filename=f'{interaction.user.name}-s_duels_stats.png'))

    @app_commands.command(name="bedwars-map")
    async def bedwars_map(self, interaction: discord.Interaction, map: str):
        await interaction.response.defer()
        name = map.capitalize().replace("%20", " ")
        map_name = name.replace("%27", "'")
        map_value = map

        data = await utils.get_map(map_value)

        try:
            image = data["data"]["preview"]
        except KeyError:
            await interaction.followup.send(f"Unknown map {map_name} (maybe a spelling error?)")
            return
        playstyle = data["data"]["playstyle"]
        gen = data["data"]["gen"]
        builders = data["data"]["builders"]
        desc = data["data"]["description"]
        def if_gen(generator):
            if generator:
                return f"It has a **{gen.lower()}** resource generator."
            return " "

        embed=discord.Embed(
            title=f"{map_name}", 
            color=discord.Color.random(),
            description=f"{map_name} is a **{playstyle.lower()}** map that was made by **{builders}**. {if_gen(generator=gen)}\n{desc}"
        )
        
        embed.set_footer(text="Hypickle")
        embed.set_image(url=f"{image}")
        
        await interaction.followup.send(embed=embed)

    @bedwars_map.autocomplete('map')
    async def bedwars_map_autocomplete(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        autocompleted_maps = []
        for map_name in utils.maps:
            if map_name.name.lower().startswith(current.lower()):
                if len(autocompleted_maps) < 25:
                    autocompleted_maps.append(app_commands.Choice(name=map_name.name, value=map_name.name))
                else:
                    break
        return autocompleted_maps

    @app_commands.command()
    async def bedwars(self, interaction: discord.Interaction):
        await interaction.response.defer()

    async def cog_command_error(self, interaction: discord.Interaction, error: Exception):
        """Handle errors that occur in any command in this cog"""
        if isinstance(error, commands.MissingPermissions):
            await interaction.followup.send('❌ You do not have permission to use this command')
        elif isinstance(error, commands.BotMissingPermissions):
            await interaction.followup.send('❌ I do not have permission to execute this command')
        elif isinstance(error, commands.MissingRequiredArgument):
            await interaction.followup.send('❌ Missing required argument')
        elif isinstance(error, commands.BadArgument):
            await interaction.followup.send('❌ Invalid argument provided')
        else:
            self.logger.error(f'Unexpected error in {interaction.command}: {str(error)}')
            await interaction.followup.send('❌ An unexpected error occurred')

async def setup(bot: commands.Bot):
    """Setup function for loading the cog"""
    await bot.add_cog(Hypixel(bot))
