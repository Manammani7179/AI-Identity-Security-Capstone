import re

print("=" * 70)
print("SECURENOVA PROJECT 4 - JWT OUTPUT GUARDRAIL")
print("=" * 70)

# Simulated model response containing a JWT-shaped credential.
model_response = (
    "The authentication response contains this credential: "
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJzdWIiOiJ1c2VyMTIzIiwicm9sZSI6ImFnZW50In0."
    "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
)

# JWT-shaped string detection:
# header.payload.signature
jwt_pattern = r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"

redacted_response, count = re.subn(
    jwt_pattern,
    "[REDACTED]",
    model_response
)

print()
print("Original model response:")
print(model_response)

print()
print("JWT regex guardrail:")
print("JWT detected:", "YES" if count > 0 else "NO")
print("JWT matches :", count)

print()
print("Guardrail output:")
print(redacted_response)

print()
if count > 0 and "[REDACTED]" in redacted_response:
    print("STATUS : BLOCKED / REDACTED")
    print("REASON : JWT-shaped credential detected and removed")
else:
    print("STATUS : PASS")
    print("REASON : No JWT-shaped credential detected")

print("=" * 70)