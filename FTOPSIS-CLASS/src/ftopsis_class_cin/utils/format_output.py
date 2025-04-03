import pandas as pd
from typing import Dict, Any

def format_to_json(resultado: pd.DataFrame, classification_col: str = 'Classificação') -> Dict[str, Any]:
    return {
        "results": {
            supplier: {
                "scores": {
                    col: float(resultado.at[supplier, col])
                    for col in resultado.columns 
                    if col != classification_col
                },
                "classification": resultado.at[supplier, classification_col]
            }
            for supplier in resultado.index
        }
    }