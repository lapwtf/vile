import discord
from discord.ext import commands
from typing import List, Optional, Union, Dict
import asyncio
import json
import re

class RoleAPI:
    def __init__(self, bot):
        self.bot = bot
        self._reaction_roles = {}
        self._autoroles = {}
        self._booster_roles = {}
        self._left_roles = {}
        
    async def setup_reaction_role(self, message_id: str, emoji: str, role_id: int) -> None:
        if message_id not in self._reaction_roles:
            self._reaction_roles[message_id] = {}
        self._reaction_roles[message_id][emoji] = role_id
        
    def remove_reaction_role(self, message_id: str, emoji: str) -> bool:
        if message_id in self._reaction_roles:
            return self._reaction_roles[message_id].pop(emoji, None) is not None
        return False
        
    def get_reaction_role(self, message_id: str, emoji: str) -> Optional[int]:
        return self._reaction_roles.get(message_id, {}).get(emoji)
        
    def get_all_reaction_roles(self, message_id: str) -> Dict[str, int]:
        return self._reaction_roles.get(message_id, {})
        
    async def handle_reaction_add(self, member: discord.Member, message_id: str, emoji: str) -> None:
        role_id = self.get_reaction_role(message_id, emoji)
        if role_id:
            role = member.guild.get_role(role_id)
            if role:
                try:
                    await member.add_roles(role)
                except:
                    pass
                    
    async def handle_reaction_remove(self, member: discord.Member, message_id: str, emoji: str) -> None:
        role_id = self.get_reaction_role(message_id, emoji)
        if role_id:
            role = member.guild.get_role(role_id)
            if role:
                try:
                    await member.remove_roles(role)
                except:
                    pass
                    
    async def setup_autorole(self, guild_id: str, role_id: int) -> None:
        if guild_id not in self._autoroles:
            self._autoroles[guild_id] = set()
        self._autoroles[guild_id].add(role_id)
        
    def remove_autorole(self, guild_id: str, role_id: int) -> bool:
        if guild_id in self._autoroles:
            try:
                self._autoroles[guild_id].remove(role_id)
                return True
            except KeyError:
                pass
        return False
        
    def get_autoroles(self, guild_id: str) -> List[int]:
        return list(self._autoroles.get(guild_id, set()))
        
    async def handle_member_join(self, member: discord.Member) -> None:
        guild_id = str(member.guild.id)
        

        for role_id in self.get_autoroles(guild_id):
            role = member.guild.get_role(role_id)
            if role:
                try:
                    await member.add_roles(role)
                except:
                    pass
                    

        if guild_id in self._left_roles and str(member.id) in self._left_roles[guild_id]:
            for role_id in self._left_roles[guild_id][str(member.id)]:
                role = member.guild.get_role(role_id)
                if role:
                    try:
                        await member.add_roles(role)
                    except:
                        pass
            del self._left_roles[guild_id][str(member.id)]
            
    async def handle_member_remove(self, member: discord.Member) -> None:
        guild_id = str(member.guild.id)
        
        if guild_id not in self._left_roles:
            self._left_roles[guild_id] = {}
            
        self._left_roles[guild_id][str(member.id)] = [
            role.id for role in member.roles 
            if role.id != member.guild.id  
        ]
        
    async def setup_booster_role(self, guild_id: str, settings: Dict) -> None:
        self._booster_roles[guild_id] = settings
        
    def get_booster_settings(self, guild_id: str) -> Dict:
        return self._booster_roles.get(guild_id, {})
        
    async def handle_member_boost(self, member: discord.Member) -> None:
        guild_id = str(member.guild.id)
        settings = self.get_booster_settings(guild_id)
        
        if not settings.get('enabled', False):
            return
            
        role_id = settings.get('role_id')
        if role_id:
            role = member.guild.get_role(role_id)
            if role:
                try:
                    await member.add_roles(role)
                except:
                    pass
                    
    async def handle_member_unboost(self, member: discord.Member) -> None:
        guild_id = str(member.guild.id)
        settings = self.get_booster_settings(guild_id)
        
        if not settings.get('enabled', False):
            return
            
        role_id = settings.get('role_id')
        if role_id:
            role = member.guild.get_role(role_id)
            if role:
                try:
                    await member.remove_roles(role)
                except:
                    pass
