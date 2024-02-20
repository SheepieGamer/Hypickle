from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice as c
import config
import aiohttp
import requests
import utils
import shutil
import os
import json
import pathlib
from PIL import Image
from utils import prettify, get_3d_head, get_pretty_username, get_uuid, get_plain_name
from typing import Literal, Optional
import discord

BASE_DIR = pathlib.Path(__file__).parent

def main(secret, bot):

    @bot.event
    async def on_ready():
        await utils.print_user(bot)
        await utils.load_cogs(bot)
        await utils.load_cmds(bot)
        await utils.other(bot)
        print("Startup complete")
        # nothing after

    @bot.hybrid_command(name="link")
    async def link(ctx, ign: str):
        if ctx.guild.id != 1189274528992460871:
            await ctx.reply("this command is not for you")
            return
        test = False

        if test:
            fp = "test-link.json"
        else:
            fp = "linked.json"
        
        try:
            uuid = await get_uuid(ign.lower())
        except KeyError:
            await ctx.send("Invalid username")
            return

        try:
            with open(fp, "r") as f:
                existing_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            existing_data = {}

        if str(ctx.author.id) in existing_data:
            await ctx.send("You have already linked your Discord account.")
            return

        if any(uuid == existing_uuid for existing_uuid in existing_data.values()):
            await ctx.send("This Minecraft Account is already linked to another Discord account.")
            return

        try:
            existing_data[str(ctx.author.id)] = uuid
        except KeyError:
            await ctx.send("Invalid username")
            return

        with open(fp, "w") as f:
            json.dump(existing_data, f, indent=4)

        await ctx.send(f"Successfully linked {ctx.author.mention} to Minecraft account **{await get_plain_name(ign)}** (``{await get_uuid(ign)}``)")

    @bot.hybrid_command(name="refresh")
    async def refresh(ctx, channel: discord.TextChannel):
        if ctx.guild.id != 1189274528992460871:
            await ctx.reply("this command is not for you")
            return
        
        # Load linked data
        try:
            with open("linked.json", "r") as f:
                linked_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            linked_data = {}

        values = list(linked_data.values())
        keys = []
        for key in linked_data:
            keys.append(key)
        # await ctx.reply(str(keys))

        usernames = []
        for value in values:
            usernames.append(await get_plain_name(value))

        formatted_keys = [f"<@{key}>" for key in keys]
        formatted_values = [f"{await get_plain_name(value)}" for value in values]

        embed = discord.Embed(
            description=str(dict(zip(formatted_keys, formatted_values)))
        )
        await ctx.reply(embed=embed)
                
        if 1 + 1 == 2:
            one_final = ""
            two_final = ""
            three_final = ""
            four_final = ""
            five_final = ""
            six_final = ""

            one_bed = ""
            two_bed = ""
            three_bed = ""
            four_bed = ""
            five_bed = ""
            six_bed = ""

            one_kill = ""
            two_kill = ""
            three_kill = ""
            four_kill = ""
            five_kill = ""
            six_kill = ""

            one_win = ""
            two_win = ""
            three_win = ""
            four_win = ""
            five_win = ""
            six_win = ""

            one_lvl = ""
            two_lvl = ""
            three_lvl = ""
            four_lvl = ""
            five_lvl = ""
            six_lvl = ""
        #await channel.send(f"# Bedwars Finals Leaderboard:# \n1. {one_final}\n2. {two_final}\n3. {three_final}\n4. {four_final}\n5. {five_final}\n6. {six_final}\n# Beds Broken Leaderboard: # \n1. {one_bed}\n2. {two_bed}\n3. {three_bed}\n4. {four_bed}\n5. {five_bed}\n6. {six_bed}\n# Bedwars Kills Leaderboard: #  \n1. {one_kill}\n2. {two_kill}\n3. {three_kill}\n4. {four_kill}\n5. {five_kill}\n6. {six_kill}\n# Bedwars Wins Leaderboard: # \n1. {one_win}\n2. {two_win}\n3. {three_win}\n4. {four_win}\n5. {five_win}\n6. {six_win}\n# Bedwars Level Leaderboad #\n1. {one_lvl}\n2. {two_lvl}\n3. {three_lvl}\n4. {four_lvl}\n5. {five_lvl}\n6. {six_lvl}")

    @bot.tree.command(name="duels")
    @app_commands.choices(gamemode=[c(name="Overall", value="overall"),c(name="UHC", value="uhc"), c(name="SkyWars", value="skywars"), c(name="MegaWalls", value="megawalls"), c(name="Blitz", value="blitz"), c(name="OP", value="op"), c(name="Classic", value="classic"), c(name="Bow", value="bow"), c(name="Combo", value="combo"), c(name="Sumo", value="sumo"), c(name="Bridge", value="bridge"), c(name="Parkour", value="parkour"), c(name="Boxing", value="boxing")])
    async def duels(interaction: discord.Interaction, username_or_uuid: str, gamemode: str = "overall"):
        await interaction.response.defer()

        username, uuid, c = await get_pretty_username(username_or_uuid, bedwars=False)

        # CONTINUE

        payload = {
            "key": f"{config.HYPIXEL_API}",
            "uuid": f"{uuid}"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.hypixel.net/v2/player', params=payload) as resp:
                status = resp.status
                r = await resp.json()

        duels = r["player"]["stats"]["Duels"]

        wins = losses= kills =deaths= bow_hits= bow_shots= blocks_placed= coins= loot_boxes= health_regened= damage_dealt= melee_hits= melee_swings = None

        pain = True
        if pain: # MASSIVE "IF" STATEMENT

            if gamemode.lower() == "overall":
                try: wins = duels["wins"]
                except: pass
                try: losses = duels["losses"]
                except: pass
                try: kills = duels["kills"]
                except: pass
                try: deaths = duels["deaths"]
                except: pass
                try: bow_shots = duels["bow_shots"]
                except: pass
                try: bow_hits = duels["bow_hits"]
                except: pass 
                try: blocks_placed = duels["blocks_placed"]
                except: pass
                try: coins = duels["coins"]
                except: pass
                try: loot_boxes = duels["duels_chests"]
                except: pass
                try: damage_dealt = duels["damage_dealt"]
                except: pass
                try: health_regened = duels["health_regenerated"]
                except: pass
                try: melee_hits = duels["melee_hits"]
                except: pass
                try: melee_swings = duels["melee_swings"]
                except: pass
            elif gamemode.lower() == "uhc":
                try: wins = duels["uhc_duel_wins"]
                except: pass
                try: losses = duels["uhc_duel_losses"]
                except: pass
                try: kills = duels["uhc_duel_kills"]
                except: pass
                try: deaths = duels["uhc_duel_deaths"]
                except: pass
                try: bow_shots = duels["uhc_duel_bow_shots"]
                except: pass
                try: bow_hits = duels["uhc_duel_bow_hits"]
                except: pass 
                try: blocks_placed = duels["uhc_duel_blocks_placed"]
                except: pass
                try: damage_dealt = duels["uhc_duel_damage_dealt"]
                except: pass
                try: health_regened = duels["uhc_duel_health_regenerated"]
                except: pass
                try: melee_hits = duels["uhc_duel_melee_hits"]
                except: pass
                try: melee_swings = duels["uhc_duel_melee_swings"]
                except: pass
            elif gamemode.lower() == "skywars":
                try: wins = duels["sw_duel_wins"]
                except: pass
                try: losses = duels["sw_duel_losses"]
                except: pass
                try: kills = duels["sw_duel_kills"]
                except: pass
                try: deaths = duels["sw_duel_deaths"]
                except: pass
                try: bow_shots = duels["sw_duel_bow_shots"]
                except: pass
                try: bow_hits = duels["sw_duel_bow_hits"]
                except: pass 
                try: blocks_placed = duels["sw_duel_blocks_placed"]
                except: pass
                try: damage_dealt = duels["sw_duel_damage_dealt"]
                except: pass
                try: health_regened = duels["sw_duel_health_regenerated"]
                except: pass
                try: melee_hits = duels["sw_duel_melee_hits"]
                except: pass
                try: melee_swings = duels["melee_swings"]
                except: pass
            elif gamemode.lower() == "megawalls":
                try: wins = duels["mw_duel_wins"]
                except: pass
                try: losses = duels["mw_duel_losses"]
                except: pass
                try: kills = duels["mw_duel_kills"]
                except: pass
                try: deaths = duels["mw_duel_deaths"]
                except: pass
                try: bow_shots = duels["mw_duel_bow_shots"]
                except: pass
                try: bow_hits = duels["mw_duel_bow_hits"]
                except: pass 
                try: blocks_placed = duels["mw_duel_blocks_placed"]
                except: pass
                try: damage_dealt = duels["mw_duel_damage_dealt"]
                except: pass
                try: health_regened = duels["mw_duel_health_regenerated"]
                except: pass
                try: melee_hits = duels["mw_duel_melee_hits"]
                except: pass
                try: melee_swings = duels["mw_duel_melee_swings"]
                except: pass
            elif gamemode.lower() == "blitz":
                try: wins = duels["blitz_duel_wins"]
                except: pass
                try: losses = duels["blitz_duel_losses"]
                except: pass
                try: kills = duels["blitz_duel_kills"]
                except: pass
                try: deaths = duels["blitz_duel_deaths"]
                except: pass
                try: bow_shots = duels["blitz_duel_bow_shots"]
                except: pass
                try: bow_hits = duels["blitz_duel_bow_hits"]
                except: pass 
                try: blocks_placed = duels["blitz_duel_blocks_placed"]
                except: pass
                try: damage_dealt = duels["blitz_duel_damage_dealt"]
                except: pass
                try: health_regened = duels["blitz_duel_health_regenerated"]
                except: pass
                try: melee_hits = duels["blitz_duel_melee_hits"]
                except: pass
                try: melee_swings = duels["blitz_duel_melee_swings"]
                except: pass
            elif gamemode.lower() == "op":
                try: wins = duels["op_duel_wins"]
                except: pass
                try: losses = duels["op_duel_losses"]
                except: pass
                try: kills = duels["op_duel_kills"]
                except: pass
                try: deaths = duels["op_duel_deaths"]
                except: pass
                try: bow_shots = duels["op_duel_bow_shots"]
                except: pass
                try: bow_hits = duels["op_duel_bow_hits"]
                except: pass 
                try: blocks_placed = duels["op_duel_blocks_placed"]
                except: pass
                try: damage_dealt = duels["op_duel_damage_dealt"]
                except: pass
                try: health_regened = duels["op_duel_health_regenerated"]
                except: pass
                try: melee_hits = duels["op_duel_melee_hits"]
                except: pass
                try: melee_swings = duels["op_duel_melee_swings"]
                except: pass
            elif gamemode.lower() == "classic":
                try: wins = duels["classic_duel_wins"]
                except: pass
                try: losses = duels["classic_duel_losses"]
                except: pass
                try: kills = duels["classic_duel_kills"]
                except: pass
                try: deaths = duels["classic_duel_deaths"]
                except: pass
                try: bow_shots = duels["classic_duel_bow_shots"]
                except: pass
                try: bow_hits = duels["classic_duel_bow_hits"]
                except: pass 
                try: blocks_placed = duels["classic_duel_blocks_placed"]
                except: pass
                try: damage_dealt = duels["classic_duel_damage_dealt"]
                except: pass
                try: health_regened = duels["classic_duel_health_regenerated"]
                except: pass
                try: melee_hits = duels["classic_duel_melee_hits"]
                except: pass
                try: melee_swings = duels["classic_duel_melee_swings"]
                except: pass
            elif gamemode.lower() == "bow":
                try: wins = duels["bow_duel_wins"]
                except: pass
                try: losses = duels["bow_duel_losses"]
                except: pass
                try: kills = duels["bow_duel_kills"]
                except: pass
                try: deaths = duels["bow_duel_deaths"]
                except: pass
                try: bow_shots = duels["bow_duel_bow_shots"]
                except: pass
                try: bow_hits = duels["bow_duel_bow_hits"]
                except: pass 
                try: blocks_placed = duels["bow_duel_blocks_placed"]
                except: pass
                try: damage_dealt = duels["bow_duel_damage_dealt"]
                except: pass
                try: health_regened = duels["bow_duel_health_regenerated"]
                except: pass
                try: melee_hits = duels["bow_duel_melee_hits"]
                except: pass
                try: melee_swings = duels["bow_duel_melee_swings"]
                except: pass
            elif gamemode.lower() == "combo":
                try: wins = duels["combo_duel_wins"]
                except: pass
                try: losses = duels["combo_duel_losses"]
                except: pass
                try: kills = duels["combo_duel_kills"]
                except: pass
                try: deaths = duels["combo_duel_deaths"]
                except: pass
                try: bow_shots = duels["combo_duel_bow_shots"]
                except: pass
                try: bow_hits = duels["combo_duel_bow_hits"]
                except: pass 
                try: blocks_placed = duels["combo_duel_blocks_placed"]
                except: pass
                try: damage_dealt = duels["combo_duel_damage_dealt"]
                except: pass
                try: health_regened = duels["combo_duel_health_regenerated"]
                except: pass
                try: melee_hits = duels["combo_duel_melee_hits"]
                except: pass
                try: melee_swings = duels["combo_duel_melee_swings"]
                except: pass
            elif gamemode.lower() == "sumo":
                try: wins = duels["sumo_duel_wins"]
                except: pass
                try: losses = duels["sumo_duel_losses"]
                except: pass
                try: kills = duels["sumo_duel_kills"]
                except: pass
                try: deaths = duels["sumo_duel_deaths"]
                except: pass
                try: bow_shots = duels["sumo_duel_bow_shots"]
                except: pass
                try: bow_hits = duels["sumo_duel_bow_hits"]
                except: pass 
                try: blocks_placed = duels["sumo_duel_blocks_placed"]
                except: pass
                try: damage_dealt = duels["sumo_duel_damage_dealt"]
                except: pass
                try: health_regened = duels["sumo_duel_health_regenerated"]
                except: pass
                try: melee_hits = duels["sumo_duel_melee_hits"]
                except: pass
                try: melee_swings = duels["sumo_duel_melee_swings"]
                except: pass
            elif gamemode.lower() == "bridge":
                try: wins = duels["bridge_duel_wins"]
                except: pass
                try: losses = duels["bridge_duel_losses"]
                except: pass
                try: kills = duels["bridge_kills"]
                except: pass
                try: deaths = duels["bridge_deaths"]
                except: pass
                try: bow_shots = duels["bridge_duel_bow_shots"]
                except: pass
                try: bow_hits = duels["bridge_duel_bow_hits"]
                except: pass 
                try: blocks_placed = duels["bridge_duel_blocks_placed"]
                except: pass
                try: damage_dealt = duels["bridge_duel_damage_dealt"]
                except: pass
                try: health_regened = duels["bridge_duel_health_regenerated"]
                except: pass
                try: melee_hits = duels["bridge_duel_melee_hits"]
                except: pass
                try: melee_swings = duels["bridge_duel_melee_swings"]
                except: pass
            elif gamemode.lower() == "parkour":
                try: wins = duels["parkour_eight_wins"]
                except: pass
                try: losses = duels["parkour_eight_losses"]
                except: pass
                try: kills = duels["parkour_eight_kills"]
                except: pass
                try: deaths = duels["parkour_eight_deaths"]
                except: pass
                try: bow_shots = duels["parkour_eight_bow_shots"]
                except: pass
                try: bow_hits = duels["parkour_eight_bow_hits"]
                except: pass 
                try: blocks_placed = duels["parkour_eight_blocks_placed"]
                except: pass
                try: damage_dealt = duels["parkour_eight_damage_dealt"]
                except: pass
                try: health_regened = duels["parkour_eight_health_regenerated"]
                except: pass
                try: melee_hits = duels["parkour_eight_melee_hits"]
                except: pass
                try: melee_swings = duels["parkour_eight_melee_swings"]
                except: pass
            elif gamemode.lower() == "boxing":
                try: wins = duels["boxing_duel_wins"]
                except: pass
                try: losses = duels["boxing_duel_losses"]
                except: pass
                try: kills = duels["boxing_duel_kills"]
                except: pass
                try: deaths = duels["boxing_duel_deaths"]
                except: pass
                try: bow_shots = duels["boxing_duel_bow_shots"]
                except: pass
                try: bow_hits = duels["boxing_duel_bow_hits"]
                except: pass 
                try: blocks_placed = duels["boxing_duel_blocks_placed"]
                except: pass
                try: damage_dealt = duels["boxing_duel_damage_dealt"]
                except: pass
                try: health_regened = duels["boxing_duel_health_regenerated"]
                except: pass
                try: melee_hits = duels["boxing_duel_melee_hits"]
                except: pass
                try: melee_swings = duels["boxing_duel_melee_swings"]
                except: pass

        if gamemode.lower() == "overall":
            stuff = "duels stats"
        else:
            stuff = f"{prettify(gamemode)} duels stats"

        if gamemode.lower() == "overall":
            embed = discord.Embed(
                title=f"{username}'s {stuff}",
                color=c
            )
            try: embed.add_field(name="Wins", value=f"Wins: {wins:,} \nLosses: {losses:,}\n-------------\nWLR: {round(int(wins)/int(losses), 2)}")
            except: embed.add_field(name="Wins", value=f"Wins: Unknown \nLosses: Unknown\n-------------\nWLR: Unknown")
            try: embed.add_field(name="Kills", value=f"Kills: {kills:,} \nDeaths: {deaths:,}\n-------------\nKDR: {round(int(kills)/int(deaths), 2)}")
            except: embed.add_field(name="Kills", value=f"Kills: Unknown \nDeaths: Unknown\n-------------\nKDR: Unknown")
            try: embed.add_field(name="Blocks", value=f"Blocks placed: {blocks_placed:,}\n\n-------------\n")
            except: embed.add_field(name="Blocks", value=f"Blocks placed: Unknown\n\n-------------\n")
            try: embed.add_field(name="Damage", value=f"Dealt: {damage_dealt:,} \nRegenerated: {health_regened:,}\n-------------\n")
            except: embed.add_field(name="Damage", value=f"Dealt: Unknown \nRegenerated: Unknown\n-------------\n")
            try: embed.add_field(name="Coins", value=f"Balance: {coins:,}\n\n-------------\n")
            except: embed.add_field(name="Coins", value=f"Balance: Unknown\n\n-------------\n")
            try: embed.add_field(name="Loot chests", value=f"Amount: {loot_boxes:,}\n\n-------------\n")
            except: embed.add_field(name="Loot chests", value=f"Amount: Unknown\n\n-------------\n")
            embed.set_thumbnail(url=await get_3d_head(uuid))
        else:
            embed = discord.Embed(
                title=f"{username}'s {stuff}",
                color=c
            )

            try: embed.add_field(name="Wins", value=f"Wins: {wins:,} \nLosses: {losses:,}\n-------------\nWLR: {round(int(wins)/int(losses), 2)}")
            except: embed.add_field(name="Wins", value=f"Wins: Unknown \nLosses: Unknown\n-------------\nWLR: Unknown")
            try:embed.add_field(name="Kills", value=f"Kills: {kills:,} \nDeaths: {deaths:,}\n-------------\nKDR: {round(int(kills)/int(deaths), 2)}")
            except: embed.add_field(name="Kills", value=f"Kills: Unknown \nDeaths: Unknown\n-------------\nKDR: Unknown")
            try: embed.add_field(name="Bow", value=f"Bow hits: {bow_hits:,} \nBow Misses: {bow_shots-bow_hits:,}\n-------------\nBHMR: {round(int(bow_hits)/int(bow_shots-bow_hits), 2)}")
            except: embed.add_field(name="Bow", value=f"Bow hits: Unknown \nBow Misses: Unknown\n-------------\nBHMR: Unknown")
            try:embed.add_field(name="Blocks", value=f"Blocks placed: {blocks_placed:,}\n\n-------------\n")
            except: embed.add_field(name="Blocks", value=f"Blocks placed: Unknown\n\n-------------\n")
            try:embed.add_field(name="Damage", value=f"Dealt: {damage_dealt:,} \nRegenerated: {health_regened:,}\n-------------\n")
            except: embed.add_field(name="Damage", value=f"Dealt: Unknown \nRegenerated: Unknown\n-------------\n")
            try:embed.add_field(name="Melee", value=f"Hits: {melee_hits:,} \nMisses: {melee_swings-melee_hits:,}\n-------------\nMHMR: {round(int(melee_hits)/int(melee_swings-melee_hits), 2)}")
            except: embed.add_field(name="Melee", value=f"Hits: Unknown \nMisses: Unknown\n-------------\nMHMR: Unknown")
            
            embed.set_footer(text="BHMR = Bow Hit Miss Ratio | MHMR = Melee Hit Miss Ratio")
            embed.set_thumbnail(url=await get_3d_head(uuid))

        await interaction.followup.send(embed=embed)

    @bot.tree.command(name="bedwars-cosmetics")
    async def bedwars_cosmetics(interaction: discord.Interaction, username_or_uuid: str):
        await interaction.response.defer()

        username, uuid, c = await get_pretty_username(username_or_uuid)

        payload = {
            "key": f"{config.HYPIXEL_API}",
            "uuid": f"{uuid}"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.hypixel.net/v2/player', params=payload) as resp:
                status = resp.status
                r = await resp.json()

        bedwars = r["player"]["stats"]["Bedwars"]
        
        try: victory_dance = str(bedwars["activeVictoryDance"]).replace("_", " ").lower().title().replace("Victorydance", " ")
        except: victory_dance = "Unknown"
        try: kill_message = str(bedwars["activeKillMessages"]).replace("_", " ").lower().title().replace("Killmessages", " ")
        except: kill_message = "Unknown"
        try: final_effect = str(bedwars["activeKillEffect"]).replace("_", " ").lower().title().replace("Killeffect", " ")
        except: final_effect = "Unknown"
        try: island_topper = str(bedwars["activeIslandTopper"]).replace("_", " ").lower().title().replace("Islandtopper", " ")
        except: island_topper = "Unknown"
        try: death_cry = str(bedwars["activeDeathCry"]).replace("_", " ").lower().title().replace("Deathcry", " ")
        except: death_cry = "Unknown"
        try: shopkeeper = str(bedwars["activeNPCSkin"]).replace("_", " ").lower().title().replace("Npcskin", " ")
        except: shopkeeper = "Unknown"
        try: bed_break = str(bedwars["activeBedDestroy"]).replace("_", " ").lower().title().replace("Beddestroy", " ")
        except: bed_break = "Unknown"
        try: wood_skin = str(bedwars["activeWoodType"]).replace("_", " ").lower().title().replace("Woodskin", " ")
        except: wood_skin = "Unknown"
        try: figurines = str(bedwars["figurines"]["active"]).replace("_", " ").lower().title().replace("Figurine", " ")
        except: figurines = "Unknown"
        try: glyphs = str(bedwars["activeGlyph"]).replace("_", " ").lower().title().replace("Glyph", " ")
        except: glyphs = "Unknown"
        try: projectile_trail = str(bedwars["activeProjectileTrail"]).replace("_", " ").lower().title().replace("Projectiletrail", " ")
        except: projectile_trail = "Unknown"
        try: spray = str(bedwars["activeSprays"]).replace("_", " ").lower().title().replace("Sprays", " ").replace(" Plus", "+")
        except: spray = "Unknown"

        embed = discord.Embed(title=f"{username}'s cosmetics", color=c)
        embed.add_field(name="Vicctory Dance", value=f"{victory_dance}")
        embed.add_field(name="Kill message", value=f"{kill_message}")
        embed.add_field(name="Final kill effect", value=f"{final_effect}")
        embed.add_field(name="Island Topper", value=f"{island_topper}")
        embed.add_field(name="Death cry", value=f"{death_cry}")
        embed.add_field(name="Shopkeeper Skin", value=f"{shopkeeper}")
        embed.add_field(name="Bed Break Effect", value=f"{bed_break}")
        embed.add_field(name="Wood Skin", value=f"{wood_skin}")
        embed.add_field(name="Figurine", value=f"{figurines}")
        embed.add_field(name="Glyphs", value=f"{glyphs}")
        embed.add_field(name="Projectile Trail", value=f"{projectile_trail}")
        embed.add_field(name="Spray", value=f"{spray}")

        embed.set_thumbnail(url=await get_3d_head(uuid))

        await interaction.followup.send(embed=embed)

    @bot.tree.command(name="bedwars")
    async def bedwars(interaction: discord.Interaction, username_or_uuid: str):
        await interaction.response.defer()
        
        name, uuid, c = await get_pretty_username(username_or_uuid)

        payload = {
            "key": f"{config.HYPIXEL_API}",
            "uuid": f"{uuid}"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.hypixel.net/v2/player', params=payload) as resp:
                status = resp.status
                json_stuff = await resp.json()
                bedwars = json_stuff["player"]["stats"]["Bedwars"]

        username = f"{name}"

        if status != 200:
            await interaction.followup.send("The API didn't respond. Try again later.")

        finals = bedwars["final_kills_bedwars"]
        final_deaths = bedwars["final_deaths_bedwars"]
        
        beds = bedwars["beds_broken_bedwars"]
        beds_lost = bedwars["beds_lost_bedwars"]
        
        wins = bedwars["wins_bedwars"]
        losses = bedwars["losses_bedwars"]

        kills = bedwars["kills_bedwars"]
        deaths = bedwars["deaths_bedwars"]

        coins = bedwars["coins"]
        slumber = True
        try:
            s_tickets = bedwars["slumber"]["tickets"]
            total_s_tickets = bedwars["slumber"]["total_tickets_earned"]
            bag_type = str(bedwars["slumber"]["bag_type"]).lower().replace("_", " ").title()
        except KeyError:
            slumber = False

        loot_chests = bedwars["bedwars_boxes"]
        opened_loot_chests = bedwars["Bedwars_openedChests"]
        embed = discord.Embed(
            title=f"{username}'s Bedwars Stats",
            color=c
        )


        embed.add_field(name="Finals", value=f"Final Kills: {finals} \nFinal Deaths: {final_deaths}\n-------------\nFKDR: {round(int(finals)/int(final_deaths), 2)}")
        embed.add_field(name="Beds", value=f"Beds Broken: {beds} \nBeds Lost: {beds_lost}\n-------------\nBBLR: {round(int(beds)/int(beds_lost), 2)}")
        embed.add_field(name="Wins/Losses", value=f"Wins: {wins}\nLosses: {losses}\n-------------\nWLR: {round(int(wins)/int(losses), 2)}")
        embed.add_field(name="Kills", value=f"Kills: {kills}\nDeaths: {deaths}\n-------------\nKDR: {round(int(kills)/int(deaths), 2)}")
        embed.add_field(name="Coins etc.", value=f"Coins: {coins:,}\nLoot chests: {loot_chests}\n-------------\nOpened chests: {opened_loot_chests}")
        if slumber:
            embed.add_field(name="Slumber Tickets", value=f"Ticket balance: {s_tickets:,}\nGathered tickets: {total_s_tickets:,}\n-------------\nWallet type: {bag_type}")

        embed.set_thumbnail(url=await get_3d_head(uuid))

        await interaction.followup.send(embed=embed)

    @bot.tree.command(name="bedwars-quickbuy")
    async def bedwars_quickbuy(interaction: discord.Interaction, username_or_uuid: str):
        await interaction.response.defer()
        
        username, uuid, c = await get_pretty_username(username_or_uuid)

        sent_error = False
        failed = False

        payload = {
            "key": f"{config.POLSU_API}",
            "uuid": f"{uuid}"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.polsu.xyz/polsu/bedwars/quickbuy', params=payload) as resp:
                status = resp.status
                r = await resp.json()

        url = r["data"]["image"]

        file_name = f"images/{uuid}.png"

        res = requests.get(url, stream = True)

        if res.status_code == 200:
            with open(file_name,'wb') as f:
                shutil.copyfileobj(res.raw, f)
        else:
            failed = True
            await interaction.followup.send("An error accured, try again later!")

        if failed == True and sent_error == False:
            await interaction.followup.send("An error accured, try again later!")
            pass
        else:
            img = Image.open(file_name)
            cropped = img.crop((413, 445, 1135, 685))
            cropped.save(f"{file_name}")

            embed = discord.Embed(
                title=f"{username}'s Bedwars Quickbuy",
                color=c
            )
            f = discord.File(f"images/{uuid}.png", filename=f"{uuid}.png")
            embed.set_image(url=f"attachment://{uuid}.png")
            embed.set_footer(text="Image via Polsu", icon_url="https://cdn.discordapp.com/avatars/875663466181058592/dabce48085a0fc414f474f3abad12416.webp?size=160")

            await interaction.followup.send(file=f, embed=embed)


        
        os.remove(f"{file_name}")
        
    @bot.tree.command(name="bedwars-map")
    async def bedwars_map(interaction: discord.Interaction, map: str):
        await interaction.response.defer()
        name = map.capitalize().replace("%20", " ")
        map_name = name.replace("%27", "'")
        map_value = map

        payload = {
            "key": f"{config.POLSU_API}",
            "map": f"{map_value}"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.polsu.xyz/polsu/bedwars/map', params=payload) as resp:
                status = resp.status
                r = await resp.json()

        try:
            image = r["data"]["preview"]
        except KeyError:
            await interaction.followup.send(f"Unknown map {map_name} (maybe a spelling error?)")
            return
        playstyle = r["data"]["playstyle"]
        gen = r["data"]["gen"]
        builders = r["data"]["builders"]
        desc = r["data"]["description"]
        rotation = r["data"]["inRotation"]
        def if_gen(generator):
            if generator:
                return f"It has a **{gen.lower()}** resource generator."
            return " "

        embed=discord.Embed(
            title=f"{map_name}", 
            color=discord.Color.random(),
            description=f"{map_name} is a **{playstyle.lower()}** map that was made by **{builders}**. {if_gen(generator=gen)}\n{desc}"
        )
        
        embed.add_field(name="In rotation?", value=f"{rotation}", inline=False)
        embed.set_footer(text="Hypickle")
        embed.set_image(url=f"{image}")
        
        await interaction.followup.send(embed=embed)

    @bedwars_map.autocomplete('map')
    async def bedwars_map_autocomplete(interaction: discord.Interaction, current: str):
        
        autocompleted_maps = []

        for map_name in utils.maps:
            if map_name.name.lower().startswith(current.lower()):
                if len(autocompleted_maps) < 25:
                    autocompleted_maps.append(map_name)
                else:
                    break

        return autocompleted_maps


    @bot.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return


        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


    bot.run(secret)

if __name__ == '__main__':
    bot = commands.Bot(command_prefix=config.PREFIX, intents=config.INTENTS, activity=discord.Game(name="on lagpixel"))
    # bot.remove_command("help")
    main(config.TOKEN, bot)




