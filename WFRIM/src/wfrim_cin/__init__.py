# wfrim_cin/__init__.py

"""
Pacote WFRIM: Implementação do método de decisão multi critério.

Uso:
    from wfrim_cin import wfriim_decision_support, Topsis

Versão:
    0.1.0
"""

__version__ = "0.1.0"

from .decision import WFRIM as Wfrim
from .main import wfrim_decision_support

__all__ = [
    "Wfrim",
    "wfrim_decision_support"
]
