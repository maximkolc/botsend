import requests
base_url = "https://cloud-api.yandex.net:443/v1/disk"
token = token
base_headers = {"Accept": "application/json",
"Authorization": "OAuth " + token,"Host": "cloud-api.yandex.net"}
    url = base_url
    r = requests.get(url, headers=self.base_headers)
    json_dict = r.json()
    returnjson_dict
https://oauth.yandex.ru/authorize?response_type=token&client_id=55cd708ef7764279ace87970649d86d1