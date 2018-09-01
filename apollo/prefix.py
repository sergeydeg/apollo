from apollo.constants import DEFAULT_PREFIX


def prefix_callable(bot, message):
    user_id = bot.user.id
    base = [f'<@!{user_id}> ', f'<@{user_id}> ']

    if message.guild is None:
        base.append(DEFAULT_PREFIX)
    else:
        custom_prefix = bot.cache.get_prefix(message.guild.id)
        if custom_prefix:
            base.append(custom_prefix)
        else:
            base.append(DEFAULT_PREFIX)

    return base
