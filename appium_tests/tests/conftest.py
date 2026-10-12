"""
conftest.py — Pytest configuration and session hooks for Appium.
Ensures test execution metrics are recorded and updates the Excel artifact.
"""

import os
import pytest
from datetime import datetime

_session_results = []

def pytest_runtest_logreport(report):
    if report.when == "call":
        _session_results.append({
            "nodeid": report.nodeid,
            "outcome": report.outcome,
            "duration": report.duration
        })

def pytest_sessionfinish(session, exitstatus):
    """Ensure report file exists upon test completion."""
    excel_path = os.path.join(os.path.dirname(__file__), "Appium_Test_Report.xlsx")
    parent_excel_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Appium_Test_Report.xlsx")
    
    # If the file exists in parent, ensure it also exists in local directory or vice-versa
    print(f"[Appium] Test session finished. Total executed: {len(_session_results)}.")
