import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Job Market Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("Job Market Dashboard")
st.caption("Historical Naukri postings from 2019.")


# Load summary counts, salary statistics, and top locations.
try:
    response = requests.get(
        f"{API_URL}/dashboard/summary",
        timeout=15,
    )
    response.raise_for_status()
    summary = response.json()

    # Display four headline metrics.
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Job postings", f"{summary['total_postings']:,}")
    col2.metric("With salary data", f"{summary['postings_with_salary']:,}")
    col3.metric(
        "Median listed salary",
        f"{summary['median_salary_lpa']:.2f} LPA",
    )
    col4.metric(
        "Mean listed salary",
        f"{summary['mean_salary_lpa']:.2f} LPA",
    )

    # Plot the number of postings in the ten most common locations.
    st.subheader("Postings by location")
    locations = summary["top_locations"]

    st.bar_chart(
        {
            item["location"]: item["posting_count"]
            for item in locations
        }
    )
    st.dataframe(
        locations,
        hide_index=True,
        use_container_width=True,
    )

except requests.RequestException as error:
    st.error(f"Could not load dashboard summary from the API: {error}")


# Let users filter technical skill demand by role and city.
st.subheader("Technical skill demand by role and city")

role_options = [
    "All roles",
    "Software Developer",
    "Team Lead/Technical Lead",
    "Testing Engineer",
    "Data Analyst",
]
location_options = [
    "All cities",
    "Bengaluru",
    "Mumbai",
    "Pune",
    "Hyderabad",
    "Chennai",
]

filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    selected_role = st.selectbox("Role", role_options)

with filter_col2:
    selected_location = st.selectbox("City", location_options)

# Pass selected filters to the skills endpoint.
params = {}

if selected_role != "All roles":
    params["role"] = selected_role

if selected_location != "All cities":
    params["location"] = selected_location

try:
    skills_response = requests.get(
        f"{API_URL}/dashboard/skills",
        params=params,
        timeout=20,
    )
    skills_response.raise_for_status()
    skill_rows = skills_response.json()["skills"]

    if skill_rows:
        st.bar_chart(
            {
                item["skill"]: item["posting_count"]
                for item in skill_rows
            }
        )
        st.dataframe(
            skill_rows,
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.info("No recognized technical skills were found for these filters.")

except requests.RequestException as error:
    st.error(f"Could not load skill demand data from the API: {error}")


# Show median listed salary for each experience band.
st.subheader("Listed salary by experience")

try:
    salary_response = requests.get(
        f"{API_URL}/dashboard/salary-by-experience",
        timeout=20,
    )
    salary_response.raise_for_status()
    salary_rows = salary_response.json()["salary_by_experience"]

    if salary_rows:
        st.bar_chart(
            {
                row["experience_band"]: row["median_salary_lpa"]
                for row in salary_rows
            }
        )
        st.dataframe(
            salary_rows,
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.info("No salary records with parsed experience were found.")

except requests.RequestException as error:
    st.error(f"Could not load salary-by-experience data: {error}")


st.info(
    "These are historical 2019 postings and salary listings, "
    "not current vacancies or current market rates."
)