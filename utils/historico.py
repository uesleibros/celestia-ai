from typing import Dict, List
from structures.text_models import DEFAULT_RP_MODEL

historico: Dict[int, List[Dict[str, str]]] = {}
rp_historico: List[Dict[str, str]] = []
memorias: List[Dict[str, str]] = []
system_context: str = None
rp_modelo: str = DEFAULT_RP_MODEL