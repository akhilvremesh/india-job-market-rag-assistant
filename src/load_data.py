import pandas as pd
import sqlite3

# Read the CSV into a table in Python.
df = pd.read_csv("data/raw/naukri_data.csv")

# Open or create the SQLite database file.
connection = sqlite3.connect("data/jobs.db")

# Copy the CSV data into a table inside the database.
# "replace" lets you rerun the script without creating duplicate tables.
df.to_sql(
    name="job_postings_raw",
    con=connection,
    if_exists="replace",
    index=False,
)

# Ask SQLite to count the saved rows and print the result.
result = connection.execute("SELECT COUNT(*) FROM job_postings_raw")
row_count = result.fetchone()[0]
print(f"Rows stored in database: {row_count}")

# Close the connection when finished.
connection.close()