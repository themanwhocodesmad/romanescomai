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
            content_type = request.META.get("CONTENT_TYPE", "")
            if "application/json" in content_type:
                try:
                    body = json.loads(request.body)
                    print("Request Body:")
                    print(json.dumps(body, indent=4))
                except json.JSONDecodeError:
                    print("Could not parse request body as JSON")
                    print(request.body)
            elif "multipart/form-data" in content_type:
                print("Request contains multi-part form data (possibly file uploads).")
            else:
                print(f"Request content type: {content_type}")

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

        # If response content type is text-based, print the first 5 and last 5 lines
        if any(ct in response['Content-Type'] for ct in ['text', 'json', 'xml']):
            try:
                lines = response.content.decode('utf-8').splitlines()
                if len(lines) > 10:
                    for line in lines[:5]:
                        print(line)
                    print("...")
                    for line in lines[-5:]:
                        print(line)
                else:
                    for line in lines:
                        print(line)
            except UnicodeDecodeError:
                print("Could not decode response content as UTF-8")

        print(f"{'-' * 20} RESPONSE END {'-' * 20}\n")

        return response
