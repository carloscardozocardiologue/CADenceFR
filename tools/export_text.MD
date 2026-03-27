# Project Export — CADenceFR
_Generated: 2026-03-27 14:33:48_

---

## 📁 Project Structure

```
CADenceFR/
├── .git/  ← skipped
├── .venv/  ← skipped
├── src/
│   ├── components/
│   │   ├── __pycache__/  ← skipped
│   │   ├── patient_characteristics.py
│   │   ├── probability_adjustment.py
│   │   ├── recommendations.py
│   │   ├── risk_factors.py
│   │   └── test_results.py
│   ├── constants/
│   │   ├── __pycache__/  ← skipped
│   │   ├── clinical_constants.py
│   │   └── likelihood_ratios.py
│   ├── localization/
│   │   ├── __pycache__/  ← skipped
│   │   ├── locales/
│   │   │   ├── en.json
│   │   │   └── fr.json
│   │   ├── __init__.py
│   │   └── translator.py
│   ├── state/
│   │   ├── __pycache__/  ← skipped
│   │   └── session_state.py
│   ├── tools/
│   │   └── generate_export.py
│   └── utils/
│       ├── __pycache__/  ← skipped
│       ├── calculations.py
│       └── validators.py
├── tools/
├── .gitignore
├── app.py
├── LICENSE
├── README.md
└── requirements.txt
```

---

## 📄 File Contents

### `.gitignore`

```text
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# UV
#   Similar to Pipfile.lock, it is generally recommended to include uv.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#uv.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/latest/usage/project/#working-with-version-control
.pdm.toml
.pdm-python
.pdm-build/

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/

# PyPI configuration file
.pypirc

```

### `app.py`

```py
"""
CADence: ESC 2024 CCS Guideline-Based Probability Calculator for Coronary Artery Disease
Main application entry point.
"""

import streamlit as st
from typing import Dict, Any

# Import components
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

# Import utilities and state management
from src.utils.calculations import (
    calculate_rf_cl,
    calculate_cacs_cl,
    adjust_likelihood_for_test_results
)
from src.state.session_state import SessionState

def setup_page():
    """Configure the Streamlit page settings."""
    st.set_page_config(
        page_title="CAD Probability Calculator",
        page_icon="🫀"#,
        #layout="wide"
    )
    
    st.title("CADence FR 🫀")
    st.markdown("""
    <p style='font-size: 20px; margin-top: -20px; font-style: italic; color: #666666;'>
    ESC 2024 CCS Guideline-Based Probability Calculator for Coronary Artery Disease
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <p style='font-size: 16px; color: #888888;'>
    Your companion for evidence-based CAD assessment, integrating ESC guidelines, 
    risk factor analysis, and diagnostic recommendations into one seamless workflow.
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
    """Handle changes to the probability score selection."""
    if 'probability_score_selector' not in st.session_state or not st.session_state.probability_score_selector:
        st.session_state.selected_probability_score = st.session_state.default_score
    else:
        st.session_state.selected_probability_score = st.session_state.probability_score_selector


# CADence: ESC 2024 CCS Guideline-Based Probability Calculator
# Main application entry point.

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
    st.set_page_config(
        page_title="CADence FR",
        page_icon="🫀"
    )

    st.session_state.language = 'fr'
    translator.set_language('fr')

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
```

### `LICENSE`

```text
MIT License

Copyright (c) 2025 U Bhalraam (Raam)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```

### `README.md`

```md
# CADence

ESC 2024 CCS Guideline-Based Probability Calculator for Coronary Artery Disease

## Overview

CADence is a clinical decision support tool that helps clinicians assess the probability of coronary artery disease based on the latest ESC guidelines. It integrates patient characteristics, risk factors, and test results to provide evidence-based recommendations.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cadence.git
cd cadence
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

## Structure

The application is organized into several modules:
- `src/components/`: UI components
- `src/constants/`: Constant values and configurations
- `src/state/`: State management
- `src/utils/`: Utility functions and calculations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Dr. U Bhalraam MBChB, BMSc, MRCP
```

### `requirements.txt`

```txt
streamlit>=1.41.0
pandas>=2.2.3
numpy>=2.2.2
```

### `src\components\patient_characteristics.py`

```py
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

```

### `src\components\probability_adjustment.py`

