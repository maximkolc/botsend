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



def _display_help():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the image selection keyboard
    keyboard.add('cock', 'pussy')
    text = 'help'
    return text, keyboard


def _display_main_menu(username):
    keyboard = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True,one_time_keyboard=True)
    keyboard.add('\u2696Обмен',
                 u'\U0001F4C8Курсы криптовалют',
                 u'\U0001F4DEКонтакты',
                 u'\U0001F4D6Условия и правила')
    text = 'Добро пожаловать, {username}, в обменник.'.format(username = username)    
    return text, keyboard

def _display_contacts(username):
    keyboard = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True,one_time_keyboard=True)
    keyboard.add(u'\U0001F448Назад',)
    text = '''
            Тут контакты Можно давать ссылки, например: @mr_rown
            Соглашение: http://telegra.ph/13423424234-03-09
            '''
    return text, keyboard
def _back_to(username):
    prev_func = Person.objects.get(name=username)
    return prev_func

class CommandReceiveView(View):
    def post(self, request, bot_token):
        if bot_token != TOKEN:
            return HttpResponseForbidden('Invalid token')

        commands = {
            '/start': _display_main_menu,
            '/help': _display_help,
            '/mainmenu': _display_main_menu,
            'контакты': _display_contacts,
            'назад': _back_to,
        }
        
        raw = request.body.decode('utf-8')
        try:
            payload = json.loads(raw)
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
        else: 
            chat_ids = payload['message']['chat']['id']
            cmd = payload['message'].get('text')[1:].lower()  # command
            print(cmd+' !!!!!!!!!!!!!!')
            #func = commands.get(cmd.split()[0].lower()) #получяем имя функции
            func = commands.get(cmd)
            # сохранение запроса пользователя в БД
            if func:
                try:
                    person = Person.objects.get(name=payload['message']['from']['username'])
                    person.prev_choice = person.next_choice 
                    person.next_choice = cmd
                    person.chat_id = chat_ids
                    person.save()
                except Person.DoesNotExist:
                    person = Person(
                        name = payload['message']['from']['username'], 
                        prev_choice =  '',
                        next_choice = cmd,
                        chat_id = chat_ids
                        )
                    person.save() 
                finally:
                    text, keyboard = func(payload['message']['from']['username'])
                    TelegramBot.send_message(chat_ids, text, reply_markup=keyboard)
            else:
                try:
                    person = Person.objects.get(name=payload['message']['from']['username'])
                    person.prev_choice = ''
                    person.next_choice = ''
                    person.chat_id = chat_ids
                    person.save()
                except Person.DoesNotExist:
                    person = Person(
                        name = payload['message']['from']['username'], 
                        prev_choice = '',
                        next_choice = '', 
                        chat_id = chat_ids
                        )
                    person.save()
                finally:
                    TelegramBot.send_message(chat_ids, 'Уважаемый {user} какаято херня'.format(user = payload['message']['from']['username']))
                    text, keyboard = _display_main_menu(payload['message']['from']['username'])
                    TelegramBot.send_message(chat_ids, text, reply_markup=keyboard)
        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)