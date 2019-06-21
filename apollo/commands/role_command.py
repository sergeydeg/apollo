import discord
from discord.ext import commands

from apollo.queries import find_or_create_guild
from apollo.translate import t


class RoleCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def role(self, ctx):
        """Change the minimum role required to perform various actions"""
        # This is a placeholder until we have support for sub command help
        if not ctx.invoked_subcommand:
            await ctx.send(
                """
**Specify the minimum role to create events**
By default anyone can create events.

```
!role event <role>
```

**Specify the minimum role to create event channels**
By default, those with `Manager Server` and above can create event channels.

```
!role channel <role>
```

**Specify the minimum role to delete events**
By default those with `Manager Server` and above can delete events.
Also worthwhile to note that users can always delete their own events.

```
!role delete <role>
```
                """
            )

    @role.command()
    async def event(self, ctx, *, role: discord.Role):
        """Change or view the minimum role required to create events"""
        with self.bot.scoped_session() as session:
            guild = find_or_create_guild(session, ctx.guild.id)
            guild.event_role_id = role.id
            session.add(guild)

        await ctx.send(t("role.event_role_changed").format(role))

    @role.command()
    async def channel(self, ctx, *, role: discord.Role):
        """Change or view the minimum role required to create event channels"""
        with self.bot.scoped_session() as session:
            guild = find_or_create_guild(session, ctx.guild.id)
            guild.channel_role_id = role.id
            session.add(guild)

        await ctx.send(t("role.channel_role_changed").format(role))

    @role.command()
    async def delete(self, ctx, *, role: discord.Role):
        """Change or view the minimum role required to delete events"""
        with self.bot.scoped_session() as session:
            guild = find_or_create_guild(session, ctx.guild.id)
            guild.delete_role_id = role.id
            session.add(guild)

        await ctx.send(t("role.delete_role_changed").format(role))

    @event.error
    async def event_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            with self.bot.scoped_session() as session:
                guild = find_or_create_guild(session, ctx.guild.id)

            role = discord.utils.get(ctx.guild.roles, id=guild.event_role_id)

            await ctx.send(t("role.event_role_current").format(role, ctx.prefix))

    @channel.error
    async def channel_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            with self.bot.scoped_session() as session:
                guild = find_or_create_guild(session, ctx.guild.id)

            role = discord.utils.get(ctx.guild.roles, id=guild.channel_role_id)

            await ctx.send(t("role.channel_role_current").format(role, ctx.prefix))

    @delete.error
    async def delete_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            with self.bot.scoped_session() as session:
                guild = find_or_create_guild(session, ctx.guild.id)

            role = discord.utils.get(ctx.guild.roles, id=guild.delete_role_id)

            await ctx.send(t("role.delete_role_current").format(role, ctx.prefix))
