import discord

from apollo.queries import find_or_create_guild


class Can:

    def __init__(self, session, user):
        self.session = session
        self.user = user
        self.guild = user.guild


    def channel(self):
        guild = find_or_create_guild(self.session, self.guild.id)
        channel_role = self._get_role(guild.channel_role_id)
        return (
            self.user.top_role >= channel_role or
            self.user.guild_permissions.manage_guild
            )


    def delete(self):
        guild = find_or_create_guild(self.session, self.guild.id)
        delete_role = self._get_role(guild.delete_role_id)
        return (
            self.user.top_role >= delete_role or
            self.user.guild_permissions.manage_guild
            )


    def event(self):
        guild = find_or_create_guild(self.session, self.guild.id)
        event_role = self._get_role(guild.event_role_id)
        return self.user.top_role >= event_role


    def _get_role(self, role_id):
        role = discord.utils.get(self.guild.roles, id=role_id)
        if not role:
            role = self.guild.default_role
        return role
