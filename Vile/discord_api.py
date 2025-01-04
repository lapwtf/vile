import discord
from discord.ext import commands
import aiohttp
import io
from PIL import Image
import asyncio
from typing import Union, List, Optional
import json
import datetime

class DiscordAPI:
    def __init__(self, bot):
        self.bot = bot
        self._session = None
        
    @property
    def session(self):
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session
        
    async def close(self):
        if self._session:
            await self._session.close()
            
    async def fetch_user_data(self, user_id: int) -> Optional[dict]:
        try:
            user = await self.bot.fetch_user(user_id)
            return {
                'id': str(user.id),
                'name': user.name,
                'discriminator': user.discriminator,
                'avatar_url': str(user.avatar.url) if user.avatar else None,
                'banner_url': str(user.banner.url) if user.banner else None,
                'bot': user.bot,
                'created_at': user.created_at.isoformat()
            }
        except:
            return None

    async def fetch_member_data(self, guild_id: int, user_id: int) -> Optional[dict]:
        try:
            guild = self.bot.get_guild(guild_id)
            if not guild:
                return None
            member = await guild.fetch_member(user_id)
            return {
                'id': str(member.id),
                'name': member.name,
                'nick': member.nick,
                'roles': [str(role.id) for role in member.roles],
                'joined_at': member.joined_at.isoformat() if member.joined_at else None,
                'premium_since': member.premium_since.isoformat() if member.premium_since else None
            }
        except:
            return None

    async def create_role(self, guild: discord.Guild, **kwargs) -> Optional[discord.Role]:
        try:
            return await guild.create_role(**kwargs)
        except:
            return None

    async def edit_role(self, role: discord.Role, **kwargs) -> bool:
        try:
            await role.edit(**kwargs)
            return True
        except:
            return False

    async def bulk_delete_messages(self, channel: discord.TextChannel, messages: List[discord.Message]) -> bool:
        try:
            await channel.delete_messages(messages)
            return True
        except:
            return False

    async def create_emoji(self, guild: discord.Guild, name: str, image_data: bytes) -> Optional[discord.Emoji]:
        try:
            return await guild.create_custom_emoji(name=name, image=image_data)
        except:
            return None

    async def fetch_emoji(self, url: str) -> Optional[bytes]:
        async with self.session.get(url) as response:
            if response.status == 200:
                return await response.read()
            return None

    async def move_member(self, member: discord.Member, channel: discord.VoiceChannel) -> bool:
        try:
            await member.move_to(channel)
            return True
        except:
            return False

    async def get_audit_logs(self, guild: discord.Guild, limit: int = 100, action: discord.AuditLogAction = None) -> List[discord.AuditLogEntry]:
        try:
            entries = []
            async for entry in guild.audit_logs(limit=limit, action=action):
                entries.append(entry)
            return entries
        except:
            return []

    async def get_invites(self, guild: discord.Guild) -> List[discord.Invite]:
        try:
            return await guild.invites()
        except:
            return []

    async def create_invite(self, channel: discord.TextChannel, **kwargs) -> Optional[discord.Invite]:
        try:
            return await channel.create_invite(**kwargs)
        except:
            return None

    async def get_bans(self, guild: discord.Guild) -> List[discord.User]:
        try:
            bans = await guild.bans()
            return [ban.user for ban in bans]
        except:
            return []

    async def get_webhooks(self, channel: discord.TextChannel) -> List[discord.Webhook]:
        try:
            return await channel.webhooks()
        except:
            return []

    async def create_webhook(self, channel: discord.TextChannel, name: str) -> Optional[discord.Webhook]:
        try:
            return await channel.create_webhook(name=name)
        except:
            return None
