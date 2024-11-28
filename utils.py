from discord.app_commands import Choice as c
from settings import POLSU_TOKEN, HYPIXEL_TOKEN, DISCORD_TOKEN
import json
import time
from maps import maps
import aiohttp
import discord


async def get_user(uuid: str):
    """Get user data from Hypixel API"""
    uuid = uuid.strip("-")

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.hypixel.net/v2/player?key={HYPIXEL_TOKEN}&uuid={uuid}") as resp:
            if resp.status != 200:
                print(f"Get_User: API Error: Status {resp.status}")
                return None
            data = await resp.json()
            if not data.get("success", False):
                print(f"Get_User: API Error: {data.get('cause', 'Unknown error')}")
                return None
            return data

# Skin Functions

async def get_3d_head(uuid: str):
    """Get 3D head render URL from polsu.xyz API"""
    try:
        async with aiohttp.ClientSession() as session:
            headers = {'Api-Key': POLSU_TOKEN}
            async with session.get(f"https://api.polsu.xyz/polsu/minecraft/player/skin/head3d?uuid={uuid}", headers=headers) as resp:
                if resp.status != 200:
                    print(f"3d_Head: API Error: Status {resp.status}")
                    return None
                data = await resp.json()
                url = data["data"]["link"]
                print(f"3d_Head: {url}")
                return url
    except Exception as e:
        print(f"3d_Head: Error: {e}")
        return None

async def get_3d_body(uuid: str):
    try:
        async with aiohttp.ClientSession() as session:
            headers = {'Api-Key': POLSU_TOKEN}
            async with session.get(f"https://api.polsu.xyz/polsu/minecraft/player/skin/body?uuid={uuid}", headers=headers) as resp:
                if resp.status != 200:
                    print(f"3d_Body: API Error: Status {resp.status}")
                    return None
                data = await resp.json()
                url = data["data"]["link"]
                print(f"3d_Body: {url}")
                return url
    except Exception as e:
        print(f"3d_Body: Error: {e}")
        return None

# Username Functions

async def get_rank(username):
    uuid = str(await get_uuid(username)).strip("-")
    data = await get_user(uuid)
    if not data or "player" not in data:
        return ""

    player = data["player"]
    
    # Check for special ranks first
    try:
        if player.get("monthlyPackageRank") == "SUPERSTAR":
            return "MVP++"
        elif player.get("monthlyPackageRank") == "NONE" and player.get("newPackageRank") == "MVP_PLUS":
            return "MVP+"
    except: 
        pass

    # Check regular ranks
    try:
        rank = player.get("newPackageRank", "")
        if rank == "MVP_PLUS":
            return "MVP+"
        elif rank == "MVP":
            return "MVP"
        elif rank == "VIP_PLUS":
            return "VIP+"
        elif rank == "VIP":
            return "VIP"
    except:
        pass

    return ""

async def get_username(uuid: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}") as resp:
            if resp.status != 200:
                print(f"Get_Username: API Error: Status {resp.status}")
                return None
            data = await resp.json()
            username = data["name"]
            print(f"Get_Username: API response: {username}")  # Debug print
            return username

async def get_uuid(username: str):
    ts = time.time()
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.mojang.com/users/profiles/minecraft/{username}?at={ts}") as resp:
            if resp.status != 200:
                print(f"Get_Uuid: API Error: Status {resp.status}")
                return None
            data = await resp.json()
            uuid = data["id"]
            print(f"Get_Uuid: API response: {uuid}")  # Debug print
            return uuid

async def get_pretty_username(username: str, bedwars: bool = True):
    uuid = await get_uuid(username)
    username = await get_username(uuid)
    rank = await get_rank(username)
    new_rank = f"[{rank}]" if rank != "" else ""

    if bedwars:
        star = get_star(await fetch_xp(username))

        name = f"[{star}✬] {new_rank} {username}"
        return name, uuid

    name = f"{new_rank} {username}"
    return name, uuid

# Text Functions

def prettify(text):
    return f"{text}".lower().replace("_", " ").replace("-", " ").title()

