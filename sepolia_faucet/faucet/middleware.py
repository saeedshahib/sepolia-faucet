import os
from django.core.cache import cache
from django.http import JsonResponse


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/faucet/fund/' and request.method == 'POST':
            ip_address = self.get_client_ip(request)
            wallet = request.POST.get('address')
            timeout = int(os.getenv('RATE_LIMIT_TIMEOUT', 60))

            ip_key = f"ip_{ip_address}"
            wallet_key = f"wallet_{wallet}"

            if cache.get(ip_key) or cache.get(wallet_key):
                return JsonResponse({"error": "Rate limit exceeded. Try again later."}, status=429)

            cache.set(ip_key, True, timeout)
            cache.set(wallet_key, True, timeout)

        return self.get_response(request)

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
