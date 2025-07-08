import pytest

def pytest_html_results_table_header(cells):
    cells.insert(2, "Description")

def pytest_html_results_table_row(report, cells):
    cells.insert(2, getattr(report, "description", "No description"))

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if hasattr(item, "function"):
        report.description = str(item.function.__doc__) if item.function.__doc__ else "No description"
