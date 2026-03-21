import time
from django.utils import timezone
from django.contrib.gis.geoip2 import GeoIP2

class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
        country = self._get_country(ip)

        start_time = time.time()
        response = self.get_response(request)
        duration = round((time.time() - start_time) * 1000, 2)  # only takes milliseconds

        log_line = (
            f"[{timezone.now().strftime('%Y-%m-%d %H:%M')}]\n"
            f"User: {request.user}\n"
            f"IP: {ip}\n"
            f"Country: {country}\n"
            f"Path: {request.path}\n"
            f"Method: {request.method}\n"
            f"Status: {response.status_code}\n"
            f"Duration: {duration}ms\n"
            f"Browser: {user_agent}\n"
            f"{'-' * 45}\n"
        )

        with open('requests.log', 'a') as f:
            f.write(log_line)

        return response

    def _get_country(self, ip):
        # If IP is missing or localhost, skip GeoIP lookup
        if not ip or ip == '127.0.0.1':
            return 'Local Network'
        try:
            g = GeoIP2() # Create GeoIP2 instance
            return g.country(ip)['country_name'] # Determine country name by IP address
        except Exception:
            return 'Unknown'
