# Hypickle Discord Bot

A powerful Discord bot for viewing Hypixel statistics, with a special focus on Duels and Bedwars game modes.

## Features

- **Duels Statistics**
  - Comprehensive stats for all game modes
  - Kills, deaths, wins, losses tracking
  - Current and best winstreak monitoring
  - Title and prestige display
  - Support for specialized modes (Bridge, UHC, SkyWars, etc.)

- **Bedwars Features**
  - Map information and previews
  - Experience and level tracking
  - Star and prestige calculation

## Commands

### Duels Commands
- `/duels [username] (gamemode)` - View Duels statistics

### Bedwars Commands
- `/bedwars-map [map]` - Get information about a Bedwars map
- Additional Bedwars commands coming soon!

## Technical Details

### APIs Used
- [Hypixel API](https://api.hypixel.net/) - Core game statistics (API key required) API KEY WILL RESET EVERY 24 HOURS
- [Polsu API](https://api.polsu.xyz/) - Map information and additional data (API key required)
- [Mojang API](https://api.mojang.com/) - Player UUID and profile information

### Dependencies
- discord.py - Discord bot framework
- aiohttp - Asynchronous HTTP requests
- python-dotenv - Environment variable management

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `credentials.py` file with your API tokens:
   ```python
    DISCORD = "discord-token"
    POLSU = "polsu-key"
    HYPIXEL = "hypixel-key"
   ```
4. Run the bot:
   ```bash
   python main.py
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to [Hypixel](https://hypixel.net) for providing the API
- Thanks to [Polsu](https://polsu.xyz) for the additional API services