def to_roman_numeral(num: int) -> str:
    """Convert an integer to Roman numeral.
    
    Args:
        num (int): Number to convert (1-3999)
    
    Returns:
        str: Roman numeral representation
    """
    if not isinstance(num, int) or num < 1 or num > 3999:
        return str(num)
        
    val = [1000, 900, 500, 400, 100,   90,   50,  40,  10,   9,    5,   4,    1]
    syb = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    roman_num = ''
    i = 0
    
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    
    return roman_num


#### GAME FUNCTIONS

# Duels Functions

async def get_duels_coins(uuid: str):
    """Get duels coins from Hypixel API"""
    uuid = uuid.strip("-")

    data = await get_user(uuid)
    
    try:
        if data and "player" in data and data["player"] and "stats" in data["player"] and "Duels" in data["player"]["stats"]:
            coins = data["player"]["stats"]["Duels"]["coins"]
            print(f"Get_Duels_Coins: API response: {coins}")
            return coins
        print("Get_Duels_Coins: No duels data found")
        return 0
    except KeyError:
        print("Get_Duels_Coins: Error accessing duels data")
        return 0

async def get_duels_blocks(uuid: str):
    """Get duels blocks from Hypixel API"""
    uuid = uuid.strip("-")

    data = await get_user(uuid)
    
    try:
        if data and "player" in data and data["player"] and "stats" in data["player"] and "Duels" in data["player"]["stats"]:
            blocks = data["player"]["stats"]["Duels"]["blocks_placed"]
            print(f"Get_Duels_Blocks: API response: {blocks}")
            return blocks
        print("Get_Duels_Blocks: No duels data found")
        return 0
    except KeyError:
        print("Get_Duels_Blocks: Error accessing duels data")
        return 0

async def get_duels_shots(uuid: str):
    """Get duels shots from Hypixel API"""
    uuid = uuid.strip("-")

    data = await get_user(uuid)
    
    try:
        if data and "player" in data and data["player"] and "stats" in data["player"] and "Duels" in data["player"]["stats"]:
            shots = data["player"]["stats"]["Duels"]["bow_shots"]
            print(f"Get_Duels_Shots: API response: {shots}")
            return shots
        print("Get_Duels_Shots: No duels data found")
        return 0
    except KeyError:
        print("Get_Duels_Shots: Error accessing duels data")
        return 0

async def get_duels_swings(uuid: str):
    """Get duels melee swings from Hypixel API"""
    uuid = uuid.strip("-")

    data = await get_user(uuid)
    
    try:
        if data and "player" in data and data["player"] and "stats" in data["player"] and "Duels" in data["player"]["stats"]:
            swings = data["player"]["stats"]["Duels"]["melee_swings"]
            print(f"Get_Duels_Swings: API response: {swings}")
            return swings
        print("Get_Duels_Swings: No duels data found")
        return 0
    except KeyError:
        print("Get_Duels_Swings: Error accessing duels data")
        return 0    

async def get_duels_ping(uuid: str):
    """Get duels ping-range from Hypixel API"""
    uuid = uuid.strip("-")

    data = await get_user(uuid)
    
    try:
        if data and "player" in data and data["player"] and "stats" in data["player"] and "Duels" in data["player"]["stats"]:
            ping = data["player"]["stats"]["Duels"]["ping_range"]
            print(f"Get_Duels_Ping: API response: {ping}")
            return ping
        print("Get_Duels_Ping: No duels data found")
        return "Unknown"
    except KeyError:
        print("Get_Duels_Ping: Error accessing duels data")
        return "Unknown"

