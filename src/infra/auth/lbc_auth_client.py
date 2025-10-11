from src.domain.ports.clients.lbc_auth_client import ILBCAuthClient

from src.domain.use_cases.models.auth.lbc_auth_input import LBCAuthInput
from src.domain.use_cases.models.auth.lbc_auth_output import LBCAuthOutput

from src.config.settings import AUTH_URL

from src.exceptions.api_types import AuthError, BadRequestError

import requests


class LBCAuthClient(ILBCAuthClient):

    def __init__(self) -> None:
        self.__auth_url = AUTH_URL


    def authenticate(self, lbc_auth_input: LBCAuthInput) -> LBCAuthOutput:
        # Implement the logic to interact with LBC Auth service and fetch user data
        # For example, make an HTTP request to the LBC Auth API with the provided token
        # and return the user data as a dictionary.

        headers = {'Content-Type': 'application/json'}

        response =  requests.post(f"{self.__auth_url}/login", headers=headers, auth=(lbc_auth_input.email, lbc_auth_input.password))

        status_code = response.status_code

        if status_code != 200:
            if status_code in [400, 401, 403]:
                raise AuthError("Credenciais inválidas.")

            else:
                raise Exception("Nao foi possível conectar a LBC.")

        auth_response = response.json()

        token_auth = auth_response.get("token", None)
        email = token_auth.get("email", None)

        if token_auth is None or email is None:
            raise BadRequestError("Resposta inválida da LBC Auth.")

        return LBCAuthOutput(
            lbc_auth_token=token_auth,
            email=email,
            name=auth_response.get("name", None),
            companies=auth_response.get("companies", []),
            ibms=auth_response.get("ibms", []),
            redes=auth_response.get("redes", [])
        )