import aiohttp
import asyncio
import async_timeout
import os
import requests
import time

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

async def produce(queue,total,filetypes):
    offset = total - 1
    while offset != 0:
        # produce an item
        payload = {'path': 'humor', 'fields':'_embedded.items.name, _embedded.items.file', 'offset':offset}
        # simulate i/o operation using sleep
        async with aiohttp.ClientSession() as session:
            async with session.get(url,headers = base_headers, params=payload) as response:
                file = await response.json()
                ext = file['_embedded']['items'][0]['name'].split('.')[1]
                if ext.lower() in filetypes:
                #print (file['_embedded']['items'][0]['name'])
                    item = file['_embedded']['items'][0]['name'], file['_embedded']['items'][0]['file']
                # put the item in the queue
        await queue.put(item)
        offset = offset - 1
    # indicate the producer is done
    await queue.put(None)


async def consume(queue,num_file):
    n = 0
    async with aiohttp.ClientSession() as session:
        while n !=num_file:
            # wait for an item from the producer
            link = await queue.get()
            print(link)
            if link is None:
                # the producer emits None to indicate that it is done
                break
            # simulate i/o operation using sleep
            async with session.get(link[1]) as resp:
                with open(link[0], 'ab') as fd:
                    while True:
                        chunk = await resp.content.read(102)
                        if not chunk:
                            break
                        fd.write(chunk)
            n = n+1


loop = asyncio.get_event_loop()
queue = asyncio.Queue(loop=loop)
start = time.time()
producer_coro = produce(queue, total, ['gif'])
consumer_coro = consume(queue, 10)
loop.run_until_complete(asyncio.gather(producer_coro, consumer_coro))
loop.close()
print("Process took: {:.2f} seconds".format(time.time() - start))