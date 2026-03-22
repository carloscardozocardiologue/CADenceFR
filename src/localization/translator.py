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
