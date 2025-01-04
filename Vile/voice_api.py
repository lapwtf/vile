import discord
from discord.ext import commands
from typing import List, Optional, Union, Dict
import asyncio
import json

class VoiceAPI:
    def __init__(self, bot):
        self.bot = bot
        self._vc_data = {}
        self._temp_channels = set()
        self._voice_roles = {}
        
    async def setup_voice_role(self, guild_id: str, voice_id: int, role_id: int) -> None:
        if guild_id not in self._voice_roles:
            self._voice_roles[guild_id] = {}
        self._voice_roles[guild_id][voice_id] = role_id
        
    def remove_voice_role(self, guild_id: str, voice_id: int) -> bool:
        if guild_id in self._voice_roles:
            return self._voice_roles[guild_id].pop(voice_id, None) is not None
        return False
        
    def get_voice_role(self, guild_id: str, voice_id: int) -> Optional[int]:
        return self._voice_roles.get(guild_id, {}).get(voice_id)
        
    async def handle_voice_join(self, member: discord.Member, channel: discord.VoiceChannel) -> None:
        guild_id = str(member.guild.id)
        
        role_id = self.get_voice_role(guild_id, channel.id)
        if role_id:
            role = member.guild.get_role(role_id)
            if role:
                try:
                    await member.add_roles(role)
                except:
                    pass
                    
        if channel.id in self._vc_data.get(guild_id, {}):
            settings = self._vc_data[guild_id][channel.id]
            if settings.get('auto_create', False):
                await self.create_temp_channel(member, settings)
                
    async def handle_voice_leave(self, member: discord.Member, channel: discord.VoiceChannel) -> None:
        guild_id = str(member.guild.id)
        
        role_id = self.get_voice_role(guild_id, channel.id)
        if role_id:
            role = member.guild.get_role(role_id)
            if role:
                try:
                    await member.remove_roles(role)
                except:
                    pass
                    
        if channel.id in self._temp_channels and not channel.members:
            try:
                await channel.delete()
                self._temp_channels.remove(channel.id)
            except:
                pass
                
    async def create_temp_channel(self, member: discord.Member, settings: Dict) -> Optional[discord.VoiceChannel]:
        try:
            channel_name = settings.get('name_format', '🔊 {user}').format(
                user=member.display_name,
                count=len(member.guild.voice_channels) + 1
            )
            
            channel = await member.guild.create_voice_channel(
                name=channel_name,
                category=member.voice.channel.category,
                bitrate=settings.get('bitrate', 64000),
                user_limit=settings.get('user_limit', 0)
            )
            
            await channel.set_permissions(member, 
                manage_channels=True,
                manage_permissions=True,
                connect=True,
                speak=True
            )
            
            await member.move_to(channel)
            
            self._temp_channels.add(channel.id)
            return channel
        except:
            return None
            
    async def setup_voice_channel(self, guild_id: str, channel_id: int, settings: Dict) -> None:
        if guild_id not in self._vc_data:
            self._vc_data[guild_id] = {}
        self._vc_data[guild_id][channel_id] = settings
        
    def remove_voice_channel(self, guild_id: str, channel_id: int) -> bool:
        if guild_id in self._vc_data:
            return self._vc_data[guild_id].pop(channel_id, None) is not None
        return False
        
    def get_voice_settings(self, guild_id: str, channel_id: int) -> Dict:
        return self._vc_data.get(guild_id, {}).get(channel_id, {})
        
    async def move_member(self, member: discord.Member, channel: discord.VoiceChannel) -> bool:
        try:
            await member.move_to(channel)
            return True
        except:
            return False
            
    async def disconnect_member(self, member: discord.Member) -> bool:
        try:
            await member.move_to(None)
            return True
        except:
            return False
