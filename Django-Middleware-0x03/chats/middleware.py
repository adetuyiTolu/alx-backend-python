# chats/middleware.py
from datetime import datetime, timedelta
from collections import defaultdict
from django.http import JsonResponse
from django.http import HttpResponseForbidden
import logging
from datetime import datetime


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Set up logging to a file
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(message)s',
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Allow access ONLY between 6PM (18) and 9PM (21)
        logging.info(f"hour is: {current_hour}")
        if current_hour < 16 or current_hour >= 21:
            return HttpResponseForbidden("Access to the messaging app is restricted during this time.")

        return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_logs = defaultdict(list)  # Tracks timestamps per IP

    def __call__(self, request):
        ip_address = self.get_client_ip(request)

        # Limit only applies to POST requests to messages endpoint
        if request.method == 'POST' and 'messages' in request.path:
            now = datetime.now()
            window_start = now - timedelta(minutes=1)

            # Clean up old timestamps
            self.message_logs[ip_address] = [
                ts for ts in self.message_logs[ip_address] if ts > window_start
            ]

            length = len(self.message_logs[ip_address])
            if length >= 5:
                return HttpResponseForbidden("Rate limit exceeded. Only 5 messages allowed per minute.")
            # Log this new message
            self.message_logs[ip_address].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '')


class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_roles = ['admin', 'moderator']

    def __call__(self, request):
        user = request.user

        if request.path.startswith('/admin/') and user.role not in self.allowed_roles:
            return HttpResponseForbidden("You don't have permission to access this page.")
        return self.get_response(request)

        return self.get_response(request)
