from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
import os
from dotenv import load_dotenv

load_dotenv()

RSA_KEY_PASSWORD = os.getenv('RSA_KEY_PASSWORD')
BINARY_PASSWORD = RSA_KEY_PASSWORD.encode()

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


# 키 생성
private_key, public_key = generate_rsa_key_pair()
save_key_to_file(private_key, public_key, "private_test_key.pem",
                 "public_test_key.pem", BINARY_PASSWORD)
