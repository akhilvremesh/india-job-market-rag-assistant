# Job Market RAG Assistant for India

An assistant that searches Indian job postings, answers questions with cited sources,
and compares a resume with a job description.

## Planned features

- Search job postings and answer questions with citations
- Match a resume to a job description and identify missing skills
- Explore job-market patterns
- Provide an API and a simple web interface

## Setup

Python 3.11 is required. Create and activate a virtual environment, then install
the dependencies listed in `requirements.txt`.

## Data and privacy

The project will use public or manually collected postings from permitted sources.
API keys and private resume data must not be committed to the repository.

## Dataset snapshot and initial findings

This project currently uses 29,425 cleaned postings from a 30,000-row
Naukri.com dataset. The downloaded data is a historical 2019 sample, not a
feed of current job openings.

- 575 postings without a job title were removed; no duplicate job IDs were found.
- Software Developer was the most common role, with 6,396 postings (about 21.7%).
- Bengaluru was the most common location, with 5,215 postings (about 17.7%).
- Bengaluru, Mumbai, and Pune together had 11,119 postings (about 37.8%).
- JavaScript appeared in 2,254 postings, SQL in 1,560, and Python in 1,177.

These are findings about this dataset, not current Indian hiring demand. The
data has no full job descriptions or company names, and its Key Skills field
includes business and role-related tags as well as technical skills.

See [data_sources.md](docs/data_sources.md) for the source and data limitations.