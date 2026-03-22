"""Utility functions for CAD probability calculations."""

import numpy as np
from typing import Dict, Union, Tuple

from src.constants.clinical_constants import (
    CONST, SEX_COEF, AGE_COEF, TYPICAL_COEF, NON_ANGINAL_COEF,
    AGE_TYPICAL_COEF, AGE_RF_COEF, TYPICAL_RF_COEF, SEX_RF_COEF
)
from src.constants.likelihood_ratios import (
    ANATOMICAL_POSITIVE_LR, ANATOMICAL_NEGATIVE_LR,
    FUNCTIONAL_POSITIVE_LR, FUNCTIONAL_NEGATIVE_LR
)

def calculate_rf_cl(
    age: int,
    sex_binary: int,
    symptoms: str,
    risk_factors: Dict[str, bool]
) -> float:
    """
    Calculate Risk Factor-weighted Clinical Likelihood using formula from Winther et al. 2020
    
    Args:
        age: Patient age
        sex_binary: 1 for male, 0 for female
        symptoms: One of 'typical', 'atypical', 'non_anginal'
        risk_factors: Dictionary of risk factors and their presence
        
    Returns:
        float: Probability as percentage (0-100)
    """
    # Convert symptoms to binary flags
    symp_typical = 1 if symptoms == "typical" else 0
    symp_non_anginal = 1 if symptoms == "non_anginal" else 0
    
    # Count number of risk factors present (0-5)
    rf_count = sum(1 for rf, has_rf in risk_factors.items() if has_rf)
    
    # Convert to nb_rf categories as per paper: 0-1, 2-3, 4-5
    if rf_count <= 1:
        nb_rf = 1
    elif rf_count <= 3:
        nb_rf = 2
    else:
        nb_rf = 3
    
    # Calculate logit
    logit = (CONST + 
             (SEX_COEF * sex_binary) +
             (AGE_COEF * age) +
             (TYPICAL_COEF * symp_typical) +
             (NON_ANGINAL_COEF * symp_non_anginal) +
             (1.4940 * nb_rf) +  # Risk factor coefficient from paper
             (AGE_TYPICAL_COEF * age * symp_typical) +
             (AGE_RF_COEF * age * nb_rf) +
             (TYPICAL_RF_COEF * symp_typical * nb_rf) +
             (SEX_RF_COEF * sex_binary * nb_rf))
             
    # Convert to probability using logistic function
    probability = 1 / (1 + np.exp(-logit))
    
    return min(probability * 100, 100)  # Convert to percentage and cap at 100

def calculate_cacs_cl(rf_cl: float, cacs: int) -> float:
    """
    Calculate CACS-weighted Clinical Likelihood
    
    Args:
        rf_cl: Risk Factor-weighted Clinical Likelihood as percentage
        cacs: Coronary Artery Calcium Score (Agatston)
        
    Returns:
        float: Probability as percentage (0-100)
    """
    # Convert percentages to proportions
    rf_ptp = rf_cl / 100
    
    # Initialize CACS category flags
    cacs_1_9 = 1 if 1 <= cacs <= 9 else 0
    cacs_10_99 = 1 if 10 <= cacs <= 99 else 0
    cacs_100_399 = 1 if 100 <= cacs <= 399 else 0
    cacs_400_999 = 1 if 400 <= cacs <= 999 else 0
    cacs_1000 = 1 if cacs >= 1000 else 0
    
    probability = (
        0.0013 + 
        (rf_ptp * 0.2021) + 
        (cacs_1_9 * 0.0082) + 
        (cacs_10_99 * 0.0238) + 
        (cacs_100_399 * 0.1131) + 
        (cacs_400_999 * 0.2306) + 
        (cacs_1000 * 0.4040) + 
        (rf_ptp * cacs_1_9 * 0.1311) + 
        (rf_ptp * cacs_10_99 * 0.2909) + 
        (rf_ptp * cacs_100_399 * 0.4077) + 
        (rf_ptp * cacs_400_999 * 0.4658) + 
        (rf_ptp * cacs_1000 * 0.4489)
    )
    
    return min(probability * 100, 100)

def adjust_likelihood_for_test_results(
    base_probability: float,
    test_results: Dict[str, str],
    reference_standard: str = 'anatomical'
) -> float:
    """
    Adjust likelihood based on test results using likelihood ratios
    
    Args:
        base_probability: Initial probability as percentage
        test_results: Dictionary of test names and their results ('Positive'/'Negative')
        reference_standard: 'anatomical' or 'functional'
        
    Returns:
        float: Adjusted probability as percentage (0-100)
    """
    positive_lr = FUNCTIONAL_POSITIVE_LR if reference_standard == 'functional' else ANATOMICAL_POSITIVE_LR
    negative_lr = FUNCTIONAL_NEGATIVE_LR if reference_standard == 'functional' else ANATOMICAL_NEGATIVE_LR
    
    odds = base_probability / (100 - base_probability)
    
    for test, result in test_results.items():
        if result == 'Positive':
            odds *= positive_lr[test]
        elif result == 'Negative':
            odds *= negative_lr[test]
    
    return min((odds / (1 + odds)) * 100, 100)