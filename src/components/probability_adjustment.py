"""Probability adjustment components."""

import streamlit as st
from typing import Optional
from src.state.session_state import SessionState
from src.localization import translator


def _on_slider_change():
    if "manual_adjustment_value" in st.session_state:
        st.session_state.manual_rf_cl_adjustment = st.session_state.manual_adjustment_value


def _on_reset_click():
    """Reset adjustment: return slider to original RF-CL, not to zero."""
    st.session_state.manual_rf_cl_adjustment = None
    # Delete the cached slider value so the next render re-initialises
    # it from base_rf_cl (synced below in render_probability_adjustment)
    if "manual_adjustment_value" in st.session_state:
        del st.session_state.manual_adjustment_value


def render_probability_adjustment(base_rf_cl: float) -> None:
    # ── KEY FIX ────────────────────────────────────────────────────────────────
    # Always persist the original RF-CL so the reset button can reference it.
    st.session_state.base_rf_cl = base_rf_cl

    # If no manual adjustment is active, force the slider widget to match the
    # current RF-CL.  Streamlit's slider ignores value= once the key exists in
    # session_state, so we must set it explicitly before the widget renders.
    if st.session_state.manual_rf_cl_adjustment is None:
        st.session_state["manual_adjustment_value"] = float(base_rf_cl)
    # ──────────────────────────────────────────────────────────────────────────

    if st.session_state.manual_rf_cl_adjustment is not None:
        st.metric(
            translator.t("probability.titles.adj_rf_cl"),
            f"{st.session_state.manual_rf_cl_adjustment:.1f}%*",
            delta=f"{st.session_state.manual_rf_cl_adjustment - base_rf_cl:.1f}%",
            delta_color="inverse"
        )
    else:
        st.metric(
            translator.t("probability.titles.rf_cl"),
            f"{base_rf_cl:.1f}%"
        )

    with st.expander(translator.t("probability.adjustment.title")) as exp:
        st.session_state.manual_adjustment_expander_open = exp
        col1, col2 = st.columns([0.7, 0.3], vertical_alignment="bottom")

        with col1:
            # starting_value drives the slider only on first render (before
            # the key exists in session_state).  After that, the explicit
            # session_state assignment above takes over.
            starting_value = (
                st.session_state.manual_rf_cl_adjustment
                if st.session_state.manual_rf_cl_adjustment is not None
                else base_rf_cl
            )
            st.slider(
                translator.t("probability.adjustment.slider_label"),
                min_value=0.0,
                max_value=100.0,
                value=float(starting_value),
                step=0.1,
                format="%.1f",
                key="manual_adjustment_value",
                on_change=_on_slider_change
            )

        with col2:
            st.button(
                translator.t("ui.buttons.reset"),
                use_container_width=True,
                on_click=_on_reset_click
            )

        st.info(translator.t("probability.adjustment.info_text"))
        _render_adjustment_guidelines()


def render_cacs_section(current_prob: float) -> Optional[int]:
    cacs = None
    with st.expander(translator.t("probability.cacs.title"), expanded=False):
        cacs = st.number_input(
            translator.t("probability.cacs.input_label"),
            min_value=0,
            value=None,
            key="cacs_score",
            help=translator.t("probability.cacs.input_help")
        )

        if cacs is not None and cacs != "":
            from src.utils.calculations import calculate_cacs_cl
            cacs_cl = calculate_cacs_cl(current_prob, cacs)
            st.session_state.current_cacs_cl = cacs_cl

            col1, col2 = st.columns([0.55, 0.45], vertical_alignment="center")
            with col1:
                is_adjusted = st.session_state.manual_rf_cl_adjustment is not None
                asterisk = "*" if is_adjusted else ""
                metric_label = (translator.t("probability.titles.adj_cacs_cl")
                                if is_adjusted
                                else translator.t("probability.titles.cacs_cl"))
                st.metric(
                    metric_label,
                    f"{cacs_cl:.1f}%{asterisk}",
                    delta=f"{cacs_cl - current_prob:.1f}%",
                    delta_color="inverse"
                )
            with col2:
                _render_cacs_interpretation(cacs)
        else:
            if "current_cacs_cl" in st.session_state:
                del st.session_state.current_cacs_cl
            if "cacs_cl" in st.session_state:
                del st.session_state.cacs_cl

    return cacs if cacs is not None and cacs != "" else None


def _render_adjustment_guidelines() -> None:
    with st.popover(translator.t("probability.adjustment.guidelines_title"), use_container_width=True):
        st.markdown(translator.t("probability.adjustment.guidelines_content"))


def _render_cacs_interpretation(cacs: int) -> None:
    if cacs == 0:
        st.success(translator.t("probability.cacs.interpretations.no_calcification"))
    elif cacs < 10:
        st.success(translator.t("probability.cacs.interpretations.minimal"))
    elif cacs < 100:
        st.warning(translator.t("probability.cacs.interpretations.mild"))
    elif cacs < 400:
        st.warning(translator.t("probability.cacs.interpretations.moderate"))
    elif cacs < 1000:
        st.error(translator.t("probability.cacs.interpretations.severe"))
    else:
        st.error(translator.t("probability.cacs.interpretations.extensive"))