import datetime

from discord.ext import commands, tasks

from apollo.models import Event

REMINDER_PERIOD_MINUTES = 10


class AutomaticReminders(commands.Cog):
    def __init__(self, bot, send_event_reminders):
        self.bot = bot
        self.send_event_reminders = send_event_reminders
        self.send_reminders.start()

    @tasks.loop(seconds=60)
    async def send_reminders(self):
        current_time = datetime.datetime.now()

        # We strip seconds so that our query will match exactly on event start times.
        targetted_start_time = (
            current_time + datetime.timedelta(minutes=REMINDER_PERIOD_MINUTES)
        ).replace(second=0, microsecond=0)

        with self.bot.scoped_session() as session:
            events_starting_soon = (
                session.query(Event).filter_by(start_time=targetted_start_time).all()
            )

        for event in events_starting_soon:
            await self.send_event_reminders.call(event)

    @send_reminders.before_loop
    async def before_sending_reminders(self):
        await self.bot.wait_until_ready()
