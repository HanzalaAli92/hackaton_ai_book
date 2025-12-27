import time
from typing import Dict
from fastapi import HTTPException
from collections import defaultdict, deque
from ..config import settings


class RateLimiter:
    def __init__(self, requests: int = 100, window: int = 60):
        """
        Initialize rate limiter.

        Args:
            requests: Number of requests allowed per window
            window: Time window in seconds
        """
        self.requests = requests
        self.window = window
        self.requests_log: Dict[str, deque] = defaultdict(deque)

    def check_rate_limit(self, identifier: str = "default") -> bool:
        """
        Check if the identifier has exceeded the rate limit.

        Args:
            identifier: Unique identifier for the client (e.g., IP address, user ID)

        Returns:
            bool: True if within limit, False if exceeded
        """
        now = time.time()
        request_times = self.requests_log[identifier]

        # Remove requests outside the current window
        while request_times and now - request_times[0] > self.window:
            request_times.popleft()

        # Check if limit is exceeded
        if len(request_times) >= self.requests:
            return False

        # Add current request time
        request_times.append(now)
        return True


# Global rate limiter instance
rate_limiter = RateLimiter(
    requests=100,  # 100 requests per minute
    window=60      # 60 second window
)


def rate_limit_check(identifier: str = "default") -> None:
    """
    Check rate limit and raise HTTPException if exceeded.
    """
    if not rate_limiter.check_rate_limit(identifier):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please try again later."
        )