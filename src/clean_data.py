import sqlite3
import pandas as pd

# Connect to the SQLite database.
connection = sqlite3.connect("data/jobs.db")

# Load the raw postings table into a pandas DataFrame.
df = pd.read_sql_query("SELECT * FROM job_postings_raw", connection)
rows_before = len(df)

# Trim spaces from text columns and convert blank text to missing values.
text_columns = [
    "Crawl Timestamp",
    "Job Title",
    "Job Salary",
    "Job Experience Required",
    "Key Skills",
    "Role Category",
    "Location",
    "Functional Area",
    "Industry",
    "Role",
]
for column in text_columns:
    df[column] = df[column].str.strip()
    df[column] = df[column].replace("", pd.NA)

# Remove repeated job IDs, keeping the first copy.
df = df.drop_duplicates(subset=["Uniq Id"], keep="first")
duplicates_removed = rows_before - len(df)

# Remove postings without a title; keep missing salary, skills, and location.
rows_before_title_filter = len(df)
df = df.dropna(subset=["Job Title"])
missing_titles_removed = rows_before_title_filter - len(df)

# Save the cleaned copy, replacing it if this script is run again.
df.to_sql("job_postings_clean", connection, if_exists="replace", index=False)

# Verify the number of rows saved in SQLite.
saved_rows = connection.execute(
    "SELECT COUNT(*) FROM job_postings_clean"
).fetchone()[0]

print(f"Rows in raw table: {rows_before}")
print(f"Duplicate IDs removed: {duplicates_removed}")
print(f"Rows without a title removed: {missing_titles_removed}")
print(f"Rows saved in clean table: {saved_rows}")

connection.close()
