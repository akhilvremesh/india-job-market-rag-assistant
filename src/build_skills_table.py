import sqlite3
import pandas as pd
from skill_extractor import parse_key_skills

# Open the database created by load_data.py.
connection = sqlite3.connect("data/jobs.db")

# Read the ID and skills columns; give the ID a simple name for the new table.
skill_data = pd.read_sql_query(
    'SELECT "Uniq Id" AS job_id, "Key Skills" FROM job_postings_clean',
    connection,
)

# Apply your function to each skills cell, then make one row per skill.
skill_data["skill"] = skill_data["Key Skills"].apply(parse_key_skills)
skill_data = skill_data[["job_id", "skill"]].explode("skill")

# Remove empty entries and repeated job-skill pairs.
skill_data = skill_data.dropna(subset=["skill"])
skill_data["skill"] = skill_data["skill"].str.strip().str.lower()
skill_data = skill_data[skill_data["skill"] != ""]
skill_data = skill_data.drop_duplicates(subset=["job_id", "skill"])

# Save the pairs as a SQLite table, replacing it if the script is rerun.
skill_data.to_sql("job_skills", connection, if_exists="replace", index=False)

# Verify how many job-skill pairs and distinct skill names were saved.
pair_count = connection.execute(
    "SELECT COUNT(*) FROM job_skills"
).fetchone()[0]

skill_count = connection.execute(
    "SELECT COUNT(DISTINCT skill) FROM job_skills"
).fetchone()[0]

print(f"Job-skill rows saved: {pair_count}")
print(f"Distinct skill names: {skill_count}")

connection.close()
