from cryptography.fernet import Fernet

key = Fernet.generate_key()
# the key is type bytes
print("key: ", key)
with open("key.fernet", "wb") as file:
    file.write(key)

f = Fernet(key)
# encrypt the message
token = f.encrypt(b"my deep dark secret")
print("token: ", token)

# decrypt the message
msg = f.decrypt(token)
print("plain text", msg)