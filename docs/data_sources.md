# Data Sources

## Naukri.com Job Postings

- **Dataset:** Jobs on Naukri.com
- **Kaggle page:** https://www.kaggle.com/datasets/promptcloud/jobs-on-naukricom
- **Publisher named on the data card:** PromptCloud and DataStock
- **Source domain:** naukri.com
- **License stated on the data card:** CC0 1.0 Public Domain
- **File used:** `data/raw/naukri_data.csv`
- **Rows in the downloaded file:** 30,000
- **Rows in the cleaned database table:** 29,425
- **Duplicate job IDs found:** 0
- **Rows without a job title removed:** 575
- **Crawl timestamps observed in the downloaded file:** 2019-07-04 to 2019-08-06

## Available fields

Uniq Id, Crawl Timestamp, Job Title, Job Salary, Job Experience Required,
Key Skills, Role Category, Location, Functional Area, Industry, Role

## Notes and limitations

The data card reports 484,879 total records and also describes a sample of up
to 30,000 records. The downloaded file used here contains 30,000 rows.

The data card gives a date range of 2019-07-01 to 2019-08-30. The timestamps
observed in this downloaded file are crawl timestamps, not necessarily the
original job-posting dates.

This is a historical dataset, not a source of currently open jobs. It has no
full job descriptions or company-name field. The Key Skills field includes
business and role-related tags as well as technical skills.

The data card states a CC0 1.0 license. This project records the license stated
by the source and links back to the Kaggle page.