async def get_duels_wins(uuid: str, gamemode: str):
    """
    Get duels wins from Hypixel API
    Gamemode:
        Options: overall, op_doubles, op_duel, op_full, uhc_doubles, sw_doubles, sumo_duel, potion_duel, sw_duel, sw_full, uhc_duel, uhc_full, classic_duel, bow_duel, blitz_duel, bowspleef_duel, combo_duel, mw_duel, mw_full, uhc_four, parkour_eight, boxing_duel, duel_arena, mw_doubles, bridge_duel, bridge_threes, bridge_four, bridge_doubles, bridge_3v3v3v3, bridge_2v2v2v2, bridge_wins
    """
    uuid = uuid.strip("-")

    data = await get_user(uuid)

    try:
        if not data or "player" not in data or not data["player"] or "stats" not in data["player"] or "Duels" not in data["player"]["stats"]:
            print("Get_Duels_Wins: No duels data found")
            return 0

        duels = data["player"]["stats"]["Duels"]
        
        if gamemode == "overall":
            wins = duels.get("wins", 0)
        elif gamemode == "op_full":
            wins = int(duels.get("op_duel_wins", 0)) + int(duels.get("op_doubles_wins", 0))
        elif gamemode == "sw_full":
            wins = int(duels.get("sw_duel_wins", 0)) + int(duels.get("sw_doubles_wins", 0))
        elif gamemode == "uhc_full":
            wins = int(duels.get("uhc_duel_wins", 0)) + int(duels.get("uhc_doubles_wins", 0)) + int(duels.get("uhc_four_wins", 0))
        elif gamemode == "mw_full":
            wins = int(duels.get("mw_duel_wins", 0)) + int(duels.get("mw_doubles_wins", 0))
        elif gamemode == "bridge":
            wins = int(duels.get("bridge_duel_wins", 0)) + int(duels.get("bridge_doubles_wins", 0)) + int(duels.get("bridge_threes_wins", 0)) + int(duels.get("bridge_3v3v3v3_wins", 0)) + int(duels.get("bridge_2v2v2v2_wins", 0)) + int(duels.get("bridge_fours_wins", 0))
        else:
            wins = duels.get(f"{gamemode}_wins", 0)
        
        print(f"{gamemode} Get_Duels_Wins: API response: {wins}")
        return wins

    except KeyError:
        print("Get_Duels_Wins: Error accessing duels data")
        return 0

async def get_duels_losses(uuid: str, gamemode: str):
    """
    Get duels losses from Hypixel API
    Gamemode:
        Options: overall, op_doubles, op_duel, op_full, uhc_doubles, sw_doubles, sumo_duel, potion_duel, sw_duel, sw_full, uhc_duel, uhc_full, classic_duel, bow_duel, blitz_duel, bowspleef_duel, combo_duel, mw_duel, mw_full, uhc_four, parkour_eight, boxing_duel, duel_arena, mw_doubles, bridge_duel, bridge_threes, bridge_four, bridge_doubles, bridge_3v3v3v3, bridge_2v2v2v2, bridge_losses
    """
    uuid = uuid.strip("-")

    data = await get_user(uuid)

    try:
        if not data or "player" not in data or not data["player"] or "stats" not in data["player"] or "Duels" not in data["player"]["stats"]:
            print("Get_Duels_Losses: No duels data found")
            return 0

        duels = data["player"]["stats"]["Duels"]
        
        if gamemode == "overall":
            losses = duels.get("losses", 0)
        elif gamemode == "op_full":
            losses = int(duels.get("op_duel_losses", 0)) + int(duels.get("op_doubles_losses", 0))
        elif gamemode == "sw_full":
            losses = int(duels.get("sw_duel_losses", 0)) + int(duels.get("sw_doubles_losses", 0))
        elif gamemode == "uhc_full":
            losses = int(duels.get("uhc_duel_losses", 0)) + int(duels.get("uhc_doubles_losses", 0)) + int(duels.get("uhc_four_losses", 0))
        elif gamemode == "mw_full":
            losses = int(duels.get("mw_duel_losses", 0)) + int(duels.get("mw_doubles_losses", 0))
        elif gamemode == "bridge":
            losses = int(duels.get("bridge_duel_losses", 0)) + int(duels.get("bridge_doubles_losses", 0)) + int(duels.get("bridge_threes_losses", 0)) + int(duels.get("bridge_3v3v3v3_losses", 0)) + int(duels.get("bridge_2v2v2v2_losses", 0)) + int(duels.get("bridge_fours_losses", 0))
        else:
            losses = duels.get(f"{gamemode}_losses", 0)
        
        print(f"Get_Duels_Losses: API response: {losses}")
        return losses

    except KeyError:
        print("Get_Duels_Losses: Error accessing duels data")
        return 0

