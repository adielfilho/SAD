from __future__ import annotations

from typing import Dict, Any
from vikor_cin import vikor_decision_support

def decision_support(input_data: Dict[str, Any]) -> Dict[str, Any]:
  if input_data.get('method', '').lower() == 'vikor': return  vikor_decision_support(input_data)
  raise Exception(f"SAD CIN: method '{input_data.get('method', '')}' not recognized")
