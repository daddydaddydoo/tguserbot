# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# You can find misc modules, which dont fit in anything xD
""" Userbot module for other small commands. """

from random import randint
from time import sleep
from os import execl
import sys
import os
import io
import sys
import json
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register
from userbot.events import register, errors_handler


@register(outgoing=True, pattern="^.random")
@errors_handler
async def randomise(items):
    """ For .random command, get a random item from the list of items. """
    if not items.text[0].isalpha() and items.text[0] not in ("/", "#", "@",
                                                             "!"):
        itemo = (items.text[8:]).split()
        index = randint(1, len(itemo) - 1)
        await items.edit("**Query: **\n`" + items.text[8:] +
                         "`\n**Output: **\n`" + itemo[index] + "`")


@register(outgoing=True, pattern="^.sleep( [0-9]+)?$")
@errors_handler
async def sleepybot(time):
    """ For .sleep command, let the userbot snooze for a few second. """
    message = time.text
    if not message[0].isalpha() and message[0] not in ("/", "#", "@", "!"):
        if " " not in time.pattern_match.group(1):
            await time.reply("Syntax: `.sleep [seconds]`")
        else:
            counter = int(time.pattern_match.group(1))
            await time.edit("`I am sulking and snoozing....`")
            sleep(2)
            if BOTLOG:
                await time.client.send_message(
                    BOTLOG_CHATID,
                    "You put the bot to sleep for " + str(counter) +
                    " seconds",
                )
            sleep(counter)


@register(outgoing=True, pattern="^.shutdown$")
@errors_handler
async def killdabot(event):
    """ For .shutdown command, shut the bot down."""
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@",
                                                             "!"):
        await event.edit("Powering off.")
        if BOTLOG:
            await event.client.send_message(BOTLOG_CHATID, "#SHUTDOWN \n"
                                            "Bot shut down")
        await event.client.disconnect()


@register(outgoing=True, pattern="^.restart$")
@errors_handler
async def killdabot(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@",
                                                             "!"):
        await event.edit("Rebooting.")
        if BOTLOG:
            await event.client.send_message(BOTLOG_CHATID, "#RESTART \n"
                                            "Bot Restarted")
        await event.client.disconnect()
        # Spin a new instance of bot
        execl(sys.executable, sys.executable, *sys.argv)
        # Shut the existing one down
        exit()

# Copyright (c) Gegham Zakaryan | 2019
@register(outgoing=True, pattern="^.repeat (.*)")
@errors_handler
async def repeat(rep):
    if not rep.text[0].isalpha() and rep.text[0] not in ("/", "#", "@", "!"):
        cnt, txt = rep.pattern_match.group(1).split(' ', 1)
        replyCount = int(cnt)
        toBeRepeated = txt

        replyText = toBeRepeated + "\n"

        for i in range(0, replyCount - 1):
            replyText += toBeRepeated + "\n"

        await rep.edit(replyText)


@register(outgoing=True, pattern="^.json$")
@errors_handler
async def json(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@",
                                                             "!"):
        the_real_message = None
        reply_to_id = None
        if event.reply_to_msg_id:
            previous_message = await event.get_reply_message()
            the_real_message = previous_message.stringify()
            reply_to_id = event.reply_to_msg_id
        else:
            the_real_message = event.stringify()
            reply_to_id = event.message.id

        with io.BytesIO(str.encode(the_real_message)) as out_file:
            out_file.name = "message.json"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                reply_to=reply_to_id,
                caption="`Here's the decoded message data !!`")
            await event.delete()


CMD_HELP.update({
    'random':
    '.random <item1> <item2> ... <itemN>\
\nUsage: Get a random item from the list of items.'
})

CMD_HELP.update({
    'sleep':
    '.sleep <seconds>\
\nUsage: Simply .sleep to sleep for the designated time in seconds'
})

CMD_HELP.update({
    "shutdown":
    ".shutdown\
\nUsage: Simply .shutdown, equivalent to CTRL-C in terminal"
})

CMD_HELP.update({
    "repeat":
    ".repeat <no.> <text>\
\nUsage: Repeats the text for a number of times. Don't confuse this with spam tho."
})

CMD_HELP.update({"restart": ".restart\
\nUsage: Restarts"})

CMD_HELP.update({
    "json":
    ".json\
\nUsage: Get detailed JSON formatted data about replied message"
})