async def get_duels_kills(uuid: str, gamemode: str):
    """
    Get duels kills from Hypixel API
    Gamemode:
        Options: overall, op_doubles, op_duel, op_full, uhc_doubles, sw_doubles, bridge_duel_bridge, bridge_threes_bridge, bridge_four_bridge, bridge_doubles_bridge, bridge_3v3v3v3_bridge, bridge_2v2v2v2_bridge, bridge_kills, sumo_duel, sw_full, sw_duel, classic_duel, bow_duel, uhc_duel, uhc_full, mw_duel, mw_full, blitz_duel, potion_duel, combo_duel, uhc_four, boxing_duel, duel_arena, capture_threes_bridge, mw_doubles 
    """
    uuid = uuid.strip("-")

    data = await get_user(uuid)

    try:
        if gamemode == "overall":
            kills = data["player"]["stats"]["Duels"]["kills"]
        elif gamemode == "op_full":
            kills = data["player"]["stats"]["Duels"]["op_duel_kills"] + data["player"]["stats"]["Duels"]["op_doubles_kills"]
        elif gamemode == "sw_full":
            kills = data["player"]["stats"]["Duels"]["sw_duel_kills"] + data["player"]["stats"]["Duels"]["sw_doubles_kills"]
        elif gamemode == "uhc_full":
            kills = data["player"]["stats"]["Duels"]["uhc_duel_kills"] + data["player"]["stats"]["Duels"]["uhc_doubles_kills"] + data["player"]["stats"]["Duels"]["uhc_four_kills"]
        elif gamemode == "mw_full":
            kills = data["player"]["stats"]["Duels"]["mw_duel_kills"] + data["player"]["stats"]["Duels"]["mw_doubles_kills"]
        
        else:
            kills = data["player"]["stats"]["Duels"][f"{gamemode}_kills"]
    
        print(f"Get_Duels_Kills: API response: {kills}")
        return kills
    except KeyError:
        print("Get_Duels_Kills: Error accessing duels data")
        return 0

async def get_duels_deaths(uuid: str, gamemode: str):
    """
    Get duels deaths from Hypixel API
    Gamemode:
        Options: overall, op_doubles, op_duel, op_full, uhc_doubles, sw_doubles, bridge_duel_bridge, bridge_threes_bridge, bridge_four_bridge, bridge_doubles_bridge, bridge_3v3v3v3_bridge, bridge_2v2v2v2_bridge, bridge_deaths, sumo_duel, sw_full, sw_duel, classic_duel, bow_duel, uhc_duel, uhc_full, mw_duel, mw_full, blitz_duel, potion_duel, combo_duel, uhc_four, boxing_duel, duel_arena, capture_threes_bridge, mw_doubles 
    """
    uuid = uuid.strip("-")

    data = await get_user(uuid)

    try:
        if gamemode == "overall":
            deaths = data["player"]["stats"]["Duels"]["deaths"]
        elif gamemode == "op_full":
            deaths = data["player"]["stats"]["Duels"]["op_duel_deaths"] + data["player"]["stats"]["Duels"]["op_doubles_deaths"]
        elif gamemode == "sw_full":
            deaths = data["player"]["stats"]["Duels"]["sw_duel_deaths"] + data["player"]["stats"]["Duels"]["sw_doubles_deaths"]
        elif gamemode == "uhc_full":
            deaths = data["player"]["stats"]["Duels"]["uhc_duel_deaths"] + data["player"]["stats"]["Duels"]["uhc_doubles_deaths"] + data["player"]["stats"]["Duels"]["uhc_four_deaths"]
        elif gamemode == "mw_full":
            deaths = data["player"]["stats"]["Duels"]["mw_duel_deaths"] + data["player"]["stats"]["Duels"]["mw_doubles_deaths"]
        
        else:
            deaths = data["player"]["stats"]["Duels"][f"{gamemode}_deaths"]
    
        print(f"Get_Duels_deaths: API response: {deaths}")
        return deaths
    except KeyError:
        print("Get_Duels_deaths: Error accessing duels data")
        return 0