```py
"""Probability adjustment components."""

import streamlit as st
from typing import Optional
from src.state.session_state import SessionState
from src.localization import translator


def _on_slider_change():
    if "manual_adjustment_value" in st.session_state:
        st.session_state.manual_rf_cl_adjustment = st.session_state.manual_adjustment_value


def _on_reset_click():
    st.session_state.manual_rf_cl_adjustment = None
    if "manual_adjustment_value" in st.session_state:
        del st.session_state.manual_adjustment_value


def render_probability_adjustment(base_rf_cl: float) -> None:
    if st.session_state.manual_rf_cl_adjustment is not None:
        st.metric(
            translator.t("probability.titles.adj_rf_cl"),
            f"{st.session_state.manual_rf_cl_adjustment:.1f}%*",
            delta=f"{st.session_state.manual_rf_cl_adjustment - base_rf_cl:.1f}%"
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
            starting_value = (st.session_state.manual_rf_cl_adjustment
                            if st.session_state.manual_rf_cl_adjustment is not None
                            else base_rf_cl)
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
                    delta=f"{cacs_cl - current_prob:.1f}%"
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

```

### `src\components\recommendations.py`

```py
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

```

### `src\components\risk_factors.py`

```py
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

```

### `src\components\test_results.py`

```py
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
        delta=f"{adjusted_prob - base_prob:.1f}%"
    )

```

### `src\constants\clinical_constants.py`

```py
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
```

### `src\constants\likelihood_ratios.py`

```py
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
```

### `src\localization\__init__.py`

```py
from .translator import translator
__all__ = ['translator']
```

### `src\localization\locales\en.json`

```json
{
  "app": {
    "title": "CADence 🫀",
    "description": "A clinical tool for estimating the pre-test probability of coronary artery disease (CAD) in patients with stable chest pain."
  },
  "ui": {
    "next": "Next",
    "previous": "Previous",
    "submit": "Submit",
    "reset": "Reset",
    "language": "Language",
    "select_language": "Select your language",
    "loading": "Loading..."
  },
  "patient": {
    "title": "Patient Characteristics",
    "age": "Age",
    "sex": "Sex",
    "male": "Male",
    "female": "Female",
    "chest_pain_type": "Chest Pain Type",
    "typical_angina": "Typical Angina",
    "atypical_angina": "Atypical Angina",
    "non_anginal": "Non-anginal Pain",
    "unknown": "Unknown"
  },
  "risk_factors": {
    "title": "Risk Factors",
    "hypertension": "Hypertension",
    "diabetes": "Diabetes",
    "dyslipidemia": "Dyslipidemia",
    "smoking": "Smoking",
    "family_history": "Family History of CAD"
  },
  "probability": {
    "title": "Pre-test Probability",
    "calculate": "Calculate Probability",
    "result": "Estimated Pre-test Probability",
    "low": "Low",
    "intermediate": "Intermediate",
    "high": "High"
  },
  "tests": {
    "title": "Test Results",
    "ecg": "ECG",
    "stress_test": "Stress Test",
    "ct_angio": "CT Angiography",
    "result": "Result",
    "positive": "Positive",
    "negative": "Negative",
    "indeterminate": "Indeterminate"
  },
  "recommendations": {
    "title": "Recommendations",
    "further_testing": "Further Testing Recommended",
    "no_testing": "No Further Testing Needed",
    "treatment": "Treatment Recommendation"
  },
  "footer": {
    "disclaimer": "This tool is for educational purposes only and should not replace clinical judgment.",
    "source": "Source: ESC Guidelines 2019"
  },
  "errors": {
    "invalid_input": "Invalid input. Please check your entries.",
    "calculation_error": "An error occurred during calculation."
  }
}

```

### `src\localization\locales\fr.json`

