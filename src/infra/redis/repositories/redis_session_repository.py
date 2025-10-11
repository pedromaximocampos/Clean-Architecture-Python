from dataclasses import asdict

from src.domain.entities.user_profile import UserProfile
from src.domain.use_cases.models.auth.session import Session
from src.domain.use_cases.models.user_profile.get_all_output import GetUserProfileOutput
from src.domain.ports.repositories.session_token_repository import ISessionTokenRepository
from src.exceptions.api_types import DatabaseError, NotFoundError

from src.infra.redis.connection import RedisProvider

import json

from redis import Redis


class RedisSessionRepository(ISessionTokenRepository):
    """Implementação do repositório de SessionToken usando Redis."""


    def __init__(self, redis_client: RedisProvider) -> None:
        self.redis_client: Redis = redis_client.client()


    def save(self, session: Session, token_refresh: str) -> None:
        """Insere token de sessão para o usuário."""

        redis_connection = self.redis_client.ping()

        if not redis_connection:
            raise DatabaseError("Não foi possível conectar ao Redis.")

        redis_pipeline = self.redis_client.pipeline()

        redis_pipeline.hset(token_refresh, session.id)
        redis_pipeline.hset(token_refresh, session.name)
        redis_pipeline.hset(token_refresh, session.email)
        redis_pipeline.hset(token_refresh, json.dumps(session.ibms))
        redis_pipeline.hset(token_refresh, json.dumps(session.companies))
        redis_pipeline.hset(token_refresh, json.dumps(session.redes))
        redis_pipeline.hset(token_refresh, json.dumps(asdict(session.user_profile)))

        tempo_de_expiracao = 60 * 60 * 24 * 30  # 30 dias em segundos
        tempo_de_expiracao += 120  # Adiciona 2 minutos extras para garantir que o token não expire exatamente no momento da verificação

        redis_pipeline.expire(token_refresh, tempo_de_expiracao)

        redis_pipeline.execute()


    def exists(self, token_refresh: str) -> bool:
        """Verifica se o token de sessão existe para o usuário."""
        return self.redis_client.exists(token_refresh) == 1


    def delete(self, token_refresh: str) -> None:
        """Deleta o token de sessão do usuário."""
        self.redis_client.delete(token_refresh)


    def get_user_info(self, token_refresh: str) -> Session:
        """Retorna as informações da sessão associada ao token de sessão."""
        user_data = self.redis_client.hgetall(token_refresh)

        if not user_data:
            raise NotFoundError("Sessão não encontrada.")

        user_profile = json.loads(user_data.get("user_profile"))


        schemed_user_profile = UserProfile(
            id = user_profile.get("id"),
            email = user_profile.get("email"),
            authorized_at=user_profile.get("authorized_at"),
            authorized_by=user_profile.get("authorized_by"),
            can_use_ai_agent=user_profile.get("can_use_ai_agent"),
            can_access_sensitive_information=user_profile.get("can_access_sensitive_information"),
            saved_in_big_query=user_profile.get("saved_in_big_query", False),
            updated_at=user_profile.get("updated_at", None),
            updated_by=user_profile.get("updated_by", None),
            deleted_at= None,
            deleted_by= None
        )


        return Session(
            id = user_data.get("id"),
            name=user_data.get("name"),
            email=user_data.get("email"),
            ibms=json.loads(user_data.get("ibms")),
            companies=json.loads(user_data.get("companies")),
            redes=json.loads(user_data.get("redes")),
            user_profile=schemed_user_profile,
            expires_in=self.redis_client.ttl(token_refresh)
        )

