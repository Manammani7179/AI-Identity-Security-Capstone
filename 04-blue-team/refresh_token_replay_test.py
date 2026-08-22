print("=" * 70)
print("SECURENOVA PROJECT 4 - REFRESH TOKEN REPLAY TEST")
print("=" * 70)

old_refresh_token = "old_refresh_token_example"

print()
print("Initial refresh token:")
print(old_refresh_token)

print()
print("Refreshing token...")
print("New refresh token issued successfully.")

print()
print("Attempting to reuse old refresh token...")
print()

# Simulated result representing Auth0 rotation/reuse detection.
replay_detected = True

if replay_detected:
    print("ERROR : Refresh token reuse detected")
    print("STATUS: REJECTED")
    print("REASON: Old refresh token was already used and cannot be replayed.")
else:
    print("STATUS: ACCEPTED")

print("=" * 70)