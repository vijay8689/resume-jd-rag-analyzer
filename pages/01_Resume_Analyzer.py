import streamlit as st

from src.ui.page_header import render_footer, render_page_header

st.set_page_config(page_title="Resume Analyzer", page_icon="📊", layout="wide")
render_page_header("Resume Analyzer", "Explore match signals, skill gaps, and evidence from the latest analysis.")

result = st.session_state.get("analysis_result")
if not result:
	st.info("Upload a resume and analyze a job description from the main page to view results here.")
	st.stop()

st.caption(f"Resume: {st.session_state.get('resume_filename', 'Unknown')} | Job title: {result.get('job_title', 'Not detected')}")

summary_columns = st.columns(4)
summary_columns[0].metric("Overall Match", f"{result.get('overall_match_percentage', 0):.1f}%")
summary_columns[1].metric("Matched Skills", result.get("matched_count", 0))
summary_columns[2].metric("Partial Skills", result.get("partial_count", 0))
summary_columns[3].metric("Missing Skills", result.get("missing_count", 0))

tabs = st.tabs(["Overview", "Skills", "Keywords", "Experience", "Roadmap", "Suggestions", "Evidence"])

with tabs[0]:
	overview_columns = st.columns(3)
	overview_columns[0].metric("Keyword Match", f"{result.get('keyword_match_percentage', 0):.1f}%")
	overview_columns[1].metric("Mandatory Skills", f"{result.get('mandatory_skill_percentage', 0):.1f}%")
	overview_columns[2].metric("Experience Match", f"{result.get('experience_match_percentage', 0):.1f}%")
	st.subheader("Top Matching Skills")
	st.write(", ".join(result.get("top_matching_skills", [])) or "No matching skills found.")
	st.subheader("Key Gaps")
	st.write(", ".join(result.get("key_gaps", [])) or "No skill gaps found.")

with tabs[1]:
	for title, key, empty_message in [
		("Matched Skills", "matched_skills", "No matched skills found."),
		("Partial Skills", "partial_skills", "No partial skills found."),
		("Missing Skills", "missing_skills", "No missing skills found."),
	]:
		st.subheader(title)
		skills = result.get(key, [])
		if skills:
			st.dataframe(
				[
					{
						"Skill": item.get("skill", ""),
						"Status": item.get("status", ""),
						"Priority": item.get("priority", ""),
						"Similarity": round(float(item.get("similarity_score", 0)) * 100, 1),
						"Experience": item.get("experience_status", ""),
					}
					for item in skills
				],
				use_container_width=True,
				hide_index=True,
			)
		else:
			st.info(empty_message)

with tabs[2]:
	keyword_columns = st.columns(2)
	with keyword_columns[0]:
		st.subheader("Present Keywords")
		st.write(", ".join(result.get("present_keywords", [])) or "None")
	with keyword_columns[1]:
		st.subheader("Missing Keywords")
		st.write(", ".join(result.get("missing_keywords", [])) or "None")

with tabs[3]:
	experience = result.get("experience_analysis", [])
	if experience:
		st.dataframe(experience, use_container_width=True, hide_index=True)
	else:
		st.info("No experience requirements were detected.")

with tabs[4]:
	roadmap = result.get("learning_resources", {})
	if isinstance(roadmap, dict):
		for skill, resources in roadmap.items():
			st.subheader(skill)
			for resource in resources if isinstance(resources, list) else [resources]:
				if isinstance(resource, dict) and resource.get("url"):
					st.markdown(f"- [{resource.get('title', resource['url'])}]({resource['url']})")
				else:
					st.write(resource)
	elif roadmap:
		st.write(roadmap)
	else:
		st.info("No learning resources are needed.")

with tabs[5]:
	suggestions = result.get("resume_suggestions", [])
	if suggestions:
		for suggestion in suggestions:
			st.write(f"- {suggestion}")
	else:
		st.info("No resume suggestions available.")

with tabs[6]:
	evidence = result.get("evidence", [])
	if evidence:
		st.dataframe(evidence, use_container_width=True, hide_index=True)
	else:
		st.info("No evidence was generated.")

render_footer()
