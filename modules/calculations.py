"""
Cálculos clínicos automáticos
"""
import math
from typing import Optional

def calculate_bsa(height_cm: float, weight_kg: float) -> Optional[float]:
    """
    Calcula BSA usando fórmula de Du Bois
    BSA (m²) = 0.007184 × altura^0.725 × peso^0.425
    """
    if not height_cm or not weight_kg:
        return None
    
    if height_cm < 50 or height_cm > 250:
        return None
    
    if weight_kg < 20 or weight_kg > 300:
        return None
    
    bsa = 0.007184 * (height_cm ** 0.725) * (weight_kg ** 0.425)
    return round(bsa, 2)


def calculate_creatinine_clearance(
    age: int, 
    weight_kg: float, 
    creatinine_mg_dl: float, 
    sex: str
) -> Optional[float]:
    """
    Calcula CrCl usando Cockcroft-Gault
    """
    if not all([age, weight_kg, creatinine_mg_dl, sex]):
        return None
    
    if age < 18 or age > 120:
        return None
    
    crcl = ((140 - age) * weight_kg) / (72 * creatinine_mg_dl)
    
    if sex.upper() == 'F':
        crcl *= 0.85
    
    return round(crcl, 1)


def calculate_nlr(neutrophils: float, lymphocytes: float) -> Optional[float]:
    """Calcula Neutrophil-to-Lymphocyte Ratio"""
    if not neutrophils or not lymphocytes or lymphocytes == 0:
        return None
    
    nlr = neutrophils / lymphocytes
    return round(nlr, 2)
