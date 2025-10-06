from abc import ABC, abstractmethod
from src.data.http_types.http_request import HttpRequest
from src.data.http_types.http_response import HttpResponse

class IControllerInterface(ABC):

    @abstractmethod
    def handle_request(self, request: HttpRequest) -> HttpResponse: pass