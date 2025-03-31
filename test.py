import requests

# API endpoint URL
url = "http://127.0.0.1:8000/create/module/"

# Yangi modul uchun ma'lumotlar
payload = {
    "name": "Python Asoslari",
    "description": "Python dasturlash tilining asosiy tushunchalari va sintaksisi"
}

# Authentication token
token = 'c63d57849647eade08a99565822ddc81fec10b94'

# So'rov headers
headers = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json"
}

# POST so'rovni yuborish
response = requests.post(url, json=payload, headers=headers)

# Natijani tekshirish
print("Status Code:", response.status_code)
print("Response:", response.text)
