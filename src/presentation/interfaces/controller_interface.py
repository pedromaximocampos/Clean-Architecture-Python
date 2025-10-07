from abc import ABC, abstractmethod
from src.application.http_types import HttpRequest
from src.application.http_types import HttpResponse

class IControllerInterface(ABC):

    @abstractmethod
    def handle_request(self, request: HttpRequest) -> HttpResponse: pass