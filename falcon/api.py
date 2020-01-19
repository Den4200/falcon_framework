import inspect
from parse import parse
from webob import Request, Response


class Api:

    def __init__(self):
        self.routes = dict()

    def __call__(self, environ, start_response):
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def route(self, path):
        if path in self.routes:
            raise AssertionError(f'Route {path} already exists.')

        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)

            if parse_result is not None:
                return handler, parse_result.named

        return None, None

    def handle_request(self, request):
        response = Response()
        handler, kwargs = self.find_handler(
            request_path=request.path
        )
        
        if handler is not None:

            if inspect.isclass(handler):
                handler = getattr(
                    handler(), request.method.lower()
                )

                if handler is None:
                    raise AttributeError('Method not allowed', request.method)

            handler(request, response, **kwargs)

        else:
            self.default_response(response)

        return response

    def default_response(self, response):
        response.status_code = 404
        response.text = 'Not found.'
