"""
CADence FR: ESC 2024 CCS Guideline-Based Probability Calculator for Coronary Artery Disease
Main application entry point.
"""

import streamlit as st
from typing import Dict, Any
from src.localization import translator
from src.components.patient_characteristics import render_patient_characteristics
from src.components.risk_factors import render_risk_factors
from src.components.probability_adjustment import (
    render_probability_adjustment,
    render_cacs_section
)
from src.components.test_results import render_test_results
from src.components.recommendations import (
    get_recommendations,
    render_recommendations
)
from src.utils.calculations import (
    calculate_rf_cl,
    calculate_cacs_cl,
    adjust_likelihood_for_test_results
)
from src.state.session_state import SessionState


def setup_page():
    st.session_state.language = 'fr'
    translator.set_language('fr')

    # CSS pour le bouton reset compact
    st.markdown("""
    <style>
    div[data-testid="stButton"][id="reset-btn"] button,
    button[kind="secondary"]#reset-btn {
        padding: 0.25rem 0.6rem;
        font-size: 1.1rem;
        line-height: 1;
        min-height: unset;
        height: 2.1rem;
        width: auto;
    }
    .reset-row {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: -8px;
        margin-bottom: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title(translator.t("app.title"))

    st.markdown(f"""
    <p style='font-size: 20px; margin-top: -20px; font-style: italic; color: #666666;'>
    {translator.t("app.subtitle")}
    </p>
    """, unsafe_allow_html=True)


def render_footer():
    st.markdown("---")
    st.markdown(f"### {translator.t('footer.references_title')}")
    st.markdown("1. Vrints C, et al. 2024 ESC Guidelines for the management of chronic coronary syndromes. *Eur Heart J.* 2024.")
    st.markdown("2. Winther S, et al. Incorporating coronary calcification into pre-test assessment of the likelihood of coronary artery disease. *J Am Coll Cardiol.* 2020.")
    st.markdown("3. Knuuti J, et al. Meta-analysis of diagnostic test accuracy for non-invasive coronary artery disease testing. *Eur Heart J.* 2019.")
    st.warning(translator.t("footer.disclaimer"))
    st.markdown(f"""
    <div style='margin-top: 20px; padding: 15px; border-left: 3px solid #0066cc; background-color: #f8f9fa;'>
        <p style='font-size: 14px; color: #444444; margin: 0;'>
            {translator.t("footer.developed_by")}
        </p>
    </div>
    """, unsafe_allow_html=True)


def _on_score_change():
    if 'probability_score_selector' not in st.session_state or not st.session_state.probability_score_selector:
        st.session_state.selected_probability_score = st.session_state.default_score
    else:
        st.session_state.selected_probability_score = st.session_state.probability_score_selector


def _get_completed_tests_for_recommendation(selected_score: str) -> Dict[str, bool]:
    if selected_score in ["RF-CL", "**Adjusted** RF-CL"]:
        return {}
    if selected_score in ["CACS-CL", "**Adjusted** CACS-CL"]:
        return {k: v for k, v in st.session_state.completed_tests.items()
                if k == 'cacs_done'}
    return st.session_state.completed_tests


def main():
    # set_page_config doit être le tout premier appel Streamlit
    st.set_page_config(
        page_title="CADenceFR",
        page_icon="🫀"
    )

    # Bouton reset — réinitialise explicitement chaque widget par sa key
    if st.button("🔄 Nouveau cas", key="reset_btn", type="primary"):
        st.session_state.clear()
        # Widgets — patient
        st.session_state["age"] = 55
        st.session_state["gender"] = "Homme"
        st.session_state["symptom_type"] = None
        st.session_state["chest_pain_criteria"] = []
        st.session_state["exertional_dyspnea"] = False
        # Widgets — facteurs de risque
        st.session_state["risk_factors"] = []
        # Widgets — tests
        st.session_state["use_ffr"] = False
        st.session_state["ccta_checkbox"] = False
        st.session_state["ccta_result"] = False
        for test in ["stress_ecg", "stress_echo", "spect", "pet", "stress_cmr"]:
            st.session_state[f"{test}_checkbox"] = False
            if f"{test}_key" in st.session_state:
                del st.session_state[f"{test}_key"]
        # Widgets — ajustement
        st.session_state["manual_adjustment_value"] = 55.0
        st.session_state["cacs_score"] = None
        st.rerun()

    setup_page()
    SessionState.initialize_state()

    try:
        age, sex_binary, symptoms = render_patient_characteristics()

        st.session_state.current_age = age
        st.session_state.current_sex_binary = sex_binary
        st.session_state.current_symptoms = symptoms

        risk_factors = render_risk_factors()
        st.session_state.selected_risk_factors = risk_factors

        if all(x is not None for x in [age, sex_binary, symptoms]):
            base_rf_cl = calculate_rf_cl(age, sex_binary, symptoms, risk_factors)
            st.session_state.current_rf_cl = base_rf_cl

            st.markdown("---")
            st.subheader(translator.t("probability.titles.risk_assessment"))

            render_probability_adjustment(base_rf_cl)

            current_prob = base_rf_cl
            if st.session_state.manual_rf_cl_adjustment is not None:
                current_prob = st.session_state.manual_rf_cl_adjustment

            cacs = render_cacs_section(current_prob)

            if cacs is not None:
                current_prob = calculate_cacs_cl(current_prob, cacs)
                st.session_state.cacs_cl = current_prob

            test_results = render_test_results()

            final_prob = current_prob
            if test_results:
                final_prob = adjust_likelihood_for_test_results(
                    current_prob,
                    test_results,
                    'functional' if st.session_state.use_ffr else 'anatomical'
                )

            st.session_state.final_probability = final_prob

            available_scores = ["RF-CL"]

            if st.session_state.manual_rf_cl_adjustment is not None:
                available_scores.append("**Adjusted** RF-CL")

            if cacs is not None:
                if st.session_state.manual_rf_cl_adjustment is not None:
                    available_scores.append("**Adjusted** CACS-CL")
                else:
                    available_scores.append("CACS-CL")

            if test_results:
                if cacs is not None:
                    if st.session_state.manual_rf_cl_adjustment is not None:
                        available_scores.append("Post-Test **Adjusted** CACS-CL")
                    else:
                        available_scores.append("Post-Test CACS-CL")
                else:
                    if st.session_state.manual_rf_cl_adjustment is not None:
                        available_scores.append("Post-Test **Adjusted** RF-CL")
                    else:
                        available_scores.append("Post-Test RF-CL")

            st.markdown("---")
            st.subheader(translator.t("recommendations.title"))

            st.session_state.default_score = available_scores[-1]

            if 'selected_probability_score' not in st.session_state:
                st.session_state.selected_probability_score = st.session_state.default_score

            selected_score = st.segmented_control(
                translator.t("ui.segmented_control.select_score"),
                available_scores,
                selection_mode="single",
                default=st.session_state.default_score,
                key='probability_score_selector',
                on_change=_on_score_change
            )

            if selected_score is None:
                selected_score = st.session_state.default_score

            st.session_state.selected_probability_score = selected_score

            recommendation_prob = base_rf_cl
            if selected_score in ["CACS-CL", "**Adjusted** CACS-CL"] and cacs is not None:
                recommendation_prob = st.session_state.current_cacs_cl
            elif selected_score == "**Adjusted** RF-CL" and st.session_state.manual_rf_cl_adjustment is not None:
                recommendation_prob = st.session_state.manual_rf_cl_adjustment
            elif selected_score in ["Post-Test RF-CL", "Post-Test **Adjusted** RF-CL",
                                    "Post-Test CACS-CL", "Post-Test **Adjusted** CACS-CL"]:
                recommendation_prob = final_prob

            if recommendation_prob is None:
                recommendation_prob = base_rf_cl

            asterisk = "*" if "**Adjusted**" in selected_score else ""
            st.markdown(translator.t(
                "recommendations.based_on",
                score=selected_score,
                probability=f"{recommendation_prob:.1f}",
                asterisk=asterisk
            ))

            completed_tests = _get_completed_tests_for_recommendation(selected_score)
            recommendations = get_recommendations(recommendation_prob, completed_tests)
            render_recommendations(recommendations, recommendation_prob)

    except Exception as e:
        st.error(translator.t("errors.general_error", error=str(e)))
        import traceback
        st.error(traceback.format_exc())

    render_footer()


if __name__ == "__main__":
    main()