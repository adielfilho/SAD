# topsis_cin/__init__.py

"""
Pacote TOPSIS: Implementação do método de decisão multi critério.

Uso:
    from topsis_cin import topsis_decision_support, Topsis

Versão:
    0.1.1
"""

__version__ = "0.1.1"

from .decision import TOPSIS as Topsis
from .main import topsis_decision_support

__all__ = [
    "Topsis",
    "topsis_decision_support"
]
