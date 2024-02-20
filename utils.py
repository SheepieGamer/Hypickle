import config
import discord, aiohttp 
from discord.app_commands import Choice as c

async def print_user(bot):
    print(f"User: {bot.user} (ID: {bot.user.id})")

async def load_cogs(bot):
    for cog_file in config.COGS_DIR.glob("*.py"):
        if cog_file.name != "__init__.py":
            await bot.load_extension(f"cogs.{cog_file.name[:-3]}")
            print(f"cogs.{cog_file.name[:-3]} successfully loaded")

async def load_cmds(bot):
    for cmd_file in config.CMDS_DIR.glob("*.py"):
        if cmd_file.name != "__init__.py":
            await bot.load_extension(f"cmds.{cmd_file.name[:-3]}")
            print(f"cmds.{cmd_file.name[:-3]} successfully loaded")

maps = [
        c(name="Acropolis", value="acropolis"),
        c(name="Airshow", value="airshow"),
        c(name="Alaric", value="alaric"),
        c(name="Amazon", value="amazon"),
        c(name="Ambush", value="ambush"),
        c(name="Apollo", value="apollo"),
        c(name="Aqil", value="aqil"),
        c(name="Aquarium", value="aquarium"),
        c(name="Archway", value="archway"),
        c(name="Artemis", value="artemis"),
        c(name="Ashfire", value="ashfire"),
        c(name="Ashore", value="ashore"),
        c(name="Babylon", value="babylon"),
        c(name="Beeeee", value="beeeee"),
        c(name="Bio-Hazard", value="bio-hazard"),
        c(name="Blitzen", value="blitzen"),
        c(name="Blossom", value="blossom"),
        c(name="Boardwalk", value="boardwalk"),
        c(name="Boletum", value="boletum"),
        c(name="Build Site", value="build%20site"),
        c(name="Bunnywars", value="bunnywars"),
        c(name="Burrow", value="burrow"),
        c(name="Carapace", value="carapace"),
        c(name="Cascade", value="cascade"),
        c(name="Casita", value="casita"),
        c(name="Castle", value="castle"),
        c(name="Catalyst", value="catalyst"),
        c(name="Cauldron", value="cauldron"),
        c(name="Chained", value="chained"),
        c(name="Cliffside", value="cliffside"),
        c(name="Coastal", value="coastal"),
        c(name="Comet", value="comet"),
        c(name="Crogorm", value="crogorm"),
        c(name="Crypt", value="crypt"),
        c(name="Cryptic", value="cryptic"),
        c(name="Daolong", value="daolong"),
        c(name="Darkened", value="darkened"),
        c(name="Deadwood", value="deadwood"),
        c(name="Deposit", value="deposit"),
        c(name="Dockyard", value="dockyard"),
        c(name="Dragonstar", value="dragonstar"),
        c(name="Dreamgrove", value="dreamgrove"),
        c(name="Easter Basket", value="easter%20basket"),
        c(name="Easter Garden", value="easter%20garden"),
        c(name="Eastwood", value="eastwood"),
        c(name="Eastwood Lunar", value="eastwood%20lunar"),
        c(name="Egg Run", value="egg%20hunt"),
        c(name="Egg hunt", value="egg%20run"),
        c(name="Enchanted", value="enchanted"),
        c(name="Entangle", value="entangle"),
        c(name="Extinction", value="extinction"),
        c(name="Fang Outpost", value="fang%20outpost"),
        c(name="Fireplace", value="fireplace"),
        c(name="Fort Doon", value="fort%20doon"),
        c(name="Frogiton", value="frogiton"),
        c(name="Frost", value="frost"),
        c(name="Frosted", value="frosted"),
        c(name="Fruitbrawl", value="fruitbrawl"),
        c(name="Gardens", value="gardens"),
        c(name="Gateway", value="gateway"),
        c(name="Gelato", value="gelato"),
        c(name="Ghoulish", value="ghoulish"),
        c(name="Gingerbread", value="gingerbread"),
        c(name="Glacier", value="glacier"),
        c(name="Graveship", value="graveship"),
        c(name="Grotto", value="grotto"),
        c(name="Harvest", value="harvest"),
        c(name="Hell Temple", value="hell%20temple"),
        c(name="Hollow", value="hollow"),
        c(name="Holmgang", value="holmgang"),
        c(name="Horizon", value="horizon"),
        c(name="Impere", value="impere"),
        c(name="Infinite", value="infinite"),
        c(name="Invasion", value="invasion"),
        c(name="Invicta", value="invicta"),
        c(name="Ironclad", value="ironclad"),
        c(name="Jurassic", value="jurassic"),
        c(name="Katsu", value="katsu"),
        c(name="Kubo", value="kubo"),
        c(name="Lectus", value="lectus"),
        c(name="Lighthouse", value="lighthouse"),
        c(name="Lighthouse Lunar", value="lighthouse%20lunar"),
        c(name="Lightstone", value="lightstone"),
        c(name="Lions Temple", value="lions%20temple"),
        c(name="Loft", value="loft"),
        c(name="Lotice", value="lotice"),
        c(name="Lotus", value="lotus"),
        c(name="Lucky Rush", value="lucky%20rush"),
        c(name="Meadow", value="meadow"),
        c(name="Meso", value="meso"),
        c(name="Mirage", value="mirage"),
        c(name="Montipora", value="montipora"),
        c(name="Mortuss", value="mortuus"),
        c(name="Mosdalr", value="mosdalr"),
        c(name="Nutcracker", value="nutcracker"),
        c(name="Obelisk", value="obelisk"),
        c(name="Ominosity", value="ominosity"),
        c(name="Orbit", value="orbit"),
        c(name="Orchestra", value="orchestra"),
        c(name="Orchid", value="orchid"),
        c(name="Paladin", value="paladin"),
        c(name="Paradox", value="paradox"),
        c(name="Pavilion", value="pavilion"),
        c(name="Pernicious", value="pernicious"),
        c(name="Pharaoh", value="pharaoh"),
        c(name="Picnic", value="picnic"),
        c(name="Planet 98", value="planet%2098"),
        c(name="Playground", value="playground"),
        c(name="Polemus", value="polemus"),
        c(name="Polygon", value="polygon"),
        c(name="Pool Party", value="pool%20party"),
        c(name="Pumpkin Bay", value="pumpkin%20bay"),
        c(name="Raze", value="raze"),
        c(name="Relic", value="relic"),
        c(name="Rise", value="rise"),
        c(name="Rooftop", value="rooftop"),
        c(name="Rooted", value="rooted"),
        c(name="Ruins", value="ruins"),
        c(name="Sanctum", value="sanctum"),
        c(name="Sandcastle", value="sandcastle"),
        c(name="Santa's Rush", value="santa%27s%20rush"),
        c(name="Scareshow", value="scareshow"),
        c(name="Scorched Sands", value="scorched%20sands"),
        c(name="Screamway", value="screamway"),
        c(name="Serenity", value="serenity"),
        c(name="Shark Attack", value="shark%20attack"),
        c(name="Siege", value="siege"),
        c(name="Sky Festival", value="sky%20festival"),
        c(name="Sky Rise", value="sky%20rise"),
        c(name="Snowkeep", value="snowkeep"),
        c(name="Snowy Square", value="snowy%20square"),
        c(name="Solace", value="solace"),
        c(name="Speedway", value="speedway"),
        c(name="Springtide", value="springtide"),
        c(name="Steampumpkin", value="steampumpkin"),
        c(name="Steampunk", value="steampunk"),
        c(name="Stilted", value="stilted"),
        c(name="Stonekeep", value="stonekeep"),
        c(name="Sunflower", value="sunflwoer"),
        c(name="Swashbuckle", value="swashbuckle"),
        c(name="Sweet Wonderland", value="sweet%20wonderland"),
        c(name="Symphonic", value="symphonic"),
        c(name="Temple", value="temple"),
        c(name="Terminal", value="terminal"),
        c(name="Tigris", value="tigris"),
        c(name="Toro", value="toro"),
        c(name="Treenan", value="treenan"),
        c(name="Trick or Yeet", value="trick%20or%20yeet"),
        c(name="Tuzi", value="tuzi"),
        c(name="Unchained", value="unchained"),
        c(name="Unturned", value="unturned"),
        c(name="Urban Plaza", value="urban%20plaza"),
        c(name="Usagi", value="usagi"),
        c(name="Varyth", value="varyth"),
        c(name="Waterfall", value="waterfall"),
        c(name="Winterland", value="winterland"),
        c(name="Yue", value="yue"),
        c(name="Zarzul", value="zarzul"),
        c(name="Zen Plaza", value="zen%20plaza")

    
    ]

