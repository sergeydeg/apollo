import discord

from apollo.can import Can
from apollo import emojis as emoji
from apollo.queries import find_or_create_guild
from apollo.queries import find_or_create_user
from apollo.queries import responses_for_event
from apollo.queries import event_count_for_event_channel
from apollo.translate import t


EMOJI_STATUSES = {
    emoji.CHECK: "accepted",
    emoji.QUESTION: "alternate",
    emoji.CROSS: "declined",
}


class HandleEventReaction:
    def __init__(self, bot, update_event, update_response, request_local_start_time):
        self.bot = bot
        self.update_event = update_event
        self.update_response = update_response
        self.request_local_start_time = request_local_start_time

    async def call(self, event, payload):
        channel = self.bot.get_channel(payload.channel_id)

        if payload.emoji.name == emoji.CLOCK:
            # We generally clear the reaction later on, but as we could we
            # waiting on the user to input a time zone, we don't want this
            # reaction to hang around for too long.
            await self.bot.remove_reaction(payload)

            discord_user = self.bot.get_user(payload.user_id)

            with self.bot.scoped_session() as session:
                apollo_user = find_or_create_user(session, payload.user_id)

            await self.request_local_start_time.call(apollo_user, discord_user, event)

        if payload.emoji.name == emoji.SKULL:
            member = self.bot.find_guild_member(payload.guild_id, payload.user_id)

            with self.bot.scoped_session() as session:
                guild = find_or_create_guild(session, payload.guild_id)

            if event.organizer_id != member.id and not Can(member, guild).delete():
                return await member.send("You don't have permission to do that.")

            with self.bot.scoped_session() as session:
                session.delete(event)

            await channel.delete_messages([discord.Object(id=event.message_id)])

            with self.bot.scoped_session() as session:
                event_count = event_count_for_event_channel(session, channel.id)

            if event_count == 0:
                await channel.send(t("channel.no_events"))

            return

        rsvp_status = EMOJI_STATUSES.get(payload.emoji.name)
        if rsvp_status:
            await self.update_response.call(event.id, payload.user_id, rsvp_status)

            with self.bot.scoped_session() as session:
                responses = responses_for_event(session, event.id)

            await self.update_event.call(event, responses, channel)
