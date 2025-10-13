from src.domain.use_cases.models.principal_page import GetPrincipalOutput, PostoResumo



class IPrincipalDataCacheRepository:
    """Interface for principal data cache repository."""

    def get_principal_data(self, ibms: list[str], user_id: str) -> list[PostoResumo]:
        """Retrieve principal data from cache by principal ID."""
        raise NotImplementedError

    def set_principal_data(self, data: GetPrincipalOutput, user_id: str) -> None:
        """Store principal data in cache."""
        raise NotImplementedError

    def delete_principal_data(self, ibms: list[str], user_id: str) -> None:
        """Delete principal data from cache by principal ID."""
        raise NotImplementedError

    def check_exists(self, ibms: list[str], user_id: str) -> dict[str, bool]:
        """Check if principal data exists in cache by principal ID."""
        raise NotImplementedError