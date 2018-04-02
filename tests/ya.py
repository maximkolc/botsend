import requests

def getNumsF(n, *args):
    sum =0
    
    token = 'AQAAAAAGNdiUAAS1Rb-7aqjgkkBvmrgKZEYo7vs'
    base_headers = {
    "Accept": "application/json",
    "Authorization": "OAuth " + token,
    "Host": "cloud-api.yandex.net"
    }
    base_url = "https://cloud-api.yandex.net:443/v1/disk"
    url = base_url + "/resources"
    payload = {'path': 'humor','fields':'_embedded.items.name, _embedded.items.type','offset':n}
    
    r = requests.get(url, headers=base_headers,params=payload)
    nums = len(r.json()['_embedded']['items'])
    
    if nums < 20:
        return sum + nums
    else:
        k = payload['offset']+nums
        #sum = nums
        return nums + getNumsF(k)

n = getNumsF(0)
print(n)