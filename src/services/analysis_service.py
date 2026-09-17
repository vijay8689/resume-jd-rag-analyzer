from __future__ import annotations

from typing import Any

from src.config.settings import settings
from src.jd.jd_parser import parse_jd
from src.jd.keyword_extractor import extract_keywords
from src.matching.exact_matcher import exact_match
from src.matching.experience_matcher import compare_experience, extract_resume_experience
from src.vectorstore.chroma_manager import get_chroma_manager
from src.matching.scoring_engine import calculate_weighted_score
from src.resources.resource_manager import get_resource_manager


class AnalysisService:
    def analyze_resume_against_jd(self, session_id: str, document_id: str, jd_text: str) -> dict[str, Any]:
        """Perform deterministic analysis of the uploaded resume versus the supplied JD."""
        parsed = parse_jd(jd_text)
        requirements = parsed["requirements"]
        resume_text = self._get_resume_text(session_id, document_id)

        matched_skills = []
        partial_skills = []
        missing_skills = []
        evidence = []

        for item in requirements:
            skill = item["skill"]
            status = "MISSING"
            similarity_score = 0.0

            if exact_match(skill, resume_text):
                status = "MATCHED"
                similarity_score = 0.95
            else:
                manager = get_chroma_manager()
                query = manager.query(
                    skill,
                    where={
                        "$and": [
                            {"session_id": session_id},
                            {"document_id": document_id},
                        ]
                    },
                    n_results=settings.top_k,
                )
                document_batches = query.get("documents") or []
                distance_batches = query.get("distances") or []
                docs = document_batches[0] if document_batches else []
                distances = distance_batches[0] if distance_batches else []
                if docs and distances:
                    # Chroma returns cosine distance; convert the closest result
                    # to a bounded similarity score before applying thresholds.
                    similarity_score = max(0.0, min(1.0, 1.0 - float(distances[0])))
                    if similarity_score >= settings.match_threshold:
                        status = "MATCHED"
                    elif similarity_score >= settings.partial_threshold:
                        status = "PARTIAL"

            resume_experience = extract_resume_experience(resume_text, skill)
            required_exp = item.get("required_experience")
            experience_status = compare_experience(required_exp, resume_experience)

            match_item = {
                "skill": skill,
                "category": item.get("category", "General"),
                "priority": item.get("priority", "MANDATORY"),
                "status": status,
                "confidence": "HIGH" if status == "MATCHED" else "MEDIUM" if status == "PARTIAL" else "LOW",
                "similarity_score": similarity_score,
                "jd_evidence": item.get("source_text", skill),
                "resume_evidence": resume_text[:200] if status != "MISSING" else "Not found",
                "required_experience": required_exp,
                "resume_experience": resume_experience,
                "experience_status": experience_status,
            }

            if status == "MATCHED":
                matched_skills.append(match_item)
            elif status == "PARTIAL":
                partial_skills.append(match_item)
            else:
                missing_skills.append(match_item)

            evidence.append(
                {
                    "skill": skill,
                    "status": status,
                    "confidence": match_item["confidence"],
                    "jd_evidence": item.get("source_text", skill),
                    "resume_evidence": match_item["resume_evidence"],
                    "source_section": "Professional Experience",
                    "source_page": 1,
                    "similarity_score": similarity_score,
                }
            )

        present_keywords = extract_keywords(jd_text)
        missing_keywords = [keyword for keyword in present_keywords if keyword.lower() not in resume_text.lower()] if present_keywords else []
        related_keywords = []

        result_rows = [
            {"priority": item["priority"], "status": item["status"]}
            for item in matched_skills + partial_skills + missing_skills
        ]
        overall_percentage = calculate_weighted_score(result_rows) if result_rows else 0.0

        resource_manager = get_resource_manager()
        roadmap = resource_manager.build_learning_roadmap([item["skill"] for item in missing_skills])
        suggestions = [
            f"Consider clearly mentioning '{item['skill']}' in the relevant experience section."
            for item in missing_skills[:3]
        ]

        return {
            "overall_match_percentage": overall_percentage,
            "matched_percentage": round((len(matched_skills) / max(len(requirements), 1)) * 100, 1),
            "partial_percentage": round((len(partial_skills) / max(len(requirements), 1)) * 100, 1),
            "missing_percentage": round((len(missing_skills) / max(len(requirements), 1)) * 100, 1),
            "keyword_match_percentage": 100.0 if not present_keywords else round((len(present_keywords) - len(missing_keywords)) / len(present_keywords) * 100, 1),
            "mandatory_skill_percentage": 100.0 if not requirements else round((sum(1 for item in matched_skills if item["priority"] == "MANDATORY") / max(sum(1 for item in requirements if item["priority"] == "MANDATORY"), 1)) * 100, 1),
            "experience_match_percentage": 100.0 if not requirements else round((sum(1 for item in matched_skills if item["experience_status"] == "MEETS_REQUIREMENT") / max(len(requirements), 1)) * 100, 1),
            "matched_skills": matched_skills,
            "partial_skills": partial_skills,
            "missing_skills": missing_skills,
            "present_keywords": present_keywords,
            "missing_keywords": missing_keywords,
            "related_keywords": related_keywords,
            "matched_count": len(matched_skills),
            "partial_count": len(partial_skills),
            "missing_count": len(missing_skills),
            "top_matching_skills": [item["skill"] for item in matched_skills[:5]],
            "key_gaps": [item["skill"] for item in missing_skills[:5]],
            "learning_resources": roadmap,
            "resume_suggestions": suggestions,
            "experience_analysis": [
                {
                    "skill": item["skill"],
                    "required": item["required_experience"],
                    "resume": item["resume_experience"],
                    "status": item["experience_status"],
                }
                for item in matched_skills + partial_skills + missing_skills
            ],
            "evidence": evidence,
            "job_title": parsed["metadata"].get("job_title", "Not detected"),
            "company": parsed["metadata"].get("company", "Not specified"),
            "location": parsed["metadata"].get("location", "Not detected"),
        }

    def _get_resume_text(self, session_id: str, document_id: str) -> str:
        """Read all document chunks for the current session and document."""
        manager = get_chroma_manager()
        results = manager.collection.get(
            where={
                "$and": [
                    {"session_id": session_id},
                    {"document_id": document_id},
                ]
            },
            include=["documents", "metadatas"],
        )
        docs = results.get("documents") or []
        return "\n\n".join(str(doc) for doc in docs)
