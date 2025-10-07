from flask import request as FlaskRequest
from typing import Callable
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse



def flask_adapter(request: FlaskRequest, controller_handle: Callable) -> HttpResponse:

    body = request.get_json(silent=True)

    http_request = HttpRequest(
        body=body,
        query_params=request.args.to_dict(),
        headers=dict(request.headers),
        method=request.method,
        url=request.url,
        path_params=request.view_args,
    )

    http_response: HttpResponse = controller_handle(http_request)

    return http_response