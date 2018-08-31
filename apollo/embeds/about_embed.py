import arrow
import discord
import psutil

from apollo.constants import VERSION, EMBED_COLOR
from apollo.models import Event, User


class AboutEmbed:

    INVITE_LINK = "https://discordapp.com/oauth2/authorize?client_id=475744554910351370&scope=bot&permissions=355408"
    SERVER_LINK = "https://discord.gg/ZVevvh2"

    def __init__(self, bot, session):
        self.bot = bot
        self.session = session


    def call(self):
        embed = discord.Embed(title=f"Apollo {VERSION}")
        embed.color = EMBED_COLOR
        embed.description = self._description()
        embed.add_field(name="Users", value=self._user_count())
        embed.add_field(name="Servers", value=len(self.bot.guilds))
        embed.add_field(name="Events", value=self._event_count())
        embed.add_field(name="Memory", value=self._memory_usage())
        embed.add_field(name="CPU", value=self._cpu_usage())
        embed.add_field(name="Uptime", value=self._uptime())
        embed.set_footer(
            text='Made with discord.py',
            icon_url='http://i.imgur.com/5BFecvA.png'
            )
        return embed


    def _cpu_usage(self):
        return "%0.2f%%" % (psutil.cpu_percent())


    def _event_count(self):
        return len(self.session.query(Event).all())


    def _description(self):
        return (f"[Invite Link]({self.INVITE_LINK})\n" +
                f"[Official Discord Server]({self.SERVER_LINK})")


    def _memory_usage(self):
        return "%0.2f MB" % (psutil.virtual_memory().used / 1024**2)


    def _uptime(self):
        now = arrow.utcnow()
        delta = now - self.bot.start_time

        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        fmt = '{h}h {m}m {s}s'
        if days:
            fmt = '{d}d ' + fmt

        return fmt.format(d=days, h=hours, m=minutes, s=seconds)


    def _user_count(self):
        return len(self.session.query(User).all())
