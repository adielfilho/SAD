from __future__ import annotations

import json
from typing import Dict, Any
from vikor_cin import vikor_decision_support
from topsis_cin import topsis_decision_support
from rim_cin import rim_decision_support
from wfrim_cin import wfrim_decision_support

def decision_support(input_data: Dict[str, Any]) -> Dict[str, Any]:
  method = input_data.get('method', '').lower()
  if method == 'vikor': return  vikor_decision_support(input_data)
  if method == 'topsis': return  json.loads(topsis_decision_support(input_data))
  if method == 'rim': return  json.loads(rim_decision_support(input_data))
  if method == 'wfrim': return  wfrim_decision_support(input_data)
  raise Exception(f"SAD CIN: method '{input_data.get('method', '')}' not recognized")
