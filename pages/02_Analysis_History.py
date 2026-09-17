import streamlit as st

from src.ui.page_header import render_footer, render_page_header

st.set_page_config(page_title="Analysis History", page_icon="🕘", layout="wide")
render_page_header("Analysis History", "Review the match profile of every completed analysis in this session.")

history = st.session_state.get("analysis_history", [])
if not history:
	st.info("Completed analyses will appear here after you analyze a job description.")
	st.stop()

rows = [
	{
		"Analyzed": item.get("timestamp", ""),
		"Resume": item.get("resume", "Unknown"),
		"Job Title": item.get("job_title", "Not detected"),
		"Overall Match": f"{float(item.get('overall_match_percentage', 0)):.1f}%",
		"Matched": item.get("matched_count", 0),
		"Partial": item.get("partial_count", 0),
		"Missing": item.get("missing_count", 0),
	}
	for item in reversed(history)
]
st.dataframe(rows, use_container_width=True, hide_index=True)

selected = st.selectbox(
	"View analysis details",
	options=list(range(len(history))),
	format_func=lambda index: f"{history[index].get('timestamp', '')} - {history[index].get('job_title', 'Not detected')}",
)
selected_result = history[selected].get("result", {})
st.subheader("Selected Analysis")
metric_columns = st.columns(4)
metric_columns[0].metric("Overall Match", f"{selected_result.get('overall_match_percentage', 0):.1f}%")
metric_columns[1].metric("Matched", selected_result.get("matched_count", 0))
metric_columns[2].metric("Partial", selected_result.get("partial_count", 0))
metric_columns[3].metric("Missing", selected_result.get("missing_count", 0))

detail_columns = st.columns(3)
with detail_columns[0]:
	st.write("**Matched Skills**")
	st.write(", ".join(item.get("skill", "") for item in selected_result.get("matched_skills", [])) or "None")
with detail_columns[1]:
	st.write("**Partial Skills**")
	st.write(", ".join(item.get("skill", "") for item in selected_result.get("partial_skills", [])) or "None")
with detail_columns[2]:
	st.write("**Missing Skills**")
	st.write(", ".join(item.get("skill", "") for item in selected_result.get("missing_skills", [])) or "None")

render_footer()
