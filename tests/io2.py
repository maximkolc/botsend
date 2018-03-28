import aiohttp
import asyncio
import async_timeout
import os
import requests
import time
#r = requests.get(url, headers=self.base_headers, params=payload)
#yadex.disk settings
base_url = "https://cloud-api.yandex.net:443/v1/disk"
base_headers = {
        "Accept": "application/json",
        "Authorization": "OAuth " + "AQAAAAAGNdiUAAS1RbarEkTeeEjOt37GB16C_5w",
        "Host": "cloud-api.yandex.net"
    }
url = base_url + "/resources"
#payload = {'path': 'humor', 'fields':'_embedded.items.name'}
#telegramm setting
TOKEN = '460229690:AAGfrgxIU1Hh6dBAv0LoYsAWd4YUF7cvLHQ' # токен вашего бота, полученный от @BotFather
tlg_url = "https://api.telegram.org/bot"+TOKEN
payload = {'path': 'humor', 'fields':' _embedded.total'}
r = requests.get(url, headers=base_headers,params=payload)
total = r.json()['_embedded']['total']

async def get_file_name_coroutine(session,total,filetypes):
    offset = total 
    print (offset)
    payload = {'path': 'humor', 'fields':'_embedded.items.name, _embedded.items.file', 'offset':offset}
    async with session.get(url,headers = base_headers, params=payload) as response:
        file = await response.json()
        ext = file['_embedded']['items'][0]['name'].split('.')[1]
        if ext.lower() in filetypes:
            print (file['_embedded']['items'][0]['name'])
            return file['_embedded']['items'][0]['name'], file['_embedded']['items'][0]['file']

async def send_mess(chat, text, session):  
    params = {'chat_id': chat, 'text': text}
    async with session.post(tlg_url + '/sendMessage', data=params) as response:
        #res = await response.json()
        try:
            assert response.status == 200
        except:
            return aiohttp.web.Response(status=500)
  
async def loadfile(session,num_file, total, ftypes):
    i = 0
    while i != num_file: 
        total = total -1
        name,link = await get_file_name_coroutine(session = session, total = total, filetypes = ftypes)
        i = i+1
        async with session.get(link) as resp:
            with open(name, 'ab') as fd:
                while True:
                    chunk = await resp.content.read(1024)
                    if not chunk:
                        break
                    fd.write(chunk)

async def main(loop):
    start = time.time()
    async with aiohttp.ClientSession(loop=loop) as session:
        tasks = [loadfile(session,20, total, ['gif'])]# send_mess("@cool_chanel", 'hello',session)]
        await asyncio.gather(*tasks)
    print("Process took: {:.2f} seconds".format(time.time() - start))
 
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(main(loop))
    loop.close()