```json
{
  "app": {
    "title": "CADence FR 🫀",
    "subtitle": "Calculateur de Probabilité d'une Coronaropathie Obstructive Chronique — Guidelines ESC 2024.",
    "description": ""
  },
  "ui": {
    "labels": {
      "age": "Âge",
      "gender": "Sexe",
      "male": "Homme",
      "female": "Femme",
      "language": "Langue"
    },
    "buttons": {
      "reset": "🔄 Réinitialiser",
      "calculate": "Calculer"
    },
    "segmented_control": {
      "select_score": "Sélectionner le score pour les recommandations"
    }
  },
  "patient": {
    "title": "🧑‍⚕️ Caractéristiques du Patient",
    "age_help": "Validé pour les âges 30-79 ans. Les résultats hors de cette plage doivent être interprétés avec prudence.",
    "basic_info": {
      "age_range_error": "L'âge doit être entre {min_age} et {max_age} ans",
      "age_validation_warning": "Modèle validé pour les âges {min_age}-{max_age} ans. Interpréter avec prudence."
    },
    "symptoms": {
      "title": "Type de Symptôme",
      "chest_pain": "Douleur Thoracique",
      "dyspnea": "Dyspnée",
      "classification_title": "Classification de la Douleur Thoracique",
      "substernal": "Gêne thoracique rétrosternale",
      "provoked": "Provoquée par l'effort ou le stress",
      "relieved": "Soulagée par le repos ou la nitroglycérine",
      "typical_angina": "🔴 Angor Typique (3/3 critères)",
      "atypical_angina": "🟡 Angor Atypique (2/3 critères)",
      "non_anginal": "🟢 Douleur Non-Angineuse (0-1/3 critères)",
      "dyspnea_description": "Dyspnée d'effort",
      "dyspnea_help": "Dyspnée équivalente à un angor atypique selon ESC 2024"
    }
  },
  "risk_factors": {
    "title": "⚠️ Facteurs de Risque",
    "pill_help": "Sélectionnez tous les facteurs de risque présents",
    "definitions_title": "📖 Définitions des Facteurs de Risque",
    "diabetes": "Diabète",
    "smoking": "Tabagisme Actuel/Passé",
    "hypertension": "Hypertension",
    "dyslipidemia": "Dyslipidémie",
    "family_history": "Antécédents Familiaux de Coronaropathie Précoce",
    "definitions": {
      "diabetes": "Glycémie à jeun ≥7,0 mmol/L ou HbA1c ≥6,5% ou traitement antidiabétique en cours.",
      "smoking": "Fumeur actuel ou arrêt depuis moins de 3 ans.",
      "hypertension": "PA systolique ≥140 mmHg ou diastolique ≥90 mmHg ou traitement antihypertenseur en cours.",
      "dyslipidemia": "Cholestérol total >5,0 mmol/L ou LDL >3,0 mmol/L ou traitement hypolipémiant en cours.",
      "family_history": "Parent du 1er degré avec Coronaropathie avant 55 ans (homme) ou 65 ans (femme)."
    }
  },
  "probability": {
    "titles": {
      "risk_assessment": "📊 Évaluation du Risque",
      "rf_cl": "RF-CL",
      "adj_rf_cl": "RF-CL Ajusté",
      "cacs_cl": "CACS-CL",
      "adj_cacs_cl": "CACS-CL Ajusté",
      "post_test_rf_cl": "Probabilité Post-Test RF-CL",
      "post_test_adj_rf_cl": "Probabilité Post-Test RF-CL Ajusté",
      "post_test_cacs_cl": "Probabilité Post-Test CACS-CL"
    },
    "adjustment": {
      "title": "⚕️ Ajustement selon les Constatations Cliniques",
      "slider_label": "Probabilité ajustée (%)",
      "info_text": "Ajustez le RF-CL en fonction des constatations cliniques supplémentaires non capturées par le modèle.",
      "guidelines_title": "📋 Considérations pour l'Ajustement Clinique",
      "guidelines_content": "### Considérations pour l'Ajustement Clinique\n\n**📊 Modifications ECG**\n- 📍 Anomalies ECG de repos — Ondes Q ou modifications du segment ST/onde T ↑ +10 à +15%\n- 📍 Constatations ECG d'effort — même si non diagnostiques ↑ +5 à +10%\n- 📍 Anomalies de conduction — BBG/BBD ↑ +5 à +10%\n\n**❤️ Fonction Cardiaque**\n- 💔 Dysfonction VG — sévère ou segmentaire ↑ +15 à +20%\n- 💓 Arythmie ventriculaire — trouble rythmique significatif ↑ +8 à +12%\n- 😮‍💨 Symptômes d'insuffisance cardiaque — dyspnée d'effort, tolérance réduite ↑ +8 à +12%\n\n**🫀 Maladie Vasculaire**\n- 🔄 Artériopathie périphérique — AOMI documentée ou symptômes ↑ +12 à +18%\n- 🔍 Calcification préexistante — notée sur imagerie thoracique antérieure ↑ +8 à +12%\n- 🔍 Maladie carotidienne — sténose carotidienne connue ↑ +8 à +12%\n- 🔍 Maladie aortique — athérosclérose aortique ↑ +5 à +8%\n\n**🏥 Comorbidités**\n- 🎯 Maladie rénale chronique — surtout si DFG <60 ↑ +8 à +12%\n- 🔥 Conditions inflammatoires — polyarthrite rhumatoïde, lupus ↑ +8 à +15%\n- ⚠️ Troubles métaboliques — maladie thyroïdienne, obésité ↑ +3 à +5%\n\n**📋 Évaluation des Facteurs de Risque**\n- 📌 Facteurs de risque multiples — au-delà de ceux capturés dans l'évaluation de base ↑ +5 à +8%\n- 📈 Sévérité des facteurs de risque — diabète mal contrôlé, hypertension sévère ↑ +8 à +12%\n- ⏳ Durée d'exposition — exposition à long terme aux facteurs de risque ↑ +3 à +5%\n- 🎯 Regroupement de facteurs de risque — facteurs multiples chez patient jeune (<50 ans) ↑ +10 à +15%\n\n**👥 Groupes de Patients Spécifiques**\n- 👩 Femmes ménopausées — surtout avec facteurs de risque ↑ +5 à +8%\n- 🎗️ Survivants du cancer — surtout après radiothérapie thoracique ↑ +10 à +15%\n- 🫀 Receveurs de transplantation — impact de l'immunosuppression ↑ +8 à +12%\n- 🦠 Patients VIH — athérosclérose accélérée ↑ +8 à +12%\n\n> ⚕️ *Ces estimations sont indicatives. L'ajustement final reste à la discrétion du clinicien.*",
      "reset_adjustments": "Réinitialiser l'ajustement",
      "total_delta": "Ajustement total"
    },
    "cacs": {
      "title": "🫀 CACS (Score Calcique Coronarien)",
      "input_label": "Entrez le CACS (score d'Agatston)",
      "input_help": "Score d'Agatston issu du scanner calcique coronarien",
      "interpretations": {
        "no_calcification": "✅ Pas de calcification — risque Coronaropathie très faible",
        "minimal": "✅ Calcification minime (1-9)",
        "mild": "⚠️ Calcification légère (10-99)",
        "moderate": "⚠️ Calcification modérée (100-399)",
        "severe": "🔴 Calcification sévère (400-999)",
        "extensive": "🔴 Calcification étendue (≥1000)"
      }
    }
  },
  "tests": {
    "title": "🔬 Avez-vous des résultats de tests antérieurs ? Entrez-les ici pour une probabilité post-test",
    "ffr_toggle": "Utiliser le référentiel FFR",
    "ffr_help": "Basculer entre les ratios de vraisemblance anatomiques et FFR",
    "ffr_info": "ℹ️ Le référentiel FFR s'applique uniquement à la Scintigraphie, la TEP et l'IRM cardiaque de stress",
    "result_label": "Résultat",
    "result_positive": "Positive",
    "result_negative": "Negative",
    "names": {
      "ccta": "Coroscanner",
      "stress_ecg": "ECG d'Effort",
      "stress_echo": "Échocardiographie de Stress",
      "spect": "Scintigraphie myocardique (SPECT)",
      "pet": "TEP myocardique",
      "stress_cmr": "IRM cardiaque de stress"
    },
    "ccta": {
      "positive_label": "Coroscanner positif (Coronaropathie obstructive)",
      "help": "**Critères de haut risque au Coroscanner :**\n- Sténose du tronc commun ≥50%\n- Maladie tritronculaire avec sténose ≥70%\n- Maladie bitronculaire avec sténose ≥70% incluant l'IVA proximale\n- Maladie monotronculaire de l'IVA proximale avec sténose ≥70% et FFR-CT ≤0,80"
    },
    "high_risk_features": {
      "stress_ecg": "**Critères de haut risque à l'ECG d'effort :**\n• Score de Duke sur tapis roulant < −10",
      "stress_echo": "**Critères de haut risque à l'Échocardiographie de stress :**\n• ≥3 segments sur 16 avec hypokinésie ou akinésie induite par le stress",
      "spect": "**Critères de haut risque à la Scintigraphie myocardique :**\n• Zone d'ischémie ≥10% du myocarde du VG",
      "pet": "**Critères de haut risque à la TEP myocardique :**\n• Zone d'ischémie ≥10% du myocarde du VG",
      "stress_cmr": "**Critères de haut risque à l'IRM cardiaque de stress :**\n• ≥2 segments sur 16 avec défauts de perfusion au stress\n• ou ≥3 segments dysfonctionnels induits par la dobutamine"
    }
  },
  "recommendations": {
    "title": "📋 Recommandations",
    "based_on": "Recommandations basées sur **{score}** : **{probability}%**{asterisk}",
    "tests": {
      "ica": "Coronarographie",
      "ccta": "Coroscanner",
      "functional_imaging": "Imagerie Fonctionnelle",
      "functional_imaging_short": "Imagerie Fonctionnelle",
      "ccta_or_functional": "Coroscanner ou Imagerie Fonctionnelle",
      "defer_testing": "Différer les Examens",
      "anoca_inoca": "Bilan ANOCA / INOCA"
    },
    "reasons": {
      "reason_label": "Raison",
      "very_high_ptp": "Probabilité pré-test très élevée (>85%) — coronarographie directe indiquée",
      "high_risk_ccta": "Critères de haut risque au Coroscanner — Coronaropathie obstructive probable",
      "high_risk_functional": "Critères de haut risque à l'imagerie fonctionnelle — ischémie confirmée",
      "uncertain_diagnosis": "Résultats discordants entre Coroscanner et imagerie fonctionnelle",
      "obstructive_cad_excluded": "Coronaropathie obstructive exclue — étiologie non obstructive probable",
      "uncertain_functional_significance": "Signification fonctionnelle incertaine des résultats du Coroscanner",
      "non_diagnostic_functional": "Test fonctionnel non diagnostique — clarification anatomique nécessaire",
      "rule_out_obstructive_cad": "Exclure une Coronaropathie obstructive par imagerie anatomique",
      "negative_functional_low_ptp": "Test fonctionnel négatif avec probabilité pré-test faible — ANOCA/INOCA possible",
      "very_low_ptp": "Probabilité pré-test très faible (≤5%) — le risque du test dépasse le bénéfice",
      "low_moderate_ptp": "Probabilité pré-test faible à modérée (5-50%)",
      "high_ptp": "Probabilité pré-test élevée (50-85%) — imagerie fonctionnelle préférée"
    },
    "performance": {
      "performance_label": "Performance",
      "ica_ffr": "Coronarographie avec capacité FFR pour évaluation hémodynamique",
      "direct_ica": "Coronarographie directe — revascularisation potentiellement indiquée",
      "ica_ffr_capability": "Coronarographie avec FFR pour évaluation hémodynamique",
      "functional_testing": "Imagerie fonctionnelle pour évaluation de l'ischémie",
      "ccta_recommended": "Coroscanner recommandé pour clarification anatomique",
      "ccta_confirm": "Coroscanner pour confirmer ou exclure une Coronaropathie obstructive",
      "either_modality": "Les deux modalités acceptables selon disponibilité locale",
      "functional_preferred": "Imagerie fonctionnelle préférée pour probabilité élevée",
      "invasive_coronary_functional": "Tests fonctionnels coronariens invasifs si symptômes persistants"
    },
    "quotes": {
      "high_risk_ica": "En cas de critères de haut risque à l'imagerie non invasive, une coronarographie est recommandée. (Classe I, Niveau A — ESC 2024 CCS)",
      "uncertain_diagnosis": "En cas de résultats discordants entre tests anatomiques et fonctionnels, une coronarographie avec FFR est recommandée. (Classe I, Niveau B — ESC 2024 CCS)",
      "anoca_inoca": "Si une Coronaropathie obstructive est exclue, un bilan de dysfonction coronarienne non obstructive (ANOCA/INOCA) est recommandé en cas de symptômes persistants. (Classe I, Niveau B — ESC 2024 CCS)",
      "uncertain_functional_significance": "En cas de sténose coronarienne de signification fonctionnelle incertaine au Coroscanner, une imagerie fonctionnelle complémentaire est recommandée. (Classe I, Niveau B — ESC 2024 CCS)",
      "non_diagnostic_functional": "En cas de test fonctionnel non diagnostique, un Coroscanner est recommandé. (Classe I, Niveau B — ESC 2024 CCS)",
      "rule_out_obstructive_cad": "Pour exclure une Coronaropathie obstructive, un Coroscanner est recommandé. (Classe I, Niveau B — ESC 2024 CCS)",
      "very_low_ptp": "En cas de probabilité pré-test très faible (≤5%), il est recommandé de différer les examens complémentaires. (Classe IIa, Niveau B — ESC 2024 CCS)",
      "low_moderate_ptp": "Pour une probabilité pré-test faible à modérée (5-50%), un Coroscanner ou une imagerie fonctionnelle sont recommandés. (Classe I, Niveau B — ESC 2024 CCS)",
      "high_ptp": "Pour une probabilité pré-test élevée (50-85%), une imagerie fonctionnelle est recommandée en première intention. (Classe I, Niveau B — ESC 2024 CCS)"
    },
    "class_levels": {
      "class_i_level_a": "Classe I — Niveau A",
      "class_i_level_b": "Classe I — Niveau B",
      "class_i_level_c": "Classe I — Niveau C",
      "class_iia_level_a": "Classe IIa — Niveau A",
      "class_iia_level_b": "Classe IIa — Niveau B",
      "class_iia_level_c": "Classe IIa — Niveau C",
      "class_iib_level_a": "Classe IIb — Niveau A",
      "class_iib_level_b": "Classe IIb — Niveau B",
      "class_iii_level_a": "Classe III — Niveau A",
      "class_iii_level_b": "Classe III — Niveau B"
    }
  },
  "footer": {
    "references_title": "Références",
    "references_text": "1. Vrints C, et al. 2024 ESC Guidelines for the management of chronic coronary syndromes. Eur Heart J. 2024.\n2. Winther S, et al. Incorporating coronary calcification into pre-test assessment of the likelihood of coronary artery disease. J Am Coll Cardiol. 2020.\n3. Knuuti J, et al. Meta-analysis of diagnostic test accuracy for non-invasive coronary artery disease testing. Eur Heart J. 2019.",
    "disclaimer": "⚠️ Cet outil est destiné à un usage clinique éducatif uniquement. Il ne remplace pas le jugement clinique ni les guidelines institutionnelles. Toujours interpréter les résultats dans le contexte clinique global du patient.",
    "developed_by": "Développé par <a href='https://x.com/cardioshades' target='_blank' style='text-decoration: none; color: inherit;'><strong>Dr. U Bhalraam</strong></a> MBChB, BMSc, MRCP<br><br>Traduction au Français : <strong>Dr. Carlos CARDOZO</strong><br>Cardiologue Interventionnel<br>Centre Cardiologique d'Evecquemont"
  },
  "errors": {
    "general_error": "Une erreur s'est produite : {error}"
  }
}
```

