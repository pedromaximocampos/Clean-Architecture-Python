from abc import ABC, abstractmethod
from src.domain.use_cases.models.principal_page import Venda

class IDailyConsolidationRepository(ABC):
    """Contrato do repositório de consolidação diária."""

    @abstractmethod
    def get_consolidation_by_date(self, date: str, ibms: list[str]) -> list[Venda]:
        """Obtém a consolidação diária por data."""
        raise NotImplementedError

    @abstractmethod
    def save_consolidation(self, venda: Venda) -> None:
        """Salva a consolidação diária."""
        raise NotImplementedError

    @abstractmethod
    def delete_d2_to_d0_consolidations(self) -> None:
        """Deleta as consolidações dos últimos 3 dias (D-2, D-1, D0)."""
        raise NotImplementedError

    @abstractmethod
    def delete_old_consolidations(self) -> None:
        """Deleta as consolidações anteriores a uma data específica."""
        raise NotImplementedError

    @abstractmethod
    def consolidate_today_and_yesterday(self) -> None:
        """Realiza a consolidação dos dados de hoje e ontem."""
        raise NotImplementedError