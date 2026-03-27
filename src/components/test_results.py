"""Test results component."""

import streamlit as st
from typing import Dict, List, Optional
from src.constants.clinical_constants import AVAILABLE_TESTS, FFR_VALIDATED_TESTS
from src.state.session_state import SessionState
from src.localization import translator


def render_test_results() -> Optional[Dict[str, str]]:
    test_results = None

    with st.expander(translator.t("tests.title"), expanded=False):
        st.toggle(
            translator.t("tests.ffr_toggle"),
            help=translator.t("tests.ffr_help"),
            key="use_ffr"
        )

        col1, col2 = st.columns([0.30, 0.70])
        with col1:
            ccta_done = st.checkbox(
                translator.t("tests.names.ccta"),
                key="ccta_checkbox",
                value=st.session_state.completed_tests["ccta_done"],
                on_change=SessionState.update_test_completion,
                args=("ccta",),
                help=translator.t("tests.ccta.help")
            )

        if ccta_done:
            with col2:
                st.session_state.completed_tests["ccta_done"] = True
                st.toggle(
                    translator.t("tests.ccta.positive_label"),
                    key="ccta_result",
                    help=translator.t("tests.ccta.help"),
                    on_change=SessionState.update_ccta_result
                )

        _render_anatomical_tests(None)

        if st.session_state.use_ffr:
            any_ffr_test_selected = any(
                st.session_state.completed_tests.get(f"{test}_done", False)
                for test in FFR_VALIDATED_TESTS
            )
            if not any_ffr_test_selected:
                st.info(translator.t("tests.ffr_info"))

        test_results = _get_valid_test_results()

        if test_results:
            _render_test_results_metric(test_results)

    return test_results


def _render_anatomical_tests(columns) -> None:
    all_tests = [
        ("stress_ecg", translator.t("tests.names.stress_ecg"), translator.t("tests.high_risk_features.stress_ecg")),
        ("stress_echo", translator.t("tests.names.stress_echo"), translator.t("tests.high_risk_features.stress_echo")),
        ("spect", translator.t("tests.names.spect"), translator.t("tests.high_risk_features.spect")),
        ("pet", translator.t("tests.names.pet"), translator.t("tests.high_risk_features.pet")),
        ("stress_cmr", translator.t("tests.names.stress_cmr"), translator.t("tests.high_risk_features.stress_cmr"))
    ]

    if st.session_state.use_ffr:
        tests_to_show = [test for test in all_tests if test[0] in FFR_VALIDATED_TESTS]
    else:
        tests_to_show = all_tests

    for (test, label, help_text) in tests_to_show:
        _render_test_row(test, label, help_text)


def _render_test_input(test: str, label: str, help_text: str) -> None:
    _render_test_row(test, label, help_text)


def _render_test_row(test: str, label: str, help_text: str) -> None:
    col1, col2 = st.columns([0.40, 0.60])
    with col1:
        test_done = st.checkbox(
            label,
            key=f"{test}_checkbox",
            value=st.session_state.completed_tests[f"{test}_done"],
            on_change=SessionState.update_test_completion,
            args=(test,),
            help=help_text
        )
    with col2:
        if test_done:
            st.selectbox(
                translator.t("tests.result_label"),
                ["Positive", "Negative"],
                format_func=lambda x: translator.t("tests.result_positive") if x == "Positive" else translator.t("tests.result_negative"),
                key=f"{test}_key",
                on_change=SessionState.update_test_result,
                args=(test,),
                help=help_text,
                label_visibility="collapsed"
            )


def _get_valid_test_results() -> Optional[Dict[str, str]]:
    test_results = {
        k: v for k, v in st.session_state.test_results.items()
        if v and st.session_state.completed_tests.get(f"{k}_done", False)
    }

    if st.session_state.use_ffr:
        test_results = {
            k: v for k, v in test_results.items()
            if k in FFR_VALIDATED_TESTS or k == "ccta"
        }

    return test_results if test_results else None


def _render_test_results_metric(test_results: Dict[str, str]) -> None:
    from src.utils.calculations import adjust_likelihood_for_test_results

    is_adjusted = st.session_state.manual_rf_cl_adjustment is not None
    asterisk = "*" if is_adjusted else ""

    if "current_cacs_cl" in st.session_state:
        base_prob = st.session_state.current_cacs_cl
        label = translator.t("probability.titles.post_test_cacs_cl")
    else:
        if is_adjusted:
            base_prob = st.session_state.manual_rf_cl_adjustment
            label = translator.t("probability.titles.post_test_adj_rf_cl")
        else:
            base_prob = st.session_state.current_rf_cl
            label = translator.t("probability.titles.post_test_rf_cl")

    reference = "functional" if st.session_state.use_ffr else "anatomical"
    adjusted_prob = adjust_likelihood_for_test_results(base_prob, test_results, reference)

    st.metric(
        label,
        f"{adjusted_prob:.1f}%{asterisk}",
        delta=f"{adjusted_prob - base_prob:.1f}%",
        delta_color="inverse"
    )