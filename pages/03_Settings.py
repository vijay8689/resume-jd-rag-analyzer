import streamlit as st

from src.config.settings import settings
from src.ui.page_header import render_footer, render_page_header

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")
render_page_header("Settings", "Tune the matching thresholds and runtime behavior of the analyzer.")

st.subheader("Model Runtime")
model_columns = st.columns(3)
model_columns[0].metric("LLM Status", "Enabled" if settings.llm_enabled else "Disabled")
model_columns[1].metric("Top-K Retrieval", settings.top_k)
model_columns[2].metric("Upload Limit", f"{settings.max_upload_size_kb} KB")

st.dataframe(
	[
		{"Setting": "LLM model", "Value": settings.model_name, "Purpose": "Generates optional reasoning and structured analysis."},
		{"Setting": "Provider endpoint", "Value": settings.openai_api_base, "Purpose": "OpenAI-compatible model endpoint."},
		{"Setting": "Embedding model", "Value": settings.embedding_model, "Purpose": "Creates vector representations for resume chunks."},
		{"Setting": "Vector collection", "Value": settings.chroma_collection_name, "Purpose": "Stores searchable resume chunks."},
		{"Setting": "Chunk size", "Value": f"{settings.chunk_size} characters", "Purpose": "Maximum text size used for each resume chunk."},
		{"Setting": "Chunk overlap", "Value": f"{settings.chunk_overlap} characters", "Purpose": "Context repeated between oversized chunks."},
	],
	use_container_width=True,
	hide_index=True,
)

st.subheader("Similarity Matching")
threshold_columns = st.columns(2)
threshold_columns[0].metric("Match Threshold", f"{settings.match_threshold:.2f}")
threshold_columns[1].metric("Partial Threshold", f"{settings.partial_threshold:.2f}")
st.info(
	"Similarity is calculated from the closest Chroma vector result. "
	f"Scores at or above {settings.match_threshold:.2f} are MATCHED; scores from "
	f"{settings.partial_threshold:.2f} up to {settings.match_threshold:.2f} are PARTIAL; "
	"lower scores are MISSING. Exact text matches are treated as high-confidence matches."
)

with st.expander("How the score is calculated"):
	st.write("Mandatory requirements have the highest weight, preferred requirements have medium weight, and optional requirements have the lowest weight.")
	st.write("Overall Match combines those weighted skill statuses: MATCHED = 100%, PARTIAL = 50%, and MISSING = 0% for each requirement weight.")

render_footer()
