class EventSummary:
    """
    This entity serves as a way to flesh out all of the details of an Apollo event
    that require us to interact with the Discord API (allowing us to keep the
    underlying model separate from the Discord API).
    """

    def __init__(self, discord_guild, event, responses):
        self.discord_guild = discord_guild
        self.event = event
        self.responses = responses

    @property
    def title(self):
        return self.event.title

    @property
    def description(self):
        return self.event.description

    @property
    def capacity(self):
        return self.event.capacity

    def start_time_display(self):
        return self.event.start_time_string()

    def organizer(self):
        return self.discord_guild.get_member(self.event.organizer_id)

    def accepted_members(self):
        user_ids = self._user_ids_by_status(self.responses, "accepted")[: self.capacity]
        return self._user_ids_to_members(user_ids, self.discord_guild)

    def declined_members(self):
        user_ids = self._user_ids_by_status(self.responses, "declined")
        return self._user_ids_to_members(user_ids, self.discord_guild)

    def tentative_members(self):
        user_ids = self._user_ids_by_status(self.responses, "alternate")
        return self._user_ids_to_members(user_ids, self.discord_guild)

    def standby_members(self):
        if not self.capacity:
            return []
        user_ids = self._user_ids_by_status(self.responses, "accepted")[self.capacity :]
        return self._user_ids_to_members(user_ids, self.discord_guild)

    def _user_ids_by_status(self, responses, status):
        filtered_responses = list(filter(lambda r: r.status == status, responses))
        filtered_responses.sort(key=lambda r: r.last_updated)
        return list(map(lambda r: r.user_id, filtered_responses))

    def _user_ids_to_members(self, user_ids, discord_guild):
        members = []
        for user_id in user_ids:
            member = discord_guild.get_member(user_id)
            if member:
                members.append(member)
        return members
