import pytest
import time
# Import the functions directly from your tools file
from course_tools import find_sections_by_department, find_sections_by_level, find_sections_by_time, df

@pytest.fixture(autouse=True)
def ensure_data_loaded():
    """A fixture to ensure the DataFrame is loaded before tests run."""
    if df.empty:
        pytest.fail("Pandas DataFrame is empty. Ensure Sections.json is present and loaded correctly.")

def test_find_by_department_cs():
    """Tests that searching for 'CS' returns Computer Science courses."""
    results = find_sections_by_department("CS")
    assert len(results) > 0
    assert "CS 100-A" in [r["SectionName"] for r in results]

def test_find_by_department_no_results():
    """Tests that a nonsense department query returns an empty list."""
    results = find_sections_by_department("XYZ")
    assert results == []

def test_find_by_level_300():
    """Tests that level '300' returns 300-level courses."""
    results = find_sections_by_level("300")
    assert len(results) > 0
    # Verify a known 300-level course is in the results
    assert "ENGR 303-A" in [r["SectionName"] for r in results]

def test_find_by_time_evening():
    """Tests that the evening filter returns courses after 5 PM (17:00)."""
    results = find_sections_by_time("evening")
    assert len(results) > 0
    # Verify a known evening course is in the results
    assert "ARTS 254-A" in [r["SectionName"] for r in results]
    
def test_performance_department_search():
    """Measures the latency of a typical department search."""
    start_time = time.time()
    results = find_sections_by_department("ENGR")
    duration = time.time() - start_time
    print(f"\nENGR search took {duration:.4f} seconds and found {len(results)} results.")
    assert duration < 1.0 # Should be very fast