### `src\localization\translator.py`

```py
"""Translation module for CADence application."""

import json
import os
from typing import Dict, Any, Optional
import streamlit as st


class Translator:
    
    def __init__(self):
        self.locales_dir = os.path.join(os.path.dirname(__file__), 'locales')
        self.translations = {}
        self.current_language = 'fr'
        self._load_translations()
    
    def _load_translations(self):
        if not os.path.exists(self.locales_dir):
            return
        for filename in os.listdir(self.locales_dir):
            if filename.endswith('.json'):
                lang_code = filename[:-5]
                filepath = os.path.join(self.locales_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        self.translations[lang_code] = json.load(f)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
    
    def get_current_language(self) -> str:
        if hasattr(st, 'session_state') and 'language' in st.session_state:
            return st.session_state.language
        return self.current_language
    
    def set_language(self, language_code: str):
        if language_code in self.translations:
            self.current_language = language_code
            if hasattr(st, 'session_state'):
                st.session_state.language = language_code
    
    def t(self, key: str, **kwargs) -> str:
        current_lang = self.get_current_language()
        translation = self._get_nested_value(
            self.translations.get(current_lang, {}), key
        )
        if translation is None and current_lang != 'fr':
            translation = self._get_nested_value(
                self.translations.get('fr', {}), key
            )
        if translation is None:
            return f"[MISSING: {key}]"
        try:
            return translation.format(**kwargs)
        except (KeyError, ValueError):
            return translation
    
    def _get_nested_value(self, data: Dict[str, Any], key: str) -> Optional[str]:
        if not isinstance(data, dict):
            return None
        keys = key.split('.')
        current = data
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return None
        return current if isinstance(current, str) else None


translator = Translator()

```

