import random
from typing import Dict, Deque
import time
from collections import deque
from colorama import Fore, Style, init

init(autoreset=True)


class SlidingWindowRateLimiter:
    """
    Sliding window rate limiter per user.

    window_size: length of the sliding window in seconds
    max_requests: maximum allowed requests per user within the window
    """

    def __init__(self, window_size: int = 10, max_requests: int = 1):
        self.window_size = window_size
        self.max_requests = max_requests
        self.user_requests: Dict[str, Deque[float]] = {}

    def _cleanup_window(self, user_id: str, current_time: float) -> None:
        """Remove timestamps that have fallen out of the current window."""
        if user_id in self.user_requests:
            while (
                self.user_requests[user_id]
                and self.user_requests[user_id][0] <= current_time - self.window_size
            ):
                self.user_requests[user_id].popleft()
            if not self.user_requests[user_id]:
                del self.user_requests[user_id]

    def can_send_message(self, user_id: str) -> bool:
        """Return True if user can send a message now."""
        current_time = time.time()
        self._cleanup_window(user_id, current_time)
        return len(self.user_requests.get(user_id, [])) < self.max_requests

    def record_message(self, user_id: str) -> bool:
        """
        Record a message for user if allowed.
        Returns True if accepted, False if rate-limited.
        """
        if self.can_send_message(user_id):
            if user_id not in self.user_requests:
                self.user_requests[user_id] = deque()
            self.user_requests[user_id].append(time.time())
            return True
        return False

    def time_until_next_allowed(self, user_id: str) -> float:
        """Seconds until the user is allowed again (0.0 if already allowed)."""
        if user_id not in self.user_requests or not self.user_requests[user_id]:
            return 0.0
        return max(
            0.0, self.window_size - (time.time() - self.user_requests[user_id][0])
        )


def test_rate_limiter() -> None:
    limiter = SlidingWindowRateLimiter(window_size=10, max_requests=1)

    print(Fore.CYAN + "\n=== Message Stream Simulation ===" + Style.RESET_ALL)
    print(" ")
    for message_id in range(1, 11):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(
            f"Message {message_id:2d} | User {user_id} | "
            f"{Fore.GREEN + '✓ accepted' if result else Fore.RED + f'× rate-limited (wait {wait_time:.1f}s)'}"
            + Style.RESET_ALL
        )
        time.sleep(random.uniform(0.1, 1.0))

    print(Fore.YELLOW + "\nWaiting 4 seconds..." + Style.RESET_ALL)
    time.sleep(4)

    print(Fore.CYAN + "\n=== New batch after waiting ===" + Style.RESET_ALL)
    print(" ")
    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(
            f"Message {message_id:2d} | User {user_id} | "
            f"{Fore.GREEN + '✓ accepted' if result else Fore.RED + f'× rate-limited (wait {wait_time:.1f}s)'}"
            + Style.RESET_ALL
        )
        time.sleep(random.uniform(0.1, 1.0))


if __name__ == "__main__":
    test_rate_limiter()
