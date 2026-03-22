"""Input validation utilities for the CADence app."""

from typing import Dict, List, Tuple, Optional
from src.constants.clinical_constants import MIN_AGE, MAX_AGE, VALIDATED_AGE_RANGE
from src.localization import translator


def validate_age(age: int) -> Tuple[bool, Optional[str]]:
    if not MIN_AGE <= age <= MAX_AGE:
        return False, translator.t(
            "patient.basic_info.age_range_error",
            min_age=MIN_AGE,
            max_age=MAX_AGE
        )
    if not VALIDATED_AGE_RANGE[0] <= age <= VALIDATED_AGE_RANGE[1]:
        return True, translator.t(
            "patient.basic_info.age_validation_warning",
            min_age=VALIDATED_AGE_RANGE[0],
            max_age=VALIDATED_AGE_RANGE[1]
        )
    return True, None


def validate_risk_factors(risk_factors: Dict[str, bool]) -> Tuple[bool, Optional[str]]:
    required_factors = {
        "diabetes", "smoking", "hypertension",
        "dyslipidemia", "family_history"
    }
    if not all(factor in risk_factors for factor in required_factors):
        return False, "Missing required risk factors"
    if not all(isinstance(value, bool) for value in risk_factors.values()):
        return False, "Risk factor values must be boolean"
    return True, None


def validate_test_results(
    test_results: Dict[str, str],
    reference_standard: str
) -> Tuple[bool, Optional[str]]:
    valid_results = {"Positive", "Negative", ""}
    if not all(result in valid_results for result in test_results.values()):
        return False, "Invalid test result value"
    if reference_standard not in {"anatomical", "functional"}:
        return False, "Invalid reference standard"
    return True, None
