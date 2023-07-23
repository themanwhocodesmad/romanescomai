
class PrintRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Print the request method, path, and headers
        print(f"Request method: {request.method}")
        print(f"Request path: {request.path}")
        print("Request headers:")
        for header, value in request.META.items():
            if header.startswith("HTTP_"):
                print(f"  {header[5:]}: {value}")

        response = self.get_response(request)
        return response