async def other(bot):
    # bot.tree.copy_global_to(guild=bot.guilds[0])
    # await bot.tree.sync(guild=bot.guilds[0])
    # print("Tree synced")
    print("--")
    print("--")

async def get_uuid(username: str) -> str:
    payload = {
        "key": f"{config.POLSU_API}",
        "player": f"{username}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.polsu.xyz/polsu/minecraft/player', params=payload) as resp:
            status = resp.status
            r = await resp.json()
            return r["data"]["uuid"]
        
async def get_plain_name(username: str) -> str:
    payload = {
        "key": f"{config.POLSU_API}",
        "player": f"{username}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.polsu.xyz/polsu/minecraft/player', params=payload) as resp:
            status = resp.status
            r = await resp.json()
            return r["data"]["username"]
        
def get_bedwars_level(xp: int) -> float | int:
    """
    Get a player's precise bedwars level from their experience
    :param xp: Player's bedwars experience
    """
    level: int = 100 * (xp // 487000)  # prestige
    xp %= 487000  # exp this prestige
    xp_map: tuple = (0, 500, 1500, 3500, 7000)

    for index, value in enumerate(xp_map):
        if xp < value:
            factor: int = xp_map[index-1]
            return level + ((xp - factor) / (value - factor)) + (index - 1)
    return level + (xp - 7000) / 5000 + 4

async def get_3d_head(uuid) -> str:
    payload = {
        "key": f"{config.POLSU_API}",
        "uuid": f"{uuid}"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.polsu.xyz/polsu/minecraft/player/skin/head3d', params=payload) as resp:
            status = resp.status
            r = await resp.json()

    return r["data"]["link"]

async def get_pretty_username(username_or_uuid: str, bedwars: bool = True):
        payload = {
            "key": f"{config.POLSU_API}",
            "player": f"{username_or_uuid}"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.polsu.xyz/polsu/minecraft/player', params=payload) as resp:
                status = resp.status
                r = await resp.json()
                uuid = r["data"]["uuid"]
                name = r["data"]["username"]

        payload = {
            "key": f"{config.HYPIXEL_API}",
            "uuid": f"{uuid}"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.hypixel.net/v2/player', params=payload) as resp:
                status = resp.status
                r = await resp.json()

        xp = r["player"]["stats"]["Bedwars"]["Experience"]

        try:
            package_rank = r["player"]["newPackageRank"]
        except:
            package_rank = "default"
            c = discord.Color.dark_embed()

        if package_rank == "MVP_PLUS":
            package_rank = "[MVP+]"
            c = discord.Color.teal()
        elif package_rank == "MVP":
            package_rank = "[MVP]"
            c = discord.Color.teal()
        elif package_rank == "VIP_PLUS":
            package_rank = "[VIP+]"
            c = discord.Color.brand_green()
        elif package_rank == "VIP":
            package_rank = "[VIP]"
            c = discord.Color.brand_green()
        elif package_rank == "default":
            package_rank = " "
            c = discord.Color.dark_embed()
        else:
            package_rank = " "
            c = discord.Color.dark_embed()

        try:
            if r["player"]["monthlyPackageRank"] and r["player"]["monthlyPackageRank"] != "NONE":
                package_rank = "[MVP++]"
                c = discord.Color.gold()
        except:
            pass

        username = f"{package_rank} {name}"



        star = get_bedwars_level(xp)

        if bedwars:
            username = f"{username}   ✬{int(star)}"

        return username, uuid, c

def prettify(text):
    return f"{text}".lower().replace("_", " ").replace("-", " ").title()

