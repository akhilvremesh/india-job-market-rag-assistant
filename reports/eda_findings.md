# Exploratory Data Analysis Findings

## Dataset and cleaning

- The downloaded sample contained 30,000 Naukri job postings.
- The cleaned table contains 29,425 postings after removing rows with blank
  job titles. No duplicate posting IDs remained.
- The observed crawl timestamps in this sample range from July 4 to
  August 6, 2019.
- The dataset is historical and should not be used to describe current
  vacancies or current hiring demand.

## Skills by role

Among the recognized technical skills for Software Developer postings, the
most frequent were:

| Skill | Postings |
|---|---:|
| JavaScript | 1,722 |
| SQL | 1,433 |
| Java | 1,140 |
| HTML | 1,065 |
| MySQL | 740 |

These results come from the curated technical-skill matcher, which recognizes
26 skill names. Skills outside that list are not included.

## Posting demand by location

The most frequent location labels were Bengaluru (6,664 postings), Mumbai
(4,918), Pune (3,347), Hyderabad (3,159), and Gurgaon (2,813).

A posting that lists multiple locations is counted once in each listed
location. Therefore, location counts can add up to more than the number of
unique postings. Delhi NCR is retained as a regional label separate from
Delhi.

For example, among recognized technical skills in Bengaluru postings, SQL
appeared in 625 postings, JavaScript in 591, Java in 558, Python in 457, and
HTML in 382.

## Salary and experience

For the 7,729 postings with both a parsed salary and parsed experience
midpoint, the median salary midpoint increased across experience bands:

| Experience midpoint band | Postings | Median salary midpoint |
|---|---:|---:|
| Up to 2 years | 1,908 | 2.25 LPA |
| Over 2 to 5 years | 3,324 | 3.50 LPA |
| Over 5 to 10 years | 1,919 | 8.00 LPA |
| Over 10 years | 578 | 16.50 LPA |

Salary ranges are represented by their midpoint, and experience ranges are
represented by their midpoint. These are approximations. The stricter salary
parser leaves entries without a clear salary unit or period unparsed.

## Limitations

- This is a 2019 sample, not a live feed of currently available jobs.
- The salary analysis covers only postings where both salary and experience
  could be parsed.
- The matcher recognizes a curated set of 26 technical skills, not every
  skill mentioned in the source data.
- Location counts include multi-location postings once for each location
  listed.
- These are descriptive patterns in this dataset; they do not show that
  experience or location causes a particular salary or skill demand.

## Charts

- `figures/top_job_locations.png`
- `figures/software_developer_skills.png`
- `figures/salary_by_experience.png`