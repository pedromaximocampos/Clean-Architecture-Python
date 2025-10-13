from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Tuple

from src.domain.use_cases.models.principal_page import Venda

class ISuppliesRepository(ABC):
    """Contrato do repositório de suprimentos."""



    @abstractmethod
    def get_supplies_by_ibms(self, ibms: list[str], date: datetime) -> Dict[str, Tuple[Venda, Venda]]:
        """Recupera um suprimento pelo seu ID."""
        raise NotImplementedError


    @abstractmethod
    def find_first_and_last_sale_date(self) -> tuple[datetime, datetime]:
        """Recupera a primeira e a última data de venda registrada."""
        raise NotImplementedError