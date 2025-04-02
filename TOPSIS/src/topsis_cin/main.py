from __future__ import annotations
from typing import Dict, Union
from .decision import TOPSIS as Topsis

def topsis_decision_support(data: Union[str, Dict]):
  return Topsis(data).to_json()
