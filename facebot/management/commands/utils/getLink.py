import requests


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
    links = []
    files = [] 
    offset = total - 1
    i =0 
    while i != num_file: 
        payload = {'path': 'humor', 'fields':'_embedded.items.name, _embedded.items.file', 'offset':offset}
        response = requests.get(url,headers = base_headers, params=payload)
        file = response.json()
        ext = file['_embedded']['items'][0]['name'].split('.')[1]
        if ext.lower() in filetypes:
            links.append(file['_embedded']['items'][0]['file'])
            files.append(file['_embedded']['items'][0]['name'])
        offset = offset - 1
        i = i+1
    return zip (links,files)    

token = 'AQAAAAAGNdiUAATo52--OmcBuE1NjWAA-rW5NPc'
