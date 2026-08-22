from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from pathlib import Path

print("=" * 70)
print("SECURENOVA PROJECT 4 - ED25519 MESSAGE SIGNATURE TEST")
print("=" * 70)

# Load the previously generated private key
private_key = serialization.load_pem_private_key(
    Path("agent_private_key.pem").read_bytes(),
    password=None,
)

public_key = serialization.load_pem_public_key(
    Path("agent_public_key.pem").read_bytes()
)

# Original outgoing agent message
original_message = "Approve SecureNova request for user_123."

# Sign the original message
signature = private_key.sign(original_message.encode("utf-8"))

print()
print("Original message:")
print(original_message)

print()
print("Signature generated successfully.")
print("Signature length:", len(signature), "bytes")

# Verify the original message
try:
    public_key.verify(signature, original_message.encode("utf-8"))
    print()
    print("Original message verification: SUCCESS")
except InvalidSignature:
    print()
    print("Original message verification: FAILED")

# Tamper with ONE character
tampered_message = "Approve SecureNova request for user_124."

print()
print("Tampered message:")
print(tampered_message)

# Verify the tampered message using the original signature
try:
    public_key.verify(signature, tampered_message.encode("utf-8"))
    print()
    print("SECURITY ERROR: Tampered message was accepted!")
except InvalidSignature:
    print()
    print("SIGNATURE VERIFICATION FAILED")
    print("STATUS : REJECTED")
    print("REASON : Message was modified after signing.")
    print("DETAIL : Ed25519 signature does not match the tampered message.")

print("=" * 70)