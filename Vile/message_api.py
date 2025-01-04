import discord
from discord.ext import commands
from typing import List, Optional, Union, Dict
import asyncio
import json
import re

class MessageAPI:
    def __init__(self, bot):
        self.bot = bot
        self._snipe_messages = {}
        self._edit_snipe_messages = {}
        self._afk_users = {}
        self._spam_settings = {}
        self._autoresponders = {}
        
    async def handle_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
            
        await self._check_afk_mentions(message)
        await self._handle_autoresponders(message)
        await self._check_spam(message)
        
    async def _check_afk_mentions(self, message: discord.Message) -> None:
        if not message.mentions:
            return
            
        for mention in message.mentions:
            if str(mention.id) in self._afk_users:
                afk_data = self._afk_users[str(mention.id)]
                embed = discord.Embed(
                    description=f"{mention.name} is AFK: {afk_data['reason']}",
                    color=discord.Color.blue()
                )
                await message.channel.send(embed=embed)
                
    async def _handle_autoresponders(self, message: discord.Message) -> None:
        if not message.guild:
            return
            
        guild_id = str(message.guild.id)
        if guild_id not in self._autoresponders:
            return
            
        content = message.content.lower()
        for trigger, response in self._autoresponders[guild_id].items():
            if trigger.lower() in content:
                await message.channel.send(response)
                
    async def _check_spam(self, message: discord.Message) -> None:
        if not message.guild:
            return
            
        guild_id = str(message.guild.id)
        if guild_id not in self._spam_settings:
            return
            
        settings = self._spam_settings[guild_id]
        if not settings.get('enabled', False):
            return
            

        
    async def snipe_message(self, message: discord.Message) -> None:
        channel_id = str(message.channel.id)
        self._snipe_messages[channel_id] = {
            'content': message.content,
            'author': message.author,
            'attachments': [att.url for att in message.attachments],
            'timestamp': message.created_at
        }
        
    async def edit_snipe_message(self, before: discord.Message, after: discord.Message) -> None:
        channel_id = str(before.channel.id)
        self._edit_snipe_messages[channel_id] = {
            'before': before.content,
            'after': after.content,
            'author': before.author,
            'timestamp': before.created_at
        }
        
    def get_snipe(self, channel_id: str) -> Optional[Dict]:
        return self._snipe_messages.get(channel_id)
        
    def get_edit_snipe(self, channel_id: str) -> Optional[Dict]:
        return self._edit_snipe_messages.get(channel_id)
        
    async def set_afk(self, user_id: str, reason: str) -> None:
        self._afk_users[user_id] = {
            'reason': reason,
            'timestamp': discord.utils.utcnow()
        }
        
    def remove_afk(self, user_id: str) -> None:
        self._afk_users.pop(user_id, None)
        
    def is_afk(self, user_id: str) -> bool:
        return user_id in self._afk_users
        
    async def add_autoresponder(self, guild_id: str, trigger: str, response: str) -> None:
        if guild_id not in self._autoresponders:
            self._autoresponders[guild_id] = {}
        self._autoresponders[guild_id][trigger] = response
        
    def remove_autoresponder(self, guild_id: str, trigger: str) -> bool:
        if guild_id in self._autoresponders:
            return self._autoresponders[guild_id].pop(trigger, None) is not None
        return False
        
    def get_autoresponders(self, guild_id: str) -> Dict:
        return self._autoresponders.get(guild_id, {})
        
    async def set_spam_settings(self, guild_id: str, settings: Dict) -> None:
        self._spam_settings[guild_id] = settings
        
    def get_spam_settings(self, guild_id: str) -> Dict:
        return self._spam_settings.get(guild_id, {})
