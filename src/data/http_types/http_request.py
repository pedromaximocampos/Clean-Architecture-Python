


class HttpRequest:
    def __init__(self, method: str, url: str, headers: dict = None, body: dict = None, query_params: dict = None, ipv4: str = None, path_params: dict = None):
        self.method = method
        self.url = url
        self.headers = headers if headers is not None else {}
        self.body = body
        self.query_params = query_params if query_params is not None else {}
        self.ipv4 = ipv4
        self.path_params = path_params if path_params is not None else {}


    def __repr__(self):
        return f"HttpRequest(method={self.method}, url={self.url}, headers={self.headers}, body={self.body})"