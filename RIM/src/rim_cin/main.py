from __future__ import annotations
from .decision import RIM as Rim

def rim_decision_support(data: dict):
  return Rim([], [], {}, {}, {}, {}).process_json(data)
