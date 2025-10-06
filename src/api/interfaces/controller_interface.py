from abc import ABC, abstractmethod
from src.api.http_types.http_request import HttpRequest
from src.api.http_types.http_response import HttpResponse

class IControllerInterface(ABC):

    @abstractmethod
    def handle_request(self, request: HttpRequest) -> HttpResponse: pass