from datetime import datetime, timedelta

print("=" * 70)
print("SECURENOVA PROJECT 4 - ANOMALY DETECTION")
print("=" * 70)

identity = "agent-securnova-01"


# ==========================================================
# SCENARIO 1 — LLM API CALL VOLUME SPIKE
# More than 20 requests within 60 seconds
# ==========================================================

request_times = [
    datetime.now() - timedelta(seconds=i)
    for i in range(21)
]

if len(request_times) > 20:
    print()
    print("ALERT")
    print("Timestamp :", datetime.now().isoformat(timespec="seconds"))
    print("Identity  :", identity)
    print("Event     : LLM API call volume spike")
    print("Details   :", len(request_times),
          "requests detected within 60 seconds")
    print("Threshold : More than 20 requests / 60 seconds")
    print("STATUS    : ALERT FIRED")


# ==========================================================
# SCENARIO 2 — SCOPE CHANGE
# ==========================================================

previous_scope = "read:books"
current_scope = "read:books write:admin"

if current_scope != previous_scope:
    print()
    print("ALERT")
    print("Timestamp :", datetime.now().isoformat(timespec="seconds"))
    print("Identity  :", identity)
    print("Event     : Agent scope change")
    print("Previous  :", previous_scope)
    print("Current   :", current_scope)
    print("STATUS    : ALERT FIRED")


# ==========================================================
# SCENARIO 3 — TOKEN REUSE AFTER EXPIRY
# ==========================================================

token_expired = True
token_reused = True

if token_expired and token_reused:
    print()
    print("ALERT")
    print("Timestamp :", datetime.now().isoformat(timespec="seconds"))
    print("Identity  :", identity)
    print("Event     : Token reuse after expiry")
    print("Details   : Expired authentication token was reused")
    print("STATUS    : ALERT FIRED")


print()
print("=" * 70)
print("ANOMALY DETECTION TEST COMPLETE")
print("=" * 70)