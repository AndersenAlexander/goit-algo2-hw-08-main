# Homework on the topic "Flow Control Algorithms and Rate Limiting"

## Task 1. Implementing a Rate Limiter using the Sliding Window algorithm to limit the frequency of messages in a chat

A chat system needs to implement a mechanism for limiting the frequency of
messages from users to prevent spam. The implementation should use the Sliding
Window algorithm to precisely control time intervals, which allows you to track
the number of messages in a given time window and limit users from sending
messages if the limit is exceeded.

### Technical requirements

1. The implementation should use the Sliding Window algorithm to precisely
   control time intervals.

2. Basic system parameters: window size (window_size) — 10 seconds and the
   maximum number of messages in the window (max_requests) — 1.

3. Implement the SlidingWindowRateLimiter class.

4. Implement the class methods:

- `_cleanup_window` — to clear outdated requests from the window and update the
  active time window;
- `can_send_message` — to check whether a message can be sent in the current
  time window;
- `record_message` — to record a new message and update the user's history;
- `time_until_next_allowed` — to calculate the waiting time until the next
  message can be sent.

5. Data structure for storing message history — collections.deque.

### Acceptance criteria

📌Homework acceptance criteria are a prerequisite for the mentor's consideration
of the homework. If any of the criteria are not met, the mentor sends the
homework for revision without grading. If you "just need to clarify"😉 or you
get stuck at some stage of the execution — contact the mentor in Slack).

1. When trying to send a message before 10 seconds, the can_send_message method
   returns False.

2. When the first message from the user is sent, True is always returned.

3. When all messages are deleted from the user window, the user's record is
   deleted from the data structure.

4. The time_until_next_allowed method returns the waiting time in seconds.

5. The test function according to the example has been run and works as
   expected.

### Task Template

```python
import random from typing import Dict import time from collections import deque

class SlidingWindowRateLimiter: def **init**(self, window_size: int = 10,
max_requests: int = 1): pass def \_cleanup_window(self, user_id: str,
current_time: float) -> None: pass

def can_send_message(self, user_id: str) -> bool:
pass

def record_message(self, user_id: str) -> bool:
pass

def time_until_next_allowed(self, user_id: str) -> float:
pass

# Demonstration of work

def test_rate_limiter(): # Create a rate limiter: window 10 seconds, 1
message limiter = SlidingWindowRateLimiter(window_size=10, max_requests=1)

# Simulate a message flow from users (sequential IDs from 1 to 20)
print("\\n=== Simulate message flow ===")
for message_id in range(1, 11):
# Simulate different users (ID from 1 to 5)
user_id = message_id % 5 + 1

result = limiter.record_message(str(user_id))
wait_time = limiter.time_until_next_allowed(str(user_id))

print(f"Message {message_id:2d} | User {user_id} | "
f"{'✓' if result else f'× (wait {wait_time:.1f}s)'}")

# Small delay between messages for realism
# Random delay from 0.1 to 1 second
time.sleep(random.uniform(0.1, 1.0))

# Wait until the window clears
print("\\nWaiting for 4 seconds...")
time.sleep(4)

print("\\n=== New message series after waiting ===")
for message_id in range(11, 21):
user_id = message_id % 5 + 1
result = limiter.record_message(str(user_id))
wait_time = limiter.time_until_next_allowed(str(user_id))
print(f"Message {message_id:2d} | User {user_id} | "
f"{'✓' if result else f'× (waiting {wait_time:.1f}s)'}")
# Random delay from 0.1 to 1 second
time.sleep(random.uniform(0.1, 1.0))

if **name** == "**main**":
```

test_rate_limiter()

````

### Expected Output

