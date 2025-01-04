import discord
from discord.ext import commands
from typing import List, Optional, Union, Dict
import asyncio
import datetime

class ModerationAPI:
    def __init__(self, bot):
        self.bot = bot
        self._muted_roles = {}
        self._temp_bans = {}
        self._temp_mutes = {}
        self._warns = {}
        self._lockdowns = set()
        
    async def create_mute_role(self, guild: discord.Guild) -> Optional[discord.Role]:
        try:
            mute_role = await guild.create_role(
                name="Muted",
                reason="Role for muted users"
            )
            
            for channel in guild.channels:
                if isinstance(channel, (discord.TextChannel, discord.VoiceChannel)):
                    await channel.set_permissions(mute_role, 
                        speak=False, 
                        send_messages=False,
                        add_reactions=False
                    )
                    
            self._muted_roles[guild.id] = mute_role.id
            return mute_role
        except:
            return None
            
    async def get_mute_role(self, guild: discord.Guild) -> Optional[discord.Role]:
        role_id = self._muted_roles.get(guild.id)
        if role_id:
            return guild.get_role(role_id)
            
        role = discord.utils.get(guild.roles, name="Muted")
        if role:
            self._muted_roles[guild.id] = role.id
            return role
            
        return await self.create_mute_role(guild)
        
    async def mute_member(self, member: discord.Member, duration: int = None, reason: str = None) -> bool:
        try:
            mute_role = await self.get_mute_role(member.guild)
            if not mute_role:
                return False
                
            await member.add_roles(mute_role, reason=reason)
            
            if duration:
                self._temp_mutes[member.id] = {
                    'end_time': discord.utils.utcnow() + datetime.timedelta(seconds=duration),
                    'role_id': mute_role.id
                }
                
            return True
        except:
            return False
            
    async def unmute_member(self, member: discord.Member, reason: str = None) -> bool:
        try:
            mute_role = await self.get_mute_role(member.guild)
            if not mute_role:
                return False
                
            await member.remove_roles(mute_role, reason=reason)
            self._temp_mutes.pop(member.id, None)
            return True
        except:
            return False
            
    async def warn_member(self, member: discord.Member, reason: str) -> int:
        guild_id = str(member.guild.id)
        user_id = str(member.id)
        
        if guild_id not in self._warns:
            self._warns[guild_id] = {}
            
        if user_id not in self._warns[guild_id]:
            self._warns[guild_id][user_id] = []
            
        warn_data = {
            'reason': reason,
            'timestamp': discord.utils.utcnow().isoformat(),
            'moderator_id': self.bot.user.id
        }
        
        self._warns[guild_id][user_id].append(warn_data)
        return len(self._warns[guild_id][user_id])
        
    def get_warns(self, guild_id: str, user_id: str) -> List[Dict]:
        return self._warns.get(guild_id, {}).get(user_id, [])
        
    def clear_warns(self, guild_id: str, user_id: str) -> bool:
        if guild_id in self._warns and user_id in self._warns[guild_id]:
            self._warns[guild_id][user_id] = []
            return True
        return False
        
    async def ban_member(self, member: discord.Member, duration: int = None, reason: str = None, delete_message_days: int = 0) -> bool:
        try:
            await member.ban(reason=reason, delete_message_days=delete_message_days)
            
            if duration:
                self._temp_bans[member.id] = {
                    'guild_id': member.guild.id,
                    'end_time': discord.utils.utcnow() + datetime.timedelta(seconds=duration)
                }
                
            return True
        except:
            return False
            
    async def unban_member(self, guild: discord.Guild, user_id: int, reason: str = None) -> bool:
        try:
            user = await self.bot.fetch_user(user_id)
            await guild.unban(user, reason=reason)
            self._temp_bans.pop(user_id, None)
            return True
        except:
            return False
            
    async def check_temp_punishments(self) -> None:
        current_time = discord.utils.utcnow()
        
        for user_id, mute_data in list(self._temp_mutes.items()):
            if current_time >= mute_data['end_time']:
                guild = self.bot.get_guild(mute_data['guild_id'])
                if guild:
                    member = guild.get_member(user_id)
                    if member:
                        await self.unmute_member(member, reason="Temporary mute expired")
                        
        for user_id, ban_data in list(self._temp_bans.items()):
            if current_time >= ban_data['end_time']:
                guild = self.bot.get_guild(ban_data['guild_id'])
                if guild:
                    await self.unban_member(guild, user_id, reason="Temporary ban expired")
                    
    async def lockdown_channel(self, channel: discord.TextChannel, reason: str = None) -> bool:
        try:
            await channel.set_permissions(channel.guild.default_role, send_messages=False, reason=reason)
            self._lockdowns.add(channel.id)
            return True
        except:
            return False
            
    async def unlock_channel(self, channel: discord.TextChannel, reason: str = None) -> bool:
        try:
            await channel.set_permissions(channel.guild.default_role, send_messages=None, reason=reason)
            self._lockdowns.discard(channel.id)
            return True
        except:
            return False
            
    def is_channel_locked(self, channel_id: int) -> bool:
        return channel_id in self._lockdowns