async def get_duels_kdr(uuid: str, gamemode: str):
    """
    Get duels kdr from Hypixel API
    Gamemode:
        Options: same as get_duels_kills
    """
    try:
        kills =  await get_duels_kills(uuid, gamemode)
        deaths = await get_duels_deaths(uuid, gamemode)
        return round(kills / deaths, 2) if deaths != 0 else kills
    except Exception as e:
        print(f"Get_Duels_KDR: Error: {e}")
        return 0

async def get_duels_wlr(uuid: str, gamemode: str):
    """
    Get duels wlr from Hypixel API
    Gamemode:
        Options: same as get_duels_kills
    """
    try:
        wins =  await get_duels_wins(uuid, gamemode)
        losses = await get_duels_losses(uuid, gamemode)
        return round(wins / losses, 2) if losses != 0 else wins
    except Exception as e:
        print(f"Get_Duels_WLR: Error: {e}")
        return 0

async def get_duels_current_winstreak(uuid: str, gamemode: str):
    """
    Get duels current winstreak from Hypixel API
    Gamemode:
        Options: same as get_duels_kills
    """
    uuid = uuid.strip("-")

    data = await get_user(uuid)

    try:
        if not data or "player" not in data or not data["player"] or "stats" not in data["player"] or "Duels" not in data["player"]["stats"]:
            print("Get_Duels_Current_Winstreak: No duels data found")
            return 0

        duels = data["player"]["stats"]["Duels"]

        if gamemode == "overall":
            ws = duels.get("current_winstreak", 0)
        elif gamemode == "op_full":
            solo = duels.get("current_winstreak_mode_op_duel", 0)
            duo = duels.get("current_winstreak_mode_op_doubles", 0)
            ws = max(solo, duo)
        elif gamemode == "sw_full":
            solo = duels.get("current_winstreak_mode_sw_duel", 0)
            duo = duels.get("current_winstreak_mode_sw_doubles", 0)
            ws = max(solo, duo)
        elif gamemode == "uhc_full":
            solo = duels.get("current_winstreak_mode_uhc_duel", 0)
            duo = duels.get("current_winstreak_mode_uhc_doubles", 0)
            four = duels.get("current_winstreak_mode_uhc_four", 0)
            ws = max(solo, duo, four)
        elif gamemode == "mw_full":
            solo = duels.get("current_winstreak_mode_mw_duel", 0)
            duo = duels.get("current_winstreak_mode_mw_doubles", 0)
            ws = max(solo, duo)
        elif gamemode == "bridge" or gamemode == "bridge_full":
            # Get all bridge mode winstreaks
            bridge = duels.get("current_winstreak_mode_bridge_duel", 0)
            doubles = duels.get("current_winstreak_mode_bridge_doubles", 0)
            threes = duels.get("current_winstreak_mode_bridge_threes", 0)
            four = duels.get("current_winstreak_mode_bridge_four", 0)
            threev3v3v3 = duels.get("current_winstreak_mode_bridge_3v3v3v3", 0)
            twov2v2v2 = duels.get("current_winstreak_mode_bridge_2v2v2v2", 0)
            ws = max(bridge, doubles, threes, four, threev3v3v3, twov2v2v2)
        else:
            ws = duels.get(f"current_winstreak_mode_{gamemode}", 0)
        
        print(f"Get_Duels_Current_Winstreak: API response for {gamemode}: {ws}")
        return ws

    except Exception as e:
        print(f"Get_Duels_Current_Winstreak: Error accessing duels data for {gamemode}: {str(e)}")
        return 0

