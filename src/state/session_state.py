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