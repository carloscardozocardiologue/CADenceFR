"""Constants for likelihood ratios used in CAD probability calculations."""

ANATOMICAL_POSITIVE_LR = {
    'stress_ecg': 1.53,
    'stress_echo': 4.67,
    'spect': 2.88,
    'pet': 5.87,
    'stress_cmr': 4.54,
    'ccta': 4.44
}

ANATOMICAL_NEGATIVE_LR = {
    'stress_ecg': 0.68,
    'stress_echo': 0.18, 
    'spect': 0.19,
    'pet': 0.12,
    'stress_cmr': 0.13,
    'ccta': 0.04
}

FUNCTIONAL_POSITIVE_LR = {
    'spect': 4.21,
    'pet': 6.04,
    'stress_cmr': 7.10,
    'ccta': 1.97
}

FUNCTIONAL_NEGATIVE_LR = {
    'spect': 0.33,
    'pet': 0.13,
    'stress_cmr': 0.13,
    'ccta': 0.13
}