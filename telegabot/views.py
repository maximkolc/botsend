from django.shortcuts import render
from django.http import HttpResponse
import telebot
from telebot import types
import time
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
import json
from .models import Person

TOKEN = '576824424:AAEFxzVpwSAQ4e8J9npuXFobSQ8PpFgWOEI'

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts
#TelegramBot = telebot.TeleBot(TOKEN)
TelegramBot = telebot.TeleBot(TOKEN)
TelegramBot.set_webhook('https://botsend.ru/telegabot/bot/{bot_token}/'.format(bot_token=TOKEN))
Bot2 = telebot.TeleBot('460229690:AAGfrgxIU1Hh6dBAv0LoYsAWd4YUF7cvLHQ')

def _display_help():
    return 'render_to_string(help.md)'


def _display_planetpy_feed():
    return 'render_to_string feed.md'


class CommandReceiveView(View):
    def post(self, request, bot_token):
        if bot_token != settings.TELEGRAM_BOT_TOKEN:
            return HttpResponseForbidden('Invalid token')

        commands = {
            '/start': _display_help,
            'help': _display_help,
            'feed': _display_planetpy_feed,
        }

        raw = request.body.decode('utf-8')

        try:
            payload = json.loads(raw)
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
        else:
            chat_id = payload['message']['chat']['id']
            cmd = payload['message'].get('text')  # command

            func = commands.get(cmd.split()[0].lower())
            if func:
                TelegramBot.sendMessage(chat_id, func(), parse_mode='Markdown')
            else:
                TelegramBot.sendMessage(chat_id, 'I do not understand you, Sir!')

        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)