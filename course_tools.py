import json
import pandas as pd
import re
from mcp.server.fastmcp import FastMCP
from mcp.types import Tool

# --- 1. Load and Prepare Data ---
try:
    df = pd.read_json("Sections.json")
    df.dropna(subset=['SectionName'], inplace=True)
except Exception as e:
    print(f"❌ Error loading Sections.json: {e}")
    df = pd.DataFrame()

# --- 2. Helper Function for Time Parsing ---
def get_start_hour(meeting_pattern):
    if not isinstance(meeting_pattern, str):
        return None
    match = re.search(r'(\d{1,2}:\d{2}\s*(?:AM|PM))', meeting_pattern)
    if not match:
        return None
    time_str = match.group(1)
    try:
        return pd.to_datetime(time_str, format='%I:%M %p').hour
    except ValueError:
        return None

# --- 3. Create the MCP Service Object ---
mcp = FastMCP("course_advisor")

# --- 4. Define Tools Using the @mcp.tool() Decorator ---
@mcp.tool()
def find_sections_by_department(department: str) -> list[dict]:
    """Finds all course sections for a given department code (Subject_RefID)."""
    if df.empty:
        return [{"error": "Course data is not available."}]
    results_df = df[df['Subject_RefID'].astype(str).str.strip().str.upper() == str(department).strip().upper()]
    if not results_df.empty:
        return results_df[['SectionName', 'SectionTitle', 'Instructors']].fillna('N/A').to_dict('records')
    return []

@mcp.tool()
def find_sections_by_level(level: str) -> list[dict]:
    """Finds all course sections at a specific level (e.g., '100', '200')."""
    if df.empty:
        return [{"error": "Course data is not available."}]
    clean_levels = pd.to_numeric(df['CourseLevel'], errors='coerce').fillna(-1).astype(int).astype(str)
    results_df = df[clean_levels == str(level).strip()]
    if not results_df.empty:
        return results_df[['SectionName', 'SectionTitle', 'Instructors']].fillna('N/A').to_dict('records')
    return []

@mcp.tool()
def find_sections_by_time(time_of_day: str) -> list[dict]:
    """Finds sections offered in the morning, afternoon, or evening."""
    if df.empty:
        return [{"error": "Course data is not available."}]
    df_temp = df.copy()
    df_temp['start_hour'] = df_temp['MeetingPatterns'].apply(get_start_hour)
    df_temp.dropna(subset=['start_hour'], inplace=True)
    df_temp['start_hour'] = df_temp['start_hour'].astype(int)
    time_of_day = time_of_day.lower()
    results_df = pd.DataFrame()
    if time_of_day == 'morning':
        results_df = df_temp[df_temp['start_hour'] < 12]
    elif time_of_day == 'afternoon':
        results_df = df_temp[(df_temp['start_hour'] >= 12) & (df_temp['start_hour'] < 17)]
    elif time_of_day == 'evening':
        results_df = df_temp[df_temp['start_hour'] >= 17]
    if not results_df.empty:
        return results_df[['SectionName', 'SectionTitle', 'Instructors', 'MeetingPatterns']].fillna('N/A').to_dict('records')
    return []

# --- 5. Run the MCP Service ---
if __name__ == "__main__":
    mcp.run()
