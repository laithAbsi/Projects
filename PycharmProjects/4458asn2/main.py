import os
from typing import Tuple

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import HMAC, SHA256
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Util.Padding import pad, unpad

MODES_MAP = {
    "ECB": AES.MODE_ECB,
    "CBC": AES.MODE_CBC,
    "CTR": AES.MODE_CTR,
    "CFB": AES.MODE_CFB,
    "OFB": AES.MODE_OFB,
}


class AESEncryption:
    """Encrypts/decrypts messages using AES encryption with the given key using the specified mode of operation."""

    def __init__(self, key: bytes, mode: str = "CBC") -> None:
        if mode not in MODES_MAP:
            raise ValueError("Invalid mode of operation specified.")

        self.key, self.mode = key, mode

    @classmethod
    def from_nbits(cls, nbits: int = 256, mode: str = "CBC"):
        """Creates an AES encryption object with a new key with the given number of bits."""
        key = get_random_bytes(nbits // 8)
        return cls(key, mode)

    def encrypt(self, message: bytes) -> bytes:
        """Encrypts the given message using AES."""
        if self.mode == "ECB":
            cipher = AES.new(self.key, AES.MODE_ECB)
            return cipher.encrypt(pad(message, AES.block_size))
        elif self.mode == "CTR":
            nonce = get_random_bytes(8)  # Typically, nonce is 8 bytes in CTR mode
            cipher = AES.new(self.key, AES.MODE_CTR, nonce=nonce)
            return nonce + cipher.encrypt(message)  # Prepend the nonce for decryption
        else:
            iv = get_random_bytes(AES.block_size)
            cipher = AES.new(self.key, MODES_MAP[self.mode], iv=iv)
            return iv + cipher.encrypt(pad(message, AES.block_size))

    def decrypt(self, message: bytes) -> bytes:
        """Decrypts the given message using AES."""
        if self.mode == "ECB":
            cipher = AES.new(self.key, AES.MODE_ECB)
            return unpad(cipher.decrypt(message), AES.block_size)
        elif self.mode == "CTR":
            nonce = message[:8]  # Extract the nonce (first 8 bytes)
            ciphertext = message[8:]
            cipher = AES.new(self.key, AES.MODE_CTR, nonce=nonce)
            return cipher.decrypt(ciphertext)
        else:
            iv = message[:AES.block_size]
            ciphertext = message[AES.block_size:]
            cipher = AES.new(self.key, MODES_MAP[self.mode], iv=iv)
            return unpad(cipher.decrypt(ciphertext), AES.block_size)


class AESEncryptionWithAuthentication:
    """
    Encrypts/decrypts messages using AES encryption and authenticates them using an attached
    MAC tag (HMAC with SHA256) with the given keys using the specified mode of operation.
    """

    def __init__(self, key_aes: bytes, key_hmac: bytes, mode: str = "CBC") -> None:
        if mode not in MODES_MAP:
            raise ValueError("Invalid mode of operation specified.")
        self.key_aes, self.key_hmac, self.mode = key_aes, key_hmac, mode

    @classmethod
    def from_nbits(cls, nbits: int = 256, mode: str = "CBC"):
        """Creates an AES encryption with authentication object with new keys with the given number of bits."""
        key_aes = get_random_bytes(nbits // 8)
        key_hmac = get_random_bytes(SHA256.digest_size)
        return cls(key_aes, key_hmac, mode)

    def encrypt(self, message: bytes) -> bytes:
        """Encrypts the given message using AES and attaches a MAC tag."""
        if self.mode == "ECB":
            cipher = AES.new(self.key_aes, AES.MODE_ECB)
            ciphertext = cipher.encrypt(pad(message, AES.block_size))
        elif self.mode == "CTR":
            nonce = get_random_bytes(8)  # Typically, nonce is 8 bytes in CTR mode
            cipher = AES.new(self.key_aes, AES.MODE_CTR, nonce=nonce)
            ciphertext = nonce + cipher.encrypt(message)
        else:
            iv = get_random_bytes(AES.block_size)
            cipher = AES.new(self.key_aes, MODES_MAP[self.mode], iv=iv)
            ciphertext = iv + cipher.encrypt(pad(message, AES.block_size))

        # Creating HMAC for authentication
        hmac = HMAC.new(self.key_hmac, ciphertext, digestmod=SHA256)
        return ciphertext + hmac.digest()

    def decrypt(self, message: bytes) -> bytes:
        """
        Decrypts the given message using AES and authenticates it using the attached MAC tag.
        Raises a `ValueError` if the message has been tampered with.
        """
        hmac_received = message[-SHA256.digest_size:]
        ciphertext = message[:-SHA256.digest_size]

        # Verifying HMAC to ensure integrity
        hmac = HMAC.new(self.key_hmac, ciphertext, digestmod=SHA256)
        try:
            hmac.verify(hmac_received)
        except ValueError:
            raise ValueError("Message authentication failed.")

        if self.mode == "ECB":
            cipher = AES.new(self.key_aes, AES.MODE_ECB)
            plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        elif self.mode == "CTR":
            nonce = ciphertext[:8]  # Extract the nonce (first 8 bytes)
            ciphertext = ciphertext[8:]
            cipher = AES.new(self.key_aes, AES.MODE_CTR, nonce=nonce)
            plaintext = cipher.decrypt(ciphertext)
        else:
            iv = ciphertext[:AES.block_size]
            ciphertext = ciphertext[AES.block_size:]
            cipher = AES.new(self.key_aes, MODES_MAP[self.mode], iv=iv)
            plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

        return plaintext

class RSAEncryption:
    """Encrypts/decrypts messages using RSA encryption with the given key."""

    def __init__(self, key: RSA.RsaKey) -> None:
        self.key = key

    @classmethod
    def from_nbits(cls, nbits: int = 2048):
        """Creates an RSA encryption object with a new key with the given number of bits."""
        key = RSA.generate(nbits)
        return cls(key)

    @classmethod
    def from_file(cls, filename: str, passphrase: str = None):
        """Creates an RSA encryption object with a key loaded from the given file."""
        with open(filename, 'rb') as f:
            key = RSA.import_key(f.read(), passphrase=passphrase)
        return cls(key)

    def to_file(self, filename: str, passphrase: str = None):
        """Saves this RSA encryption object's key to the given file."""
        with open(filename, 'wb') as f:
            if passphrase:
                f.write(self.key.export_key(pkcs=8, protection="scryptAndAES128-CBC", passphrase=passphrase))
            else:
                f.write(self.key.export_key())

    def encrypt(self, message: bytes) -> bytes:
        """Encrypts the given message using RSA."""
        cipher_rsa = PKCS1_OAEP.new(self.key)
        return cipher_rsa.encrypt(message)

    def decrypt(self, message: bytes) -> bytes:
        """Decrypts the given message using RSA."""
        cipher_rsa = PKCS1_OAEP.new(self.key)
        return cipher_rsa.decrypt(message)


class HybridEncryption:
    """Uses RSA and AES encryption (hybrid cryptosystem) to encrypt (large) messages."""

    def __init__(self, rsa: RSAEncryption) -> None:
        self.rsa = rsa

    def encrypt(self, message: bytes) -> Tuple[bytes, bytes]:
        """
        Encrypts the given message using a hybrid cryptosystem (AES and RSA).
        Returns the encrypted message and the encrypted symmetric key.
        """
        aes = AESEncryption.from_nbits()
        encrypted_message = aes.encrypt(message)
        encrypted_key = self.rsa.encrypt(aes.key)
        return encrypted_message, encrypted_key

    def decrypt(self, message: bytes, message_key: bytes) -> bytes:
        """
        Decrypts the given message using a hybrid cryptosystem (AES and RSA).
        Requires the encrypted symmetric key that the message was encrypted with.
        """
        aes_key = self.rsa.decrypt(message_key)
        aes = AESEncryption(aes_key)
        return aes.decrypt(message)


class DigitalSignature:
    """Uses RSA encryption and SHA-256 hashing to create/verify digital signatures."""

    def __init__(self, rsa: RSAEncryption) -> None:
        self.rsa = rsa

    def sign(self, message: bytes) -> bytes:
        """Signs the given message using RSA and SHA-256 and returns the digital signature."""
        h = SHA256.new(message)
        signer = pkcs1_15.new(self.rsa.key)
        return signer.sign(h)

    def verify(self, message: bytes, signature: bytes) -> bool:
        """Verifies the digital signature of the given message using RSA and SHA-256."""
        h = SHA256.new(message)
        verifier = pkcs1_15.new(self.rsa.key.publickey())
        try:
            verifier.verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False


if __name__ == "__main__":
    # Messages and Keys
    MESSAGE = b"This is a test message."
    MESSAGE_LONG = get_random_bytes(100_000)
    LOREM = "lorem.txt"

    RSA_KEY = "rsa_key.pem"
    RSA_KEY_TEST = "rsa_key_test.pem"
    RSA_SIG = "rsa_sig.pem"
    RSA_PASSPHRASE = "123456"

    # AES
    for mode in MODES_MAP:
        aes = AESEncryption.from_nbits(256, mode)
        encrypted_msg = aes.encrypt(MESSAGE)
        decrypted_msg = aes.decrypt(encrypted_msg)
        print(f"[AES] {mode} Successfully Decrypted:", MESSAGE == decrypted_msg)

    # AES with Authentication
    for mode in MODES_MAP:
        aes_auth = AESEncryptionWithAuthentication.from_nbits(256, mode)
        encrypted_msg = aes_auth.encrypt(MESSAGE)
        decrypted_msg = aes_auth.decrypt(encrypted_msg)
        print(f"[AES-AUTH] {mode} Successfully Decrypted:", MESSAGE == decrypted_msg)

    aes_auth = AESEncryptionWithAuthentication.from_nbits(256)
    encrypted_msg = aes_auth.encrypt(MESSAGE_LONG)

    modified_msg = bytearray(encrypted_msg)
    modified_msg[1000] ^= 0xFF  # invert bits of byte
    modified_msg = bytes(modified_msg)

    try:
        aes_auth.decrypt(modified_msg)
        errored = False
    except ValueError:
        errored = True

    print("[AES-AUTH] Modified Fails Decryption:", errored)

    # RSA
    rsa = RSAEncryption.from_file(RSA_KEY, RSA_PASSPHRASE)
    encrypted_msg = rsa.encrypt(MESSAGE)
    decrypted_msg = rsa.decrypt(encrypted_msg)
    print("[RSA] Successfully Decrypted:", MESSAGE == decrypted_msg)

    rsa.to_file(RSA_KEY_TEST, RSA_PASSPHRASE)
    rsa_test = RSAEncryption.from_file(RSA_KEY_TEST, RSA_PASSPHRASE)
    print("[RSA] Successfully Imported/Exported:", rsa.key == rsa_test.key)
    os.remove(RSA_KEY_TEST)

    # Hybrid
    with open(LOREM, "rb") as f:
        lorem = f.read()

    hybrid = HybridEncryption(rsa)
    encrypted_msg, encrypted_msg_key = hybrid.encrypt(lorem)
    decrypted_msg = hybrid.decrypt(encrypted_msg, encrypted_msg_key)
    print("[HYBRID] Successfully Decrypted:", decrypted_msg == lorem)

    # Digital Signature
    signer = DigitalSignature(RSAEncryption.from_file(RSA_SIG, RSA_PASSPHRASE))
    encrypted_msg, encrypted_msg_key = hybrid.encrypt(MESSAGE_LONG)
    msg_signature = signer.sign(encrypted_msg)

    modified_msg = bytearray(encrypted_msg)
    modified_msg[1000] ^= 0xFF  # invert bits of byte
    modified_msg = bytes(modified_msg)

    print("[SIG] Original Valid:", signer.verify(encrypted_msg, msg_signature))
    print("[SIG] Modified NOT Valid:", not signer.verify(modified_msg, msg_signature))

    decrypted_msg = hybrid.decrypt(encrypted_msg, encrypted_msg_key)
    print("[SIG] Original Successfully Decrypted:", MESSAGE_LONG == decrypted_msg)

    decrypted_msg = hybrid.decrypt(modified_msg, encrypted_msg_key)
    print("[SIG] Modified Fails Decryption:", MESSAGE_LONG != decrypted_msg)
