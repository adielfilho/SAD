# rim_cin/__init__.py

"""
Pacote RIM: Implementação do método de decisão multi critério.

Uso:
    from rim_cin import rim_decision_support, Rim

Versão:
    0.1.0
"""

__version__ = "0.1.0"

from .decision import RIM as Rim
from .main import rim_decision_support

__all__ = [
    "Rim",
    "rim_decision_support"
]
