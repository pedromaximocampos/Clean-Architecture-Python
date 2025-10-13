from src.domain.use_cases.models.principal_page import GetPrincipalOutput, PostoResumo



class IPrincipalDataCacheRepository:
    """Interface for principal data cache repository."""

    def get_principal_data(self, ibms: list[str], user_id: str) -> list[PostoResumo]:
        """Retrieve principal data from cache by principal ID."""
        raise NotImplementedError

    def set_principal_data(self, data: list[PostoResumo], user_id: str) -> None:
        """Store principal data in cache."""
        raise NotImplementedError


    def clear_cache(self, user_id: str) -> None:
        """Clear all principal data from cache for a specific user."""
        raise NotImplementedError