from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key


# RSA 비대칭 키 쌍 생성
def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        # 공개 지수 설정
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return private_key, public_key


# Private key 저장
def save_key_to_file(private_key, public_key, private_key_file, public_key_file, password=None):
    with open(private_key_file, "wb") as key_file:
        key_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.BestAvailableEncryption(
                    password) if password else serialization.NoEncryption()
            )
        )

    with open(public_key_file, "wb") as key_file:
        key_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )


# 개인키 가져오기
def load_private_key(filename: str, password=None):
    with open(filename, "rb") as key_file:
        return load_pem_private_key(
            key_file.read(),
            password=password.encode() if password else None
        )


def load_public_key(filename: str):
    with open(filename, "rb") as pub_file:
        return load_pem_public_key(
            pub_file.read()
        )


# 공개 키로 암호화
def encrypt_with_public_key(public_key, message: str) -> bytes:
    encrypted_message = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_message


# 비공개 키로 복호화
def decrypt_with_private_key(private_key, encrypted_message: bytes) -> str:
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ).decode()
    return decrypted_message
