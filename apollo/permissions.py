import discord


class HavePermission:
    """Checks whether a user has the necessary permission to perform an action"""

    def __init__(self, discord_member, guild):
        self.discord_member = discord_member
        self.guild = guild

    def channel(self):
        if self.discord_member.guild_permissions.manage_guild:
            return True
        channel_create_role = self._get_role(self.guild.channel_role_id)
        if channel_create_role:
            return self.discord_member.top_role >= channel_create_role

    def delete(self):
        if self.discord_member.guild_permissions.manage_guild:
            return True
        event_delete_role = self._get_role(self.guild.delete_role_id)
        if event_delete_role:
            return self.discord_member.top_role >= event_delete_role

    def event(self):
        if self.discord_member.guild_permissions.manage_guild:
            return True
        event_create_role = self._get_role(self.guild.event_role_id)
        if event_create_role:
            return self.discord_member.top_role >= event_create_role
        else:
            # By default anyone can create events
            return True

    def _get_role(self, role_id):
        return discord.utils.get(self.discord_member.guild.roles, id=role_id)
