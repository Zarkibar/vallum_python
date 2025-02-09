from Crypto.Cipher import ChaCha20
import base64


class Cipher:
    # def __init__(self, key: int):
    #     self.key = key.to_bytes(32, byteorder='big')
    #
    # def encrypt(self, message):
    #     cipher = ChaCha20.new(key=self.key)
    #     nonce = cipher.nonce
    #     encrypted = cipher.encrypt(message.encode())
    #     return base64.b64encode(nonce + encrypted).decode()
    #
    # def decrypt(self, message):
    #     encrypted_message = base64.b64decode(message)
    #     nonce = encrypted_message[:8]
    #     ciphertext = encrypted_message[8:]
    #
    #     cipher = ChaCha20.new(key=self.key, nonce=nonce)
    #     decrypted = cipher.decrypt(ciphertext)
    #     return decrypted.decode()

    def __init__(self, key: int):
        self.key = key % 256

    def encrypt(self, message):
        return ''.join(chr(ord(char) ^ self.key) for char in message)

    def decrypt(self, message):
        return ''.join(chr(ord(char) ^ self.key) for char in message)

