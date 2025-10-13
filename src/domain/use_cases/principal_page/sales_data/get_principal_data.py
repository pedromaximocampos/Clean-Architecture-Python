from src.domain.use_cases.models.principal_page import GetPrincipalInput, GetPrincipalOutput

from abc import ABC, abstractmethod



class IGetPrincipalDataUseCase(ABC):
    @abstractmethod
    def execute(self, input_data: GetPrincipalInput) -> GetPrincipalOutput:
        pass
