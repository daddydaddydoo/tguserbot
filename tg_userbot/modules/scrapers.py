import os

from emoji import get_emoji_regexp
from googletrans import LANGUAGES, Translator
from gtts import gTTS
from requests import get

from tg_userbot import CMD_HELP, BOTLOG, BOTLOG_CHATID, LANG
from tg_userbot.events import register


@register(outgoing=True, pattern="^\.currency (.*)")
async def _(event):  # calculates exchange rates, no clue why you would need it, but sure
    if not event.text[0].isalpha() and event.text[0] in ("."):
        if event.fwd_from:
            return
        input_str = event.pattern_match.group(1)
        input_sgra = input_str.split(" ")
        if len(input_sgra) == 3:
            try:
                number = float(input_sgra[0])
                currency_from = input_sgra[1].upper()
                currency_to = input_sgra[2].upper()
                request_url = "https://api.exchangeratesapi.io/latest?base={}".format(currency_from)
                current_response = get(request_url).json()
                if currency_to in current_response["rates"]:
                    current_rate = float(current_response["rates"][currency_to])
                    rebmun = round(number * current_rate, 2)
                    await event.edit("{} {} = {} {}".format(number, currency_from, rebmun, currency_to))
                else:
                    await event.edit("`This seems to be some alien currency, which I can't convert right now.`")
            except e:
                await event.edit(str(e))
        else:
            await event.edit("`Invalid syntax.`")
            return


@register(outgoing=True, pattern=r"^\.tts(?: |$)([\s\S]*)")
async def text_to_speech(query):  # text to speech
    if not query.text[0].isalpha() and query.text[0] in ("."):
        textx = await query.get_reply_message()
        message = query.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await query.edit("`Give a text or reply to a message for Text-to-Speech!`")
            return
        try:
            gTTS(message, lang=LANG)
        except AssertionError:
            await query.edit('The text is empty.\nNothing left to speak after pre-precessing, tokenizing and cleaning.')
            return
        except ValueError:
            await query.edit('Language is not supported.')
            return
        except RuntimeError:
            await query.edit('Error loading the languages dictionary.')
            return
        tts = gTTS(message, lang=LANG)
        tts.save("k.mp3")
        with open("k.mp3", "rb") as audio:
            linelist = list(audio)
            linecount = len(linelist)
        if linecount == 1:
            tts = gTTS(message, lang=LANG)
            tts.save("k.mp3")
        with open("k.mp3", "r"):
            await query.client.send_file(query.chat_id, "k.mp3", voice_note=True)
            os.remove("k.mp3")
            if BOTLOG:
                await query.client.send_message(BOTLOG_CHATID, "tts of `" + message + "` executed successfully!")
            await query.delete()


@register(outgoing=True, pattern=r"^\.trt(?: |$)([\s\S]*)")
async def translateme(trans):  # translator
    if not trans.text[0].isalpha() and trans.text[0] in ("."):
        translator = Translator()
        textx = await trans.get_reply_message()
        message = trans.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await trans.edit("`Give a text or reply to a message to translate!`")
            return
        try:
            reply_text = translator.translate(deEmojify(message), dest=LANG)
        except ValueError:
            await trans.edit("Invalid destination language.")
            return
        source_lan = LANGUAGES[f'{reply_text.src.lower()}']
        transl_lan = LANGUAGES[f'{reply_text.dest.lower()}']
        reply_text = f"From **{source_lan.title()}**\nTo **{transl_lan.title()}:**\n\n{reply_text.text}"
        await trans.edit(reply_text)
        if BOTLOG:
            await trans.client.send_message(BOTLOG_CHATID,
                                            f"Translated some {source_lan.title()} stuff to {transl_lan.title()} just now.")


def deEmojify(inputString):  # removes emojis for safe string handling
    return get_emoji_regexp().sub(u'', inputString)


CMD_HELP.update({
    'scrappers':
        '`.currency <amount> <from> <to>`\
         \nUsage: Converts various currencies for you.\
         \n\n`.tts <text> [or reply]`\
         \nUsage: Translates text to speech for the default language which is set.\nUse .lang <text> to set language for your TTS.\
         \n\n`.trt <text> [or reply]`\
         \nUsage: Translates text to the default language which is set.'})
