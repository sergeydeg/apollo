class FormatDateTime:
    def __init__(self):
        pass

    def call(self, date_time):
        formatted_date_time = date_time.format("ddd MMM Do, YYYY @ h:mm A")
        time_zone = date_time.tzname()
        return f"{formatted_date_time} {time_zone}"
