import arrow
import discord
import psutil

from apollo.constants import EMBED_COLOR
from apollo.models import Event, User
from apollo.translate import t


class AboutEmbed:

    INVITE_LINK = "https://discordapp.com/oauth2/authorize?client_id=475744554910351370&scope=bot&permissions=355408"
    SERVER_LINK = "https://discord.gg/ZVevvh2"
    GITHUB_LINK = "https://github.com/jgayfer/apollo"

    def __init__(self, bot, session):
        self.bot = bot
        self.session = session


    def call(self):
        embed = discord.Embed(title=t("apollo"))
        embed.color = EMBED_COLOR
        embed.description = self._description()
        embed.add_field(name=t("about.users"), value=self._user_count())
        embed.add_field(name=t("about.servers"), value=len(self.bot.guilds))
        embed.add_field(name=t("about.events"), value=self._event_count())
        embed.add_field(name=t("about.memory"), value=self._memory_usage())
        embed.add_field(name=t("about.cpu"), value=self._cpu_usage())
        embed.add_field(name=t("about.uptime"), value=self._uptime())
        embed.set_footer(
            text=t("about.made_with"),
            icon_url='http://i.imgur.com/5BFecvA.png'
            )
        return embed


    def _cpu_usage(self):
        return "%0.2f%%" % (psutil.cpu_percent())


    def _event_count(self):
        return len(self.session.query(Event).all())


    def _description(self):
        return (t("about.invite_link").format(self.INVITE_LINK) + "\n" +
                t("about.discord_server").format(self.SERVER_LINK) + "\n" +
                t("about.source_code").format(self.GITHUB_LINK))


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
