import json


class PrintRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Print the request method and path
        print(f"\n{'-' * 20} REQUEST START {'-' * 20}")
        print(f"Request method: {request.method}")
        print(f"Request path: {request.path}")

        # Print request user if authenticated
        if hasattr(request, 'user') and request.user.is_authenticated:
            print(f"Authenticated user: {request.user.username}")

        # Print request query parameters
        print("Query parameters:")
        for key, value in request.GET.items():
            print(f"  {key}: {value}")

        # Print request body data for POST, PUT methods
        if request.method in ["POST", "PUT"]:
            try:
                body = json.loads(request.body)
                print("Request Body:")
                print(json.dumps(body, indent=4))
            except json.JSONDecodeError:
                print("Could not parse request body as JSON")
                print(request.body)

        # Print request headers
        print("Request headers:")
        for header, value in request.META.items():
            if header.startswith("HTTP_"):
                print(f"  {header[5:].replace('_', '-').title()}: {value}")

        response = self.get_response(request)

        # Optionally, print some response details
        print(f"\n{'-' * 20} RESPONSE START {'-' * 20}")
        print(f"Response status code: {response.status_code}")
        print(f"Response content type: {response['Content-Type']}")
        print(f"{'-' * 20} RESPONSE END {'-' * 20}\n")

        return response
