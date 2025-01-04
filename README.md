# Lapbot - Advanced Discord Bot

A powerful, feature-rich Discord bot built with discord.py, offering comprehensive moderation, utility, and entertainment features.

## Features

### Moderation System
- Advanced user management (ban, kick, mute, warn)
- Temporary punishments with automatic expiration
- Bulk message deletion
- Channel lockdown capabilities
- Anti-spam protection

### Role Management
- Reaction roles system
- Auto-roles for new members
- Special booster roles
- Role persistence for returning members
- Voice channel roles

### Voice Features
- Dynamic voice channel creation
- Voice channel management
- User movement controls
- Temporary voice channels

### Message Management
- Message snipe system
- Edit snipe functionality
- AFK system
- Custom autoresponders
- Spam protection

### Roblox Integration
- User profile lookup
- Last online status
- Friend list viewing
- Badge display
- Group information

### Utility Features
- User information display
- Server statistics
- Avatar and banner commands
- Emoji management
- Urban Dictionary lookup

## Project Structure

```
Lapbot/
├── api/                    # API integrations
│   ├── discord_api.py     # Discord API wrapper
│   ├── roblox.py          # Roblox API integration
│   ├── message_api.py     # Message handling
│   ├── moderation_api.py  # Moderation tools
│   ├── role_api.py        # Role management
│   └── voice_api.py       # Voice features
├── cogs/                  # Bot commands and features
├── utils/                 # Utility functions
└── vile.py               # Main bot file

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/lapbot.git
cd lapbot
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Configure your bot:
- Create a `config.py` file with your bot token and settings
- Set up necessary permissions in your Discord server

4. Run the bot:
```bash
python vile.py
```

## API Documentation

### Discord API
```python
from api.discord_api import DiscordAPI

discord_api = DiscordAPI(bot)
await discord_api.fetch_user_data(user_id)
```

### Roblox API
```python
from api.roblox import RobloxAPI

roblox_api = RobloxAPI()
await roblox_api.get_user_profile(user_id)
```

### Message API
```python
from api.message_api import MessageAPI

message_api = MessageAPI(bot)
await message_api.handle_message(message)
```

### Moderation API
```python
from api.moderation_api import ModerationAPI

mod_api = ModerationAPI(bot)
await mod_api.mute_member(member, duration)
```

### Role API
```python
from api.role_api import RoleAPI

role_api = RoleAPI(bot)
await role_api.setup_reaction_role(message_id, emoji, role_id)
```

### Voice API
```python
from api.voice_api import VoiceAPI

voice_api = VoiceAPI(bot)
await voice_api.handle_voice_join(member, channel)
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
