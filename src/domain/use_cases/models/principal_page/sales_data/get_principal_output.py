import json
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any


@dataclass(slots=True)
class Variacao:
    abastecimentos: float
    custo: float
    lucro: float
    valor: float
    volume: float
    # por litro
    lpl: float
    ppl: float
    cpl: float
    # ticket medio
    ticketMedioValor: float
    ticketMedioVolume: float




@dataclass(slots=True)
class Venda:
    ibm: str
    data: str
    abastecimentos: int
    # totais
    lucro: float
    custo: float
    valor: float
    volume: float
    # por litro
    lpl: float
    ppl: float
    cpl: float
    # ticket medio
    ticketMedioValor: float
    ticketMedioVolume: float
    primeiro_abastecimento: Optional[str] = None
    ultimo_abastecimento: Optional[str] = None
    ticketMedioLucro: Optional[float] = 0.0
    ticketMedioCusto: Optional[float] = 0.0
    # primeiros e ultimos





@dataclass(slots=True)
class PostoResumo:
    ibm: str
    primeiro_abastecimento: str
    ultimo_abastecimento: str
    variacao: Variacao
    vendas: List[Venda] = field(default_factory=list)

    # Campos opcionais (podem vir vazios)
    cnpj: Optional[str] = ""
    nome: Optional[str] = ""
    rede: Optional[str] = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PostoResumo":
        return cls(
            ibm=data["ibm"],
            primeiro_abastecimento=data["primeiro_abastecimento"],
            ultimo_abastecimento=data["ultimo_abastecimento"],
            variacao=Variacao.from_dict(data["variacao"]),
            vendas=[Venda.from_dict(v) for v in data["vendas"]],
            cnpj=data.get("cnpj") or None,
            nome=data.get("nome") or None,
            rede=data.get("rede") or None,
        )


    @classmethod
    def from_json(cls, json_str: str) -> "PostoResumo":
        return cls.from_dict(json.loads(json_str))



@dataclass(slots=True)
class GetPrincipalOutput:
    """Lista agregada de vários postos."""
    postos: List[PostoResumo] = field(default_factory=list)