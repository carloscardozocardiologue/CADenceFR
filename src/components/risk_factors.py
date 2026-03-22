"""Risk factors component for CADence."""

import streamlit as st
from typing import Dict
from src.localization import translator


def _initialize_state():
    if "risk_factors_state" not in st.session_state:
        st.session_state.risk_factors_state = []
    if "needs_recalculation" not in st.session_state:
        st.session_state.needs_recalculation = False


def _handle_risk_change():
    st.session_state.needs_recalculation = True
    if "manual_rf_cl_adjustment" in st.session_state:
        st.session_state.manual_rf_cl_adjustment = None
    if "risk_factors" in st.session_state:
        st.session_state.risk_factors_state = st.session_state.risk_factors


def render_risk_factors() -> Dict[str, bool]:
    _initialize_state()

    st.subheader(translator.t("risk_factors.title"))

    localized_risk_factors = [
        translator.t("risk_factors.diabetes"),
        translator.t("risk_factors.smoking"),
        translator.t("risk_factors.hypertension"),
        translator.t("risk_factors.dyslipidemia"),
        translator.t("risk_factors.family_history")
    ]

    selected_risks = st.pills(
        label=translator.t("risk_factors.title"),
        options=localized_risk_factors,
        selection_mode="multi",
        default=st.session_state.risk_factors_state,
        key="risk_factors",
        on_change=_handle_risk_change,
        label_visibility="collapsed",
        help=translator.t("risk_factors.pill_help")
    )

    with st.expander(
        translator.t("risk_factors.definitions_title"),
        expanded=False
    ):
        definition_keys = {
            translator.t("risk_factors.diabetes"): "diabetes",
            translator.t("risk_factors.smoking"): "smoking",
            translator.t("risk_factors.hypertension"): "hypertension",
            translator.t("risk_factors.dyslipidemia"): "dyslipidemia",
            translator.t("risk_factors.family_history"): "family_history"
        }
        for label, key in definition_keys.items():
            st.markdown(f"### {label}")
            st.markdown(translator.t(f"risk_factors.definitions.{key}"))

    risk_factors = {
        "diabetes": translator.t("risk_factors.diabetes") in selected_risks,
        "smoking": translator.t("risk_factors.smoking") in selected_risks,
        "hypertension": translator.t("risk_factors.hypertension") in selected_risks,
        "dyslipidemia": translator.t("risk_factors.dyslipidemia") in selected_risks,
        "family_history": translator.t("risk_factors.family_history") in selected_risks
    }

    return risk_factors
