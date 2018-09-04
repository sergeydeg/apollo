import discord
from discord.ext import commands

from apollo.queries import find_or_create_guild


class RoleCommand:

    def __init__(self, bot):
        self.bot = bot


    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def role(self, ctx):
        """Change the minimum role required to perform various actions"""
        pass


    @role.command()
    async def event(self, ctx, *, role: discord.Role):
        """Change or view the minimum role required to create events"""
        session = self.bot.Session()
        guild = find_or_create_guild(session, ctx.guild.id)
        guild.event_role_id = role.id
        session.add(guild)
        session.commit()

        await ctx.send(f"The minimum event creation role has been set to: **{role}**")


    @role.command()
    async def channel(self, ctx, *, role: discord.Role):
        """Change or view the minimum role required to create event channels"""
        session = self.bot.Session()
        guild = find_or_create_guild(session, ctx.guild.id)
        guild.channel_role_id = role.id
        session.add(guild)
        session.commit()

        await ctx.send(f"The minimum channel creation role has been set to: **{role}**")


    @role.command()
    async def delete(self, ctx, *, role: discord.Role):
        """Change or view the minimum role required to delete events"""
        session = self.bot.Session()
        guild = find_or_create_guild(session, ctx.guild.id)
        guild.delete_role_id = role.id
        session.add(guild)
        session.commit()

        await ctx.send(f"The minimum event deletion role has been set to: **{role}**")


    @event.error
    async def event_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            session = self.bot.Session()
            guild = find_or_create_guild(session, ctx.guild.id)
            session.commit()

            role = discord.utils.get(ctx.guild.roles, id=guild.event_role_id)

            await ctx.send(
                f"The minimum role required for event creation is: **{role}**\n\n"
                + f"To change this role, use: `{ctx.prefix}role event <role>`"
                )


    @channel.error
    async def channel_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            session = self.bot.Session()
            guild = find_or_create_guild(session, ctx.guild.id)
            session.commit()

            role = discord.utils.get(ctx.guild.roles, id=guild.channel_role_id)

            await ctx.send(
                f"The minimum role required for event channel creation is: **{role}**\n\n"
                + "Note that regardless of this setting, users with the "
                + "`Manage Server` permission will always be able to create event channels.\n\n"
                + f"To change this role, use: `{ctx.prefix}role channel <role>`"
                )


    @delete.error
    async def delete_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            session = self.bot.Session()
            guild = find_or_create_guild(session, ctx.guild.id)
            session.commit()

            role = discord.utils.get(ctx.guild.roles, id=guild.delete_role_id)

            await ctx.send(
                f"The minimum role required for event deletion is: **{role}**\n\n"
                + "Note that regardless of this setting, users with the "
                + "`Manage Server` permission will always be able to delete events.\n\n"
                + f"To change this role, use: `{ctx.prefix}role delete <role>`"
                )
