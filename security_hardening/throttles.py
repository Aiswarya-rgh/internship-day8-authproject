from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class LoginRateThrottle(AnonRateThrottle):
    scope = "login"


class AuthenticatedAPIRateThrottle(UserRateThrottle):
    scope = "authenticated"

class PremiumAPIRateThrottle(UserRateThrottle):
    scope = "premium"