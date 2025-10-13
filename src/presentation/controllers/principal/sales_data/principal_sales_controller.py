from src.domain.use_cases.models.principal_page import GetPrincipalOutput, PostoResumo
from src.presentation.http_types import HttpRequest, HttpResponse
from src.presentation.interfaces import IControllerInterface
from src.domain.use_cases.principal_page.sales_data.get_principal_data import IGetPrincipalDataUseCase, GetPrincipalInput

from src.utils.utils import UtilsMethods

class PrincipalSalesController(IControllerInterface):
    def __init__(self, get_principal_data_use_case: IGetPrincipalDataUseCase):
        self.get_principal_data_use_case = get_principal_data_use_case

    def handle_request(self, request: HttpRequest) -> HttpResponse:
        ibms =  request.body.get("ibm")
        date = request.body.get("data")
        rede = request.body.get("rede")

        date_time = UtilsMethods.convert_date_from_isoformat(date)

        check_data = UtilsMethods.check_data(date_time)

        input_data = GetPrincipalInput(
            ibms=ibms,
            date=check_data,
            rede=rede
        )
        output_data: GetPrincipalOutput = self.get_principal_data_use_case.execute(input_data)


        return HttpResponse(
            status_code=200,
            body={
                "data": [posto.to_dict() for posto in output_data.postos]
            }
        )