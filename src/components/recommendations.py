"""Recommendations component for CADence."""

import streamlit as st
from typing import Dict, List, TypedDict, Optional
from src.localization import translator


class Recommendation(TypedDict):
    test: str
    reason: str
    performance: str
    recommendation_quote: str
    class_: Optional[str]
    level: Optional[str]


def get_recommendations(
    adjusted_ptp: float,
    completed_tests: Optional[Dict[str, bool]] = None
) -> List[Recommendation]:
    from src.localization import translator

    if completed_tests is None:
        completed_tests = {}

    recommendations = []

    has_ccta = completed_tests.get("ccta_done", False)
    has_functional = any(completed_tests.get(f"{test}_done", False)
                         for test in ["stress_ecg", "stress_echo", "spect", "pet", "stress_cmr"])

    if has_ccta and st.session_state.test_results.get("ccta") == "Positive":
        recommendations.append({
            "test": translator.t("recommendations.tests.ica"),
            "reason": translator.t("recommendations.reasons.high_risk_ccta"),
            "performance": translator.t("recommendations.performance.ica_ffr"),
            "recommendation_quote": translator.t("recommendations.quotes.high_risk_ica"),
            "class_": "I",
            "level": "A"
        })
        return recommendations

    if has_functional:
        for test in ["stress_ecg", "stress_echo", "spect", "pet", "stress_cmr"]:
            if completed_tests.get(f"{test}_done") and st.session_state.test_results.get(test) == "Positive":
                recommendations.append({
                    "test": translator.t("recommendations.tests.ica"),
                    "reason": translator.t("recommendations.reasons.high_risk_functional"),
                    "performance": translator.t("recommendations.performance.ica_ffr"),
                    "recommendation_quote": translator.t("recommendations.quotes.high_risk_ica"),
                    "class_": "I",
                    "level": "A"
                })
                return recommendations

    if adjusted_ptp > 85:
        recommendations.append({
            "test": translator.t("recommendations.tests.ica"),
            "reason": translator.t("recommendations.reasons.very_high_ptp"),
            "performance": translator.t("recommendations.performance.direct_ica"),
            "recommendation_quote": translator.t("recommendations.quotes.high_risk_ica"),
            "class_": "I",
            "level": "A"
        })

    elif has_ccta and has_functional:
        if (st.session_state.test_results.get("ccta") == "Positive" or
            any(st.session_state.test_results.get(test) == "Positive"
                for test in ["stress_ecg", "stress_echo", "spect", "pet", "stress_cmr"])):
            recommendations.append({
                "test": translator.t("recommendations.tests.ica"),
                "reason": translator.t("recommendations.reasons.uncertain_diagnosis"),
                "performance": translator.t("recommendations.performance.ica_ffr_capability"),
                "recommendation_quote": translator.t("recommendations.quotes.uncertain_diagnosis"),
                "class_": "I",
                "level": "B"
            })
        else:
            recommendations.append({
                "test": translator.t("recommendations.tests.anoca_inoca"),
                "reason": translator.t("recommendations.reasons.obstructive_cad_excluded"),
                "performance": translator.t("recommendations.performance.invasive_coronary_functional"),
                "recommendation_quote": translator.t("recommendations.quotes.anoca_inoca"),
                "class_": "I",
                "level": "B"
            })

    elif has_ccta and not has_functional and st.session_state.test_results.get("ccta") != "Positive":
        recommendations.append({
            "test": translator.t("recommendations.tests.functional_imaging"),
            "reason": translator.t("recommendations.reasons.uncertain_functional_significance"),
            "performance": translator.t("recommendations.performance.functional_testing"),
            "recommendation_quote": translator.t("recommendations.quotes.uncertain_functional_significance"),
            "class_": "I",
            "level": "B"
        })

    elif has_functional and not has_ccta:
        if any(st.session_state.test_results.get(test) == "Non-diagnostic"
               for test in ["stress_ecg", "stress_echo", "spect", "pet", "stress_cmr"]
               if completed_tests.get(f"{test}_done")):
            recommendations.append({
                "test": translator.t("recommendations.tests.ccta"),
                "reason": translator.t("recommendations.reasons.non_diagnostic_functional"),
                "performance": translator.t("recommendations.performance.ccta_recommended"),
                "recommendation_quote": translator.t("recommendations.quotes.non_diagnostic_functional"),
                "class_": "I",
                "level": "B"
            })
        else:
            if 5 < adjusted_ptp <= 50:
                recommendations.append({
                    "test": translator.t("recommendations.tests.ccta"),
                    "reason": translator.t("recommendations.reasons.rule_out_obstructive_cad"),
                    "performance": translator.t("recommendations.performance.ccta_confirm"),
                    "recommendation_quote": translator.t("recommendations.quotes.rule_out_obstructive_cad"),
                    "class_": "I",
                    "level": "B"
                })
            elif adjusted_ptp <= 5:
                recommendations.append({
                    "test": translator.t("recommendations.tests.anoca_inoca"),
                    "reason": translator.t("recommendations.reasons.negative_functional_low_ptp"),
                    "performance": translator.t("recommendations.performance.invasive_coronary_functional"),
                    "recommendation_quote": translator.t("recommendations.quotes.anoca_inoca"),
                    "class_": "I",
                    "level": "B"
                })

    elif not has_ccta and not has_functional:
        if adjusted_ptp <= 5:
            recommendations.append({
                "test": translator.t("recommendations.tests.defer_testing"),
                "reason": translator.t("recommendations.reasons.very_low_ptp"),
                "performance": translator.t("recommendations.performance.risk_exceeds_benefit"),
                "recommendation_quote": translator.t("recommendations.quotes.very_low_ptp"),
                "class_": "IIa",
                "level": "B"
            })
        elif 5 < adjusted_ptp <= 50:
            recommendations.append({
                "test": translator.t("recommendations.tests.ccta_or_functional"),
                "reason": translator.t("recommendations.reasons.low_moderate_ptp"),
                "performance": translator.t("recommendations.performance.either_modality"),
                "recommendation_quote": translator.t("recommendations.quotes.low_moderate_ptp"),
                "class_": "I",
                "level": "B"
            })
        elif 50 < adjusted_ptp <= 85:
            recommendations.append({
                "test": translator.t("recommendations.tests.functional_imaging_short"),
                "reason": translator.t("recommendations.reasons.high_ptp"),
                "performance": translator.t("recommendations.performance.functional_preferred"),
                "recommendation_quote": translator.t("recommendations.quotes.high_ptp"),
                "class_": "I",
                "level": "B"
            })

    return recommendations


def render_recommendations(
    recommendations: List[Recommendation],
    current_probability: float
) -> None:
    for rec in recommendations:
        _render_single_recommendation(rec)


def _render_single_recommendation(rec: Recommendation) -> None:
    st.error(f"### {rec['test']}")

    content = ""
    if rec["class_"] is not None and rec["level"] is not None:
        class_level_key = f"class_{rec['class_'].lower()}_level_{rec['level'].lower()}"
        content += f"**{translator.t(f'recommendations.class_levels.{class_level_key}')}**\n\n"

    content += f"{rec['recommendation_quote']}\n\n"
    content += f"**{translator.t('recommendations.reasons.reason_label')}:** {rec['reason']}\n\n"
    content += f"**{translator.t('recommendations.performance.performance_label')}:** {rec['performance']}"

    st.info(content)
