from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from pathlib import Path

print("=" * 70)
print("SECURENOVA PROJECT 4 - ED25519 KEY PAIR GENERATION")
print("=" * 70)

private_key = Ed25519PrivateKey.generate()
public_key = private_key.public_key()

private_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)

public_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)

Path("agent_private_key.pem").write_bytes(private_bytes)
Path("agent_public_key.pem").write_bytes(public_bytes)

print()
print("Ed25519 key pair generated successfully.")
print()
print("Private key file :", Path("agent_private_key.pem").resolve())
print("Public key file  :", Path("agent_public_key.pem").resolve())
print()
print("Private key exists:", Path("agent_private_key.pem").exists())
print("Public key exists :", Path("agent_public_key.pem").exists())
print()
print("STATUS : KEY PAIR GENERATED")
print("=" * 70)