### `src\state\session_state.py`

```py
"""Session state management for the CADence app."""

import streamlit as st
from typing import Dict, Any
from src.constants.clinical_constants import AVAILABLE_TESTS

class SessionState:
    """Manages the session state for the CADence app."""
    
    @staticmethod
    def initialize_state():
        """Initialize all session state variables if they don't exist."""
        if 'test_results' not in st.session_state:
            st.session_state.test_results = {
                test: '' for test in AVAILABLE_TESTS
            }
            
        if 'completed_tests' not in st.session_state:
            st.session_state.completed_tests = {
                f'{test}_done': False for test in AVAILABLE_TESTS
            }
            
        if 'use_ffr' not in st.session_state:
            st.session_state.use_ffr = False
            
        if 'manual_rf_cl_adjustment' not in st.session_state:
            st.session_state.manual_rf_cl_adjustment = None
            
        if 'manual_adjustment_expander_open' not in st.session_state:
            st.session_state.manual_adjustment_expander_open = False
            
        if 'current_rf_cl' not in st.session_state:
            st.session_state.current_rf_cl = None

    @staticmethod
    def update_manual_adjustment(value: float):
        """Update the manual RF-CL adjustment value."""
        if (st.session_state.manual_adjustment_expander_open and 
            'manual_adjustment_value' in st.session_state):
            st.session_state.manual_rf_cl_adjustment = value

    @staticmethod
    def reset_manual_adjustment():
        """Reset the manual RF-CL adjustment state."""
        st.session_state.manual_rf_cl_adjustment = None
        st.session_state.manual_adjustment_expander_open = False
        if 'manual_adjustment_value' in st.session_state:
            del st.session_state.manual_adjustment_value

    @staticmethod
    def update_test_completion(test_name: str):
        """Handle changes when a test's completion status is toggled."""
        checkbox_key = f'{test_name}_checkbox'
        if checkbox_key in st.session_state:
            st.session_state.completed_tests[f'{test_name}_done'] = st.session_state[checkbox_key]
            
            if not st.session_state[checkbox_key]:
                # Clear test results when unchecking
                st.session_state.test_results[test_name] = ''
                if f'{test_name}_key' in st.session_state:
                    del st.session_state[f'{test_name}_key']
                if test_name == 'ccta' and 'ccta_result' in st.session_state:
                    del st.session_state.ccta_result
            else:
                # Set default states when checking
                if test_name == 'ccta':
                    if 'ccta_result' not in st.session_state:
                        st.session_state.ccta_result = False
                    st.session_state.test_results['ccta'] = 'Negative'
                else:
                    st.session_state[f'{test_name}_key'] = 'Negative'
                    st.session_state.test_results[test_name] = 'Negative'

    @staticmethod
    def update_test_result(test_name: str):
        """Handle changes in test results."""
        key = f'{test_name}_key'
        if key in st.session_state:
            st.session_state.test_results[test_name] = st.session_state[key]

    @staticmethod
    def update_ccta_result():
        """Handle changes when the CCTA result toggle is switched."""
        if 'ccta_result' in st.session_state:
            st.session_state.test_results['ccta'] = (
                'Positive' if st.session_state.ccta_result else 'Negative'
            )

    @staticmethod
    def get_state() -> Dict[str, Any]:
        """Get the current state as a dictionary."""
        return {
            'test_results': st.session_state.test_results,
            'completed_tests': st.session_state.completed_tests,
            'use_ffr': st.session_state.use_ffr,
            'manual_rf_cl_adjustment': st.session_state.manual_rf_cl_adjustment,
            'current_rf_cl': st.session_state.current_rf_cl
        }
```

