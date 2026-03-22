"""Clinical constants used in RF-CL calculations."""

# Base coefficients from Winther et al. 2020
CONST = -9.5260
SEX_COEF = 1.6128
AGE_COEF = 0.08440
TYPICAL_COEF = 2.7112
NON_ANGINAL_COEF = -0.4675

# Interaction coefficients
AGE_TYPICAL_COEF = -0.0187
AGE_RF_COEF = -0.0131
TYPICAL_RF_COEF = -0.2799
SEX_RF_COEF = -0.2091

# Test options
AVAILABLE_TESTS = [
    'ccta',
    'stress_ecg',
    'stress_echo',
    'spect',
    'pet',
    'stress_cmr'
]

FFR_VALIDATED_TESTS = [
    'spect',
    'pet',
    'stress_cmr'
]

# Risk factors
RISK_FACTORS = [
    "Diabetes",
    "Current/Past Smoking",
    "Dyslipidemia",
    "Hypertension",
    "Family History of Early CAD"
]

# Age validation
MIN_AGE = 18
MAX_AGE = 100
VALIDATED_AGE_RANGE = (30, 79)