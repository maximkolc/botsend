import requests
import random

class NotFileinDisk(Exception):
    pass

def get_links(dir, filetypes, num_file, token):
    base_url = "https://cloud-api.yandex.net:443/v1/disk"
    base_headers = {
            "Accept": "application/json",
            "Authorization": "OAuth " + token,
            "Host": "cloud-api.yandex.net"
        }
    url = base_url + "/resources"
    payload = {'path': dir, 'fields':' _embedded.total'}
    r = requests.get(url, headers=base_headers,params=payload)
    total = r.json()['_embedded']['total']
    links = [] # возвращается список имен файлов
    names = [] # возвращается список ссылок на файлы
    payload = {'path': dir, 'fields':'_embedded.items.name, _embedded.items.file', 'limit':total}
    response = requests.get(url,headers = base_headers, params=payload)
    files = response.json()
    random.shuffle(files['_embedded']['items'])
    i = 0 
    count_true_file = 0 
    while i != total:    
        ext = files['_embedded']['items'][i]['name'].split('.')[1]
        if ext.lower() in filetypes:
            links.append(files['_embedded']['items'][i]['file'])
            names.append(files['_embedded']['items'][i]['name'])
            count_true_file = count_true_file + 1
        if count_true_file == num_file:
            break
        i = i+1
    if count_true_file != num_file:
        raise NotFileinDisk
    return links,names    

token = 'AQAAAAAGNdiUAATo52--OmcBuE1NjWAA-rW5NPc'

try:
    links, names = get_links('humor',['exe'], 3, token)
    for link, name in zip(links, names):
        print(link)
    print(name)
except NotFileinDisk:
    print('файлы указанного типа отсутствуют на диске')
