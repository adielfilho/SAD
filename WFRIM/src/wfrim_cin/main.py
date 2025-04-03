from __future__ import annotations
from .decision import WFRIM
from typing import Union

def wfrim_decision_support(data: Union[dict, str]):
  return WFRIM(data).run()
