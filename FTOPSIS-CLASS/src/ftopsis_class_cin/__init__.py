# ftopsis_class_cin/__init__.py

"""
Pacote FTOPSIS-CLASS: Implementação do método de decisão multi critério.

Uso:
    from ftopsis_class_cin import ftopsis_class_cin_decision_support, trapezoidal_ftopsis_class, triangular_ftopsis_class, FtopsisProcessor

Versão:
    0.1.1
"""

__version__ = "0.1.1"

from .decision import FTOPSISProcessor as FtopsisProcessor, trapezoidal_ftopsis_class, triangular_ftopsis_class
from .main import ftopsis_class_decision_support

__all__ = [
    "FtopsisProcessor",
    "trapezoidal_ftopsis_class",
    "triangular_ftopsis_class",
    "ftopsis_class_decision_support"
]