async def get_duels_best_winstreak(uuid: str, gamemode: str):
    """
    Get duels best winstreak from Hypixel API
    Gamemode:
        Options: same as get_duels_current_winstreak
    """
    uuid = uuid.strip("-")

    data = await get_user(uuid)
    
    try:
        if gamemode == "overall":
            ws = data["player"]["stats"]["Duels"]["best_overall_winstreak"]
        elif gamemode == "op_full":
            solo = data["player"]["stats"]["Duels"]["best_winstreak_mode_op_duel"]
            duo = data["player"]["stats"]["Duels"]["best_winstreak_mode_op_doubles"]
            ws = max(solo, duo)
        elif gamemode == "sw_full":
            solo = data["player"]["stats"]["Duels"]["best_winstreak_mode_sw_duel"]
            duo = data["player"]["stats"]["Duels"]["best_winstreak_mode_sw_doubles"]
            ws = max(solo, duo)
        elif gamemode == "uhc_full":
            solo = data["player"]["stats"]["Duels"]["best_winstreak_mode_uhc_duel"]
            duo = data["player"]["stats"]["Duels"]["best_winstreak_mode_uhc_doubles"]
            four = data["player"]["stats"]["Duels"]["best_winstreak_mode_uhc_four"]
            ws = max(solo, duo, four)
        elif gamemode == "mw_full":
            solo = data["player"]["stats"]["Duels"]["best_winstreak_mode_mw_duel"]
            duo = data["player"]["stats"]["Duels"]["best_winstreak_mode_mw_doubles"]
            ws = max(solo, duo)
        elif gamemode == "bridge_full" or gamemode == "bridge":
            bridge = data["player"]["stats"]["Duels"]["best_winstreak_mode_bridge_duel"]
            threes = data["player"]["stats"]["Duels"]["best_winstreak_mode_bridge_threes"]
            four = data["player"]["stats"]["Duels"]["best_winstreak_mode_bridge_four"]
            doubles = data["player"]["stats"]["Duels"]["best_winstreak_mode_bridge_doubles"]
            threev3v3v3 = data["player"]["stats"]["Duels"]["best_winstreak_mode_bridge_3v3v3v3"]
            twov2v2v2 = data["player"]["stats"]["Duels"]["best_winstreak_mode_bridge_2v2v2v2"]
            ctf = data["player"]["stats"]["Duels"]["best_winstreak_mode_capture_threes"]
            ws = max(bridge, threes, four, doubles, twov2v2v2, threev3v3v3, ctf)
        else:
            ws = data["player"]["stats"]["Duels"][f"best_winstreak_mode_{gamemode}"]
        
        print(f"Get_Duels_Best_Winstreak: API response: {ws}")
        return ws
    
    except KeyError:
        print(f"Get_Duels_Best_Winstreak: Error accessing duels data: {gamemode} not found")
        return 0

async def get_duels_title(uuid: str, gamemode: str):
    """Get the highest title and prestige for a player in a specific duels gamemode.
    
    Args:
        uuid (str): Player UUID
        gamemode (str): Duels gamemode (overall, blitz, bow, tnt_games, boxing, bridge, 
                       classic, combo, mega_walls, no_debuff, op, parkour, skywars, sumo, uhc)
    
    Returns:
        tuple: (prestige in roman numerals, formatted title string, hex color code, is_bold)
    """
    TITLE_DATA = [
        ("rookie", "#808080", False),      # Gray
        ("iron", "#FFFFFF", False),        # White
        ("gold", "#FFFF00", False),        # Yellow
        ("diamond", "#00A0A0", False),     # Dark Teal
        ("master", "#00FF00", False),      # Green
        ("legend", "#FF0000", True),       # Bold Red
        ("grandmaster", "#FFD700", True),  # Bold Light Yellow
        ("godlike", "#FF00FF", True),      # Bold Purple
        ("celestial", "#00FFFF", True),    # Bold Light Teal
        ("divine", "#FF6B6B", False),      # Light Red
        ("ascended", "#FF6B6B", True)      # Bold Light Red
    ]
    
    uuid = uuid.strip("-")
    
    try:
        raw_data = await get_user(uuid)
        data = raw_data["player"]["stats"]["Duels"]
        
        prefix = "all_modes" if gamemode.lower() == "overall" else gamemode.lower()
        
        # Find highest achieved title
        current_title = None
        current_color = "#808080"
        is_bold = False
        for title, color, bold in TITLE_DATA:
            key = f"{prefix}_{title}_title_prestige"
            if key not in data or data[key] < 5:
                current_title = title
                current_color = color
                is_bold = bold
                break
            if title == "ascended":  # Last title in hierarchy
                current_title = "ascended"
                current_color = color
                is_bold = bold
        
        if not current_title:
            current_title = "rookie"
            current_color = "#808080"
            is_bold = False
            
        # Get prestige for current title
        prestige_key = f"{prefix}_{current_title}_title_prestige"
        prestige = data.get(prestige_key, 0)
        
        if current_title == "rookie" and prestige == 1:
            prestige = 0
            current_title = ""
            current_color = "#808080"
            is_bold = False
            
            return prestige, current_title, current_color, is_bold
            
        
        # Format the title string
        title_str = current_title.title()
        if gamemode.lower() != "overall":
            title_str = f"{prettify(gamemode)} {title_str}"
        
        return to_roman_numeral(int(prestige)), title_str, current_color, is_bold

    except Exception as e:
        print(f"Get_Duels_Title: Error retrieving title - {e}")
        return "None", "Rookie", "#808080", False

