from __future__ import annotations
import json
from .decision import FTOPSISProcessor, trapezoidal_ftopsis_class, triangular_ftopsis_class
from typing import Union

def ftopsis_class_decision_support(data: Union[dict, str]):
  if type(data) == str: data = json.loads(data)
  fuzzy_type = FTOPSISProcessor.detect_fuzzy_type(data)
        
  if fuzzy_type == 'triangular': return triangular_ftopsis_class(data)
  return trapezoidal_ftopsis_class(data)
