"""Patient characteristics component."""

import streamlit as st
from typing import Tuple
from src.utils.validators import validate_age
from src.localization import translator


def _initialize_state():
    if "gender" not in st.session_state:
        st.session_state.gender = translator.t("ui.labels.male")
    if "symptom_type_state" not in st.session_state:
        st.session_state.symptom_type_state = None
    if "chest_pain_criteria_state" not in st.session_state:
        st.session_state.chest_pain_criteria_state = []
    if "dyspnea_state" not in st.session_state:
        st.session_state.dyspnea_state = False
    if "needs_recalculation" not in st.session_state:
        st.session_state.needs_recalculation = False


def _handle_age_change():
    st.session_state.needs_recalculation = True
    if "manual_rf_cl_adjustment" in st.session_state:
        st.session_state.manual_rf_cl_adjustment = None


def _handle_gender_change():
    st.session_state.needs_recalculation = True
    if "manual_rf_cl_adjustment" in st.session_state:
        st.session_state.manual_rf_cl_adjustment = None


def _handle_symptom_type_change():
    st.session_state.needs_recalculation = True
    if "manual_rf_cl_adjustment" in st.session_state:
        st.session_state.manual_rf_cl_adjustment = None
    if "symptom_type" in st.session_state:
        st.session_state.symptom_type_state = (
            st.session_state.symptom_type or
            translator.t("patient.symptoms.chest_pain")
        )


def _handle_chest_pain_criteria_change():
    st.session_state.needs_recalculation = True
    if "manual_rf_cl_adjustment" in st.session_state:
        st.session_state.manual_rf_cl_adjustment = None
    if "chest_pain_criteria" in st.session_state:
        st.session_state.chest_pain_criteria_state = st.session_state.chest_pain_criteria


def _handle_dyspnea_change():
    st.session_state.needs_recalculation = True
    if "manual_rf_cl_adjustment" in st.session_state:
        st.session_state.manual_rf_cl_adjustment = None
    if "exertional_dyspnea" in st.session_state:
        st.session_state.dyspnea_state = st.session_state.exertional_dyspnea


def render_patient_characteristics() -> Tuple[int, int, str]:
    _initialize_state()

    st.subheader(translator.t("patient.title"))

    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        age = st.slider(
            translator.t("ui.labels.age"),
            min_value=18,
            max_value=100,
            value=55,
            step=1,
            key="age",
            help=translator.t("patient.age_help"),
            on_change=_handle_age_change
        )
    with col2:
        sex = st.radio(
            translator.t("ui.labels.gender"),
            options=[
                translator.t("ui.labels.male"),
                translator.t("ui.labels.female")
            ],
            horizontal=True,
            key="gender",
            on_change=_handle_gender_change
        )

    is_valid, warning = validate_age(age)
    if warning:
        st.warning(f"⚠️ {warning}")

    symptom_type = st.pills(
        translator.t("patient.symptoms.title"),
        [
            translator.t("patient.symptoms.chest_pain"),
            translator.t("patient.symptoms.dyspnea")
        ],
        selection_mode="single",
        default=st.session_state.symptom_type_state,
        key="symptom_type",
        on_change=_handle_symptom_type_change
    )

    symptom_type = symptom_type or translator.t("patient.symptoms.chest_pain")
    symptoms = "non_anginal"

    if symptom_type == translator.t("patient.symptoms.chest_pain"):
        symptoms_criteria = st.pills(
            translator.t("patient.symptoms.classification_title"),
            [
                translator.t("patient.symptoms.substernal"),
                translator.t("patient.symptoms.provoked"),
                translator.t("patient.symptoms.relieved")
            ],
            selection_mode="multi",
            default=st.session_state.chest_pain_criteria_state,
            key="chest_pain_criteria",
            on_change=_handle_chest_pain_criteria_change
        )

        num_criteria = len(symptoms_criteria)

        if num_criteria == 3:
            symptoms = "typical"
            st.error(translator.t("patient.symptoms.typical_angina"))
        elif num_criteria == 2:
            symptoms = "atypical"
            st.warning(translator.t("patient.symptoms.atypical_angina"))
        else:
            symptoms = "non_anginal"
            st.success(translator.t("patient.symptoms.non_anginal"))

    elif symptom_type == translator.t("patient.symptoms.dyspnea"):
        exertional_dyspnea = st.toggle(
            translator.t("patient.symptoms.dyspnea_description"),
            value=st.session_state.dyspnea_state,
            key="exertional_dyspnea",
            help=translator.t("patient.symptoms.dyspnea_help"),
            on_change=_handle_dyspnea_change
        )

        if exertional_dyspnea:
            symptoms = "atypical"
        else:
            symptoms = "non_anginal"

    sex_binary = 1 if sex == translator.t("ui.labels.male") else 0

    st.session_state.current_age = age
    st.session_state.current_sex_binary = sex_binary
    st.session_state.current_symptoms = symptoms

    return age, sex_binary, symptoms
