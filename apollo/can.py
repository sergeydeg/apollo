import discord


class Can:

    def __init__(self, discord_member, guild):
        self.discord_member = discord_member
        self.guild = guild


    def channel(self):
        if self.discord_member.guild_permissions.manage_guild:
            return True
        if self._user_is_at_or_above_role(self.guild.channel_role_id):
            return True


    def delete(self):
        if self.discord_member.guild_permissions.manage_guild:
            return True
        if self._user_is_at_or_above_role(self.guild.delete_role_id):
            return True


    def event(self):
        if self.discord_member.guild_permissions.manage_guild:
            return True
        if self._user_is_at_or_above_role(self.guild.event_role_id):
            return True


    def _user_is_at_or_above_role(self, role_id):
        role = discord.utils.get(self.discord_member.guild.roles, id=role_id)
        if not role:
            return True
        return self.discord_member.top_role >= role
