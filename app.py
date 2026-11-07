"""DART 재무 분석 — 로컬 Streamlit 진입점."""
from dotenv import load_dotenv

load_dotenv()

from dart_analyst.ui import main

main()