```bash
=== Simulating message flow === Message 1 | User 2 | ✓
Message 2 | User 3 | ✓ Message 3 | User 4 | ✓ Message
4 | User 5 | ✓ Message 5 | User 1 | ✓ Message 6 |
User 2 | × (waiting 7.0s) Message 7 | User 3 | × (waiting
6.5s) Message 8 | User 4 | × (waiting
7.0s) Message 9 |
User 5 | × (waiting
6.8s) Message 10 | User 1 | ×
(waiting
7.4s)

Waiting 4 seconds...

=== New batch of messages after waiting === Message 11 | User 2 |
× (waiting 1.0s) Message 12 | User 3 | × (waiting 0.7s)
Message 13 | User 4 | × (waiting 0.4s) Message 14 |
User 5 | × (waiting 0.0s) Message 15 | User 1 | ✓
Message 16 | User 2 | ✓ Message 17 | User 3 | ✓
Message 18 | User 4 | ✓ Message 19 | User 5 | ✓
Message 20 | User 1 | × (waiting 7.0s)
````

## Task 2. Implementing Rate Limiter using Throttling algorithm to limit message frequency in chat

The chat system needs to implement a mechanism to limit the frequency of
messages from users to prevent spam. The implementation must use the Throttling
algorithm to control the time intervals between messages, which provides a fixed
waiting interval between user messages and limits the sending frequency if this
interval is not met.

### Specifications

1. The implementation must use the Throttling algorithm to control the time
   intervals.

2. Basic system parameter: minimum interval between messages (min_interval) — 10
   seconds.

3. Implement the ThrottlingRateLimiter class.

4. Implement the class methods:

- `can_send_message` — to check the possibility of sending a message based on
  the time of the last message;

- `record_message` — to record a new message with the time of the last message
  updated;

- `time_until_next_allowed` — to calculate the time until the next message can
  be sent.

5. Data structure for storing the time of the last message — Dict[str, float].

### Acceptance Criteria

1. When trying to send a message earlier than 10 seconds after the previous one,
   the can_send_message method returns False.

2. When the first message from the user is sent, True is always returned.

3. The time_until_next_allowed method returns the waiting time in seconds until
   the next allowed message.

4. The test function according to the example has been run and works as
   expected.

### Task template

```python
import time from typing import Dict import random

class ThrottlingRateLimiter: def **init**(self, min_interval: float = 10.0):
pass

def can_send_message(self, user_id: str) -> bool:
pass

def record_message(self, user_id: str) -> bool:
pass

def time_until_next_allowed(self, user_id: str) -> float:
pass

def test_throttling_limiter(): limiter =
ThrottlingRateLimiter(min_interval=10.0)

print("\\n=== Simulation of message flow (Throttling) ===")
for message_id in range(1, 11):
user_id = message_id % 5 + 1

result = limiter.record_message(str(user_id))
wait_time = limiter.time_until_next_allowed(str(user_id))

print(f"Message {message_id:2d} | User {user_id} | "
f"{'✓' if result else f'× (waiting {wait_time:.1f}s)'}")

# Random delay between messages
time.sleep(random.uniform(0.1, 1.0))

print("\\nWaiting for 10 seconds...")
time.sleep(10)

print("\\n=== New series of messages after waiting ===")
for message_id in range(11, 21):
user_id = message_id % 5 + 1
result = limiter.record_message(str(user_id))
wait_time = limiter.time_until_next_allowed(str(user_id))
print(f"Message {message_id:2d} | User {user_id} | "
f"{'✓' if result else f'× (waiting {wait_time:.1f}s)'}")
time.sleep(random.uniform(0.1, 1.0))

if **name** == "**main**": test_throttling_limiter()
```

### Expected Output

```bash
=== Simulating Message Flow (Throttling) === Message 1 | User 2
| ✓ Message 2 | User 3 | ✓ Message 3 | User 4 | ✓
Message 4 | User 5 | ✓ Message 5 | User 1 | ✓ Message
6 | User 2 | × (waiting 7.4s) Message 7 | User 3 | ×
(waiting 7.6s) Message 8 | User 4 | × (waiting 7.6s)
Message 9 | User 5 | × (waiting 7.6s) Message 10 | User
1 | × (waiting 7.4s)

Waiting 4 seconds...

=== New series of messages after waiting === Message 11 | User 2 |
× (waiting 0.7s) Message 12 | User 3 | × (waiting 0.6s)
Message 13 | User 4 | × (waiting 0.5s) Message 14 |
User 5 | ✓ Message 15 | User 1 | ✓ Message
```
