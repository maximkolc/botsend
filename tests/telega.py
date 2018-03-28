import requests
import time
#telegramm setting

TOKEN = '460229690:AAGfrgxIU1Hh6dBAv0LoYsAWd4YUF7cvLHQ' # токен вашего бота, полученный от @BotFather
tlg_url = "https://api.telegram.org/bot"+TOKEN

def send_mess(chat, text):  
    start = time.time()
    params = {'chat_id': chat, 'text': text}
    response = requests.post(tlg_url + '/sendMessage', data=params)
    print("время выполнения: {:.3f} sec".format(time.time() - start))
    return response

res = send_mess('@cool_chanel','sdfsdf')
print (res.json())