# Bedwars Functions

class BedWarsXP:
    EASY_LEVELS = 4
    EASY_LEVELS_XP = [500, 1000, 2000, 3500]
    EASY_LEVELS_XP_TOTAL = sum(EASY_LEVELS_XP)
    XP_PER_LEVEL = 5000
    XP_PER_PRESTIGE = 96 * XP_PER_LEVEL + EASY_LEVELS_XP_TOTAL
    LEVELS_PER_PRESTIGE = 100
    HIGHEST_PRESTIGE = 100000000 

    @classmethod
    def calculate_star(cls, exp):
        """
        Main method to calculate the BedWars star (level as a float rounded to 3 decimals)
        and prestige for a given XP.
        """
        level = cls.get_level_for_exp(exp)
        prestige = cls.get_prestige_for_exp(exp)
        return level, prestige

    @classmethod
    def get_prestige_for_exp(cls, exp):
        level = cls.get_level_for_exp(exp)
        return cls.get_prestige_for_level(level)

    @classmethod
    def get_prestige_for_level(cls, level):
        prestige = level // cls.LEVELS_PER_PRESTIGE
        return min(prestige, cls.HIGHEST_PRESTIGE)

    @classmethod
    def get_level_for_exp(cls, exp):
        prestiges = exp // cls.XP_PER_PRESTIGE
        level = prestiges * cls.LEVELS_PER_PRESTIGE

        exp_without_prestiges = exp % cls.XP_PER_PRESTIGE

        for i in range(1, cls.EASY_LEVELS + 1):
            exp_for_easy_level = cls.get_exp_for_level(i)
            if exp_without_prestiges < exp_for_easy_level:
                break
            level += 1
            exp_without_prestiges -= exp_for_easy_level

        level += exp_without_prestiges / cls.XP_PER_LEVEL
        return round(level, 3) 

    @classmethod
    def get_exp_for_level(cls, level):
        if level == 0:
            return 0

        respected_level = cls.get_level_respecting_prestige(level)
        if respected_level <= cls.EASY_LEVELS:
            return cls.EASY_LEVELS_XP[respected_level - 1]
        return cls.XP_PER_LEVEL

    @classmethod
    def get_level_respecting_prestige(cls, level):
        if level > cls.HIGHEST_PRESTIGE * cls.LEVELS_PER_PRESTIGE:
            return level - cls.HIGHEST_PRESTIGE * cls.LEVELS_PER_PRESTIGE
        return level % cls.LEVELS_PER_PRESTIGE

async def get_map(map: str):
    headers = {'Api-Key': POLSU_TOKEN}
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.polsu.xyz/polsu/bedwars/map?map={map}", headers=headers) as response:
            data = await response.json()
            return data

def get_star(exp):
    level, _ = BedWarsXP.calculate_star(exp)
    return level

def get_prestige(exp):
    _, prestige = BedWarsXP.calculate_star(exp)
    return prestige

async def fetch_xp(username):
    uuid = str(await get_uuid(username)).strip("-")
    data = await get_user(uuid)
    if not data or "player" not in data:
        return None

    try:
        xp = data["player"]["stats"]["BedWars"]["Experience"]
        print(f"Fetch_Xp: API response: {xp}")  # Debug print
        return xp
    except KeyError:
        return None
