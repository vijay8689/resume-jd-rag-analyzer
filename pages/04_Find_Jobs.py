import streamlit as st

from src.services.job_search_service import find_jobs, search_api_key
from src.ui.page_header import render_footer, render_page_header

st.set_page_config(page_title="Find Jobs", page_icon=":material/work:", layout="wide")
render_page_header("Find Jobs", "Discover roles on LinkedIn and Naukri, then follow the listing to apply.", tone="blue")

with st.form("job_search_form"):
    roles_text = st.text_input("Job roles", placeholder="Python Developer, Data Engineer", max_chars=504, help="Enter up to five roles separated by commas.")
    location = st.text_input("Location", value="India", placeholder="City or country", max_chars=100)
    submitted = st.form_submit_button("Find jobs", type="primary")

if submitted:
    try:
        with st.spinner("Finding matching roles..."):
            st.session_state.job_search_results = find_jobs(roles_text.split(','), location, search_api_key())
    except ValueError as exc:
        st.session_state.pop("job_search_results", None)
        st.warning(str(exc))

results = st.session_state.get("job_search_results")
if results:
    st.caption(f"Searched {results['searched_at']} · Location: {results['location'] or 'Any location'}")
    st.caption("Listings may expire. Confirm role details and submit your application on the job site; sign-in may be required.")
    for group in results['groups']:
        with st.container(border=True):
            st.subheader(f"{group['source']} · {group['role']}")
            st.link_button(f"Search {group['source']}", group['search_url'])
            if group['notice']:
                st.info(group['notice'])
            for job in group['jobs']:
                with st.container(border=True):
                    st.text(job['title'])
                    details = [job.get('company'), job.get('location'), job.get('posted')]
                    st.caption(" · ".join(value for value in details if value))
                    if job.get('snippet'):
                        st.text(job['snippet'])
                    if job.get('indexed'):
                        st.caption("Search-index listing · availability not verified")
                    st.link_button(f"View & apply on {group['source']}", job['url'], type="primary")
else:
    st.info("Enter the roles you want to explore, choose a location, and select Find jobs.")

with st.expander("About job sources"):
    st.write("LinkedIn listings come from its public search when available. Naukri search links always open the matching search on Naukri.")
    st.write("To display indexed Naukri listings here, configure SERPAPI_API_KEY in your local .env, environment, or Streamlit secrets. Search-provider usage may incur charges. Only role and location search terms are sent; your resume is not used for this search.")

render_footer()