### `src\tools\generate_export.py`

```py
"""
tools/generate_export.py
Generates export_text.MD — a full snapshot of the project for LLM review.
Usage: run from the project root → python tools/generate_export.py
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# ── Configuration ─────────────────────────────────────────────────────────────

# Folders to skip entirely
SKIP_DIRS = {
    ".venv", "venv", "__pycache__", ".git", ".mypy_cache",
    ".pytest_cache", "node_modules", ".streamlit/secrets",
    "dist", "build", ".eggs", "*.egg-info",
}

# Files to skip by name
SKIP_FILES = {
    ".env", ".env.local", ".DS_Store", "Thumbs.db",
    "export_text.MD",           # avoid including a previous export
}

# Extensions to skip (binary / large assets)
SKIP_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico",
    ".pdf", ".xlsx", ".xls", ".csv",
    ".pkl", ".pickle", ".h5", ".parquet",
    ".zip", ".tar", ".gz",
    ".pyc", ".pyo",
    ".lock",                    # package-lock / poetry.lock can be huge
}

# Extensions to include as readable text
TEXT_EXTENSIONS = {
    ".py", ".md", ".txt", ".toml", ".yaml", ".yml",
    ".json", ".ini", ".cfg", ".env.example",
    ".html", ".css", ".js", ".ts", ".jsx", ".tsx",
    ".sh", ".bat", "",          # extensionless files (Makefile, Dockerfile…)
}

OUTPUT_FILE = Path("tools/export_text.MD")
MAX_FILE_BYTES = 100_000        # skip files larger than ~100 KB

# ── Helpers ───────────────────────────────────────────────────────────────────

def should_skip_dir(name: str) -> bool:
    return name in SKIP_DIRS or name.startswith(".")

def should_skip_file(path: Path) -> bool:
    if path.name in SKIP_FILES:
        return True
    if path.suffix.lower() in SKIP_EXTENSIONS:
        return True
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return True          # unknown extension → skip to be safe
    if path.stat().st_size > MAX_FILE_BYTES:
        return True
    return False

def build_tree(root: Path, prefix: str = "") -> list[str]:
    """Return directory tree lines (like `tree` command)."""
    lines = []
    entries = sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    for i, entry in enumerate(entries):
        connector = "└── " if i == len(entries) - 1 else "├── "
        if entry.is_dir():
            if should_skip_dir(entry.name):
                lines.append(f"{prefix}{connector}{entry.name}/  ← skipped")
                continue
            lines.append(f"{prefix}{connector}{entry.name}/")
            extension = "    " if i == len(entries) - 1 else "│   "
            lines.extend(build_tree(entry, prefix + extension))
        else:
            lines.append(f"{prefix}{connector}{entry.name}")
    return lines

def iter_files(root: Path):
    """Yield all readable files in deterministic order."""
    for path in sorted(root.rglob("*")):
        if path.is_file():
            # Check if any parent dir should be skipped
            if any(should_skip_dir(p.name) for p in path.parents):
                continue
            if should_skip_file(path):
                continue
            yield path

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    root = Path(".").resolve()
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    print(f"📦 Generating export from: {root}")
    print(f"📄 Output: {OUTPUT_FILE.resolve()}")

    lines = []

    # Header
    lines.append(f"# Project Export — {root.name}")
    lines.append(f"_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n")
    lines.append("---\n")

    # Directory tree
    lines.append("## 📁 Project Structure\n")
    lines.append("```")
    lines.append(f"{root.name}/")
    lines.extend(build_tree(root))
    lines.append("```\n")
    lines.append("---\n")

    # File contents
    lines.append("## 📄 File Contents\n")

    file_list = list(iter_files(root))
    print(f"   Found {len(file_list)} files to include.")

    for path in file_list:
        rel = path.relative_to(root)
        ext = path.suffix.lower().lstrip(".") or "text"
        lines.append(f"### `{rel}`\n")
        lines.append(f"```{ext}")
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
            lines.append(content)
        except Exception as e:
            lines.append(f"[Error reading file: {e}]")
        lines.append("```\n")

    # Write output
    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    size_kb = OUTPUT_FILE.stat().st_size / 1024
    print(f"✅ Done! export_text.MD written ({size_kb:.1f} KB, {len(file_list)} files)")

if __name__ == "__main__":
    main()
```

### `src\utils\calculations.py`

```py
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
```

### `src\utils\validators.py`

```py
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

```
