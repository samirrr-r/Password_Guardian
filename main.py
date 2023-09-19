import base64
from cryptography.fernet import Fernet
key = Fernet.generate_key()
f = Fernet(key)
l=  Fernet(b'bEla0jgfV-J34Xx8Mzy2Mw5UEu3kkhZZ5jS164-_Fhs=')

print(str(key)[2:45])
with open("test.txt", "r") as file:
    cont=file.read()
print(cont)

token = l.encrypt(bytes(cont,'utf-8'))
fas=l.decrypt(token)
print(token)
print(fas)
print(len(key))