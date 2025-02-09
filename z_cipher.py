import random
from sympy import randprime
from Crypto.Cipher import ChaCha20
import base64

p = randprime(2**64, 2**128)
g = 6443

a = random.randint(1, p-1)
b = random.randint(1, p-1)

A = pow(g, a, p)
B = pow(g, b, p)

bob = pow(A, b, p)
alice = pow(B, a, p)

print(bob)
print(alice)

###

# key = os.urandom(32)
key = bob.to_bytes(32, byteorder='big')


def encrypt(message, _key):
    cipher = ChaCha20.new(key=_key)
    nonce = cipher.nonce
    encrypted = cipher.encrypt(message.encode())
    return base64.b64encode(nonce + encrypted).decode()


def decrypt(message, _key):
    encrypted_message = base64.b64decode(message)
    nonce = encrypted_message[:8]
    ciphertext = encrypted_message[8:]

    cipher = ChaCha20.new(key=_key, nonce=nonce)
    decrypted = cipher.decrypt(ciphertext)
    return decrypted.decode()


user_input = input("Say Something: ")
print(f"Original {user_input}")

user_input = encrypt(user_input, key)
print(f"Encrypted: {user_input}")

user_input = decrypt(user_input, key)
print(f"Decrypted: {user_input}")


