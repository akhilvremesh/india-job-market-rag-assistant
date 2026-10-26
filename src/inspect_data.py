import pandas as pd

# Load the CSV into a pandas DataFrame (a table of rows and columns).
df = pd.read_csv("data/raw/naukri_data.csv")

# Show the number of rows and columns.
rows, columns = df.shape
print(f"Rows: {rows}")
print(f"Columns: {columns}")
print(f"Column names: {df.columns.tolist()}")

# Count blank or missing values in each column.
print("\nMissing values per column:")
print(df.isna().sum().to_string())

# Count repeated job IDs, if the expected ID column exists.
if "Uniq Id" in df.columns:
    duplicate_ids = df.duplicated(subset=["Uniq Id"]).sum()
    print(f"\nDuplicate Uniq Id values: {duplicate_ids}")
else:
    print("\nCould not check duplicates: 'Uniq Id' column was not found.")

# Convert the crawl timestamps to dates; unparseable values become missing.
if "Crawl Timestamp" in df.columns:
    crawl_dates = pd.to_datetime(df["Crawl Timestamp"], errors="coerce")
    valid_dates = crawl_dates.dropna()

    print(f"Unparseable crawl timestamps: {crawl_dates.isna().sum()}")

    if not valid_dates.empty:
        print(f"Earliest crawl timestamp: {valid_dates.min()}")
        print(f"Latest crawl timestamp: {valid_dates.max()}")
    else:
        print("No crawl timestamps could be parsed.")
else:
    print("\nCould not check dates: 'Crawl Timestamp' column was not found.")