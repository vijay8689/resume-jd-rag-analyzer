# Resume AI Match Analyzer
## Complete Code Generation Prompt

---

# 1. ROLE

You are a senior Python architect, RAG engineer, LangChain developer, Streamlit developer, and QA automation architect.

Build a complete, production-quality, GitHub-ready application named:

**Resume AI Match Analyzer**

The application is a RAG-based Resume vs Job Description analyzer.

The application must be:

- Python based
- Streamlit based
- LangChain based
- ChromaDB based
- OpenAI-compatible
- Qwen based
- Deployable to Streamlit Cloud/shared Streamlit environment
- Modular
- Testable
- Secure
- Explainable
- Cost-conscious

Do not generate a prototype with placeholder functions.

Generate working code for every core feature.

---

# 2. BUSINESS OBJECTIVE

Build a web application where a user can:

1. Upload a resume.
2. Extract all resume information.
3. Detect resume sections.
4. Chunk resume content.
5. Generate embeddings.
6. Store chunks in ChromaDB.
7. Paste a Job Description.
8. Analyze the JD against the resume.
9. Identify matching skills.
10. Identify partially matching skills.
11. Identify missing skills.
12. Identify missing keywords.
13. Compare required experience against resume experience.
14. Calculate an overall match percentage.
15. Calculate detailed match percentages.
16. Show evidence from the resume.
17. Explain why a skill matched.
18. Explain why a skill is missing.
19. Recommend learning resources for missing skills.
20. Provide clickable learning hyperlinks.
21. Provide resume optimization suggestions.
22. Export the complete analysis.
23. Support multiple JD analyses against the same resume.
24. Maintain session isolation between users.

---

# 3. TECHNOLOGY STACK

Use:

```text
Python 3.11+
Streamlit
LangChain
LangChain OpenAI integration
ChromaDB
Sentence Transformers
PyMuPDF
python-docx
Pydantic
PyYAML
Plotly
Pandas
OpenPyXL
ReportLab
python-dotenv
pytest
```

Do not introduce unnecessary frameworks.

The application should initially be a Streamlit application rather than FastAPI + React.

---

# 4. LLM PROVIDER

Use the following OpenAI-compatible XKIRO endpoint.

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.xkiro.com/v1",
    api_key=API_KEY
)

response = client.chat.completions.create(
    model="qwen/qwen3.7-flash:free",
    messages=[
        {
            "role": "user",
            "content": "Hello!"
        }
    ]
)

print(response.choices[0].message.content)
```

The application must use:

```text
Model:
qwen/qwen3.7-flash:free

Base URL:
https://api.xkiro.com/v1
```

Never hard-code the API key.

---

# 5. API KEY MANAGEMENT

For local development support:

```text
.env
```

Example:

```env
XKIRO_API_KEY=your-api-key
```

For Streamlit deployment use:

```text
.streamlit/secrets.toml
```

Example:

```toml
XKIRO_API_KEY = "your-api-key"
```

Python:

```python
import streamlit as st

api_key = st.secrets["XKIRO_API_KEY"]
```

Fallback to environment variable:

```python
import os

api_key = st.secrets.get(
    "XKIRO_API_KEY",
    os.getenv("XKIRO_API_KEY")
)
```

Never commit:

```text
.env
.streamlit/secrets.toml
```

Add both to `.gitignore`.

---

# 6. LLM ARCHITECTURE

Do not tightly couple the application to Qwen.

Create an abstraction:

```python
class LLMProvider:
    def generate(self, prompt: str) -> str:
        raise NotImplementedError
```

Implement:

```text
XKiroQwenProvider
```

Create:

```text
src/llm/llm_client.py
```

Expose:

```python
get_llm()
```

The rest of the application must not directly instantiate the Qwen client.

---

# 7. LLM RESPONSIBILITIES

Use the LLM for:

- Job Description requirement extraction
- Skill extraction
- Requirement classification
- Contextual skill matching
- Match explanations
- Resume improvement suggestions
- Learning roadmap generation

Do NOT use the LLM for:

- Final percentage calculation
- Basic exact keyword detection
- ChromaDB operations
- File parsing
- Determining factual resume information without evidence

The final score must be calculated by deterministic Python code.

---

# 8. EMBEDDING MODEL

Use a local embedding model.

Default:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Create:

```text
src/embeddings/embedding_service.py
```

Expose:

```python
get_embedding_model()
```

The embedding model should be loaded once using:

```python
@st.cache_resource
```

or an equivalent application-level cache.

Do not use the Qwen LLM for embeddings.

---

# 9. RAG ARCHITECTURE

Implement the following architecture:

```text
                        RESUME
                           |
                           v
                    File Upload
                           |
                           v
                   Text Extraction
                           |
                           v
                    Text Cleaning
                           |
                           v
                  Section Detection
                           |
                           v
                   Smart Chunking
                           |
                           v
                    Embeddings
                           |
                           v
                       ChromaDB
                           |
                           |
                           |
JOB DESCRIPTION ----------+
                           |
                           v
                 JD Requirement Parser
                           |
                           v
                    Skill Extraction
                           |
                           v
                  Skill Normalization
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
        Exact Match   Vector Search   LLM Reasoning
             |             |             |
             +-------------+-------------+
                           |
                           v
                  Hybrid Match Engine
                           |
                           v
                  Experience Analysis
                           |
                           v
                   Keyword Analysis
                           |
                           v
                    Scoring Engine
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
          Matched       Partial       Missing
             |             |             |
             +-------------+-------------+
                           |
                           v
                  Learning Resources
                           |
                           v
                     Streamlit UI
```

---

# 10. RESUME UPLOAD

Create a resume upload component.

Supported:

```text
PDF
DOCX
TXT
```

Maximum size:

```text
10 MB
```

UI:

```text
Resume Upload

[ Drag and Drop Resume ]

Supported formats:
PDF | DOCX | TXT

[ Upload Resume ]
```

After upload display:

```text
✓ Resume uploaded

Filename:
Vijay_Kumar_Resume.pdf

File type:
PDF

Pages:
4

Characters:
12,453

Sections:
7

Chunks:
42

Vector Database:
Indexed
```

---

# 11. RESUME PROCESSING PIPELINE

Implement:

```text
Upload
  ↓
Validate File
  ↓
Extract Text
  ↓
Clean Text
  ↓
Detect Sections
  ↓
Chunk Content
  ↓
Generate Embeddings
  ↓
Store in ChromaDB
```

Show progress using Streamlit.

---

# 12. PDF PROCESSING

Use PyMuPDF.

Extract:

- Page text
- Headings
- Paragraphs
- Bullet points
- Tables where possible

Handle:

- Multi-page PDFs
- Empty pages
- Headers
- Footers
- Different layouts
- Basic scanned PDF fallback if practical

If OCR is not included in Version 1, clearly report that scanned PDFs may not be supported.

---

# 13. DOCX PROCESSING

Use python-docx.

Extract:

- Paragraphs
- Headings
- Bullet points
- Tables

Preserve section boundaries.

---

# 14. TXT PROCESSING

Read the entire file.

Normalize:

- Line breaks
- Whitespace
- Unicode
- Bullets

---

# 15. TEXT CLEANING

Implement:

```text
src/ingestion/document_processor.py
```

Cleaning must:

- Remove excessive whitespace
- Normalize newlines
- Normalize bullet characters
- Remove duplicate headers/footers where detectable
- Preserve technical terms
- Preserve version numbers
- Preserve years
- Preserve acronyms
- Preserve section headings

Do NOT remove:

```text
Java
Python
C#
JavaScript
TypeScript
Selenium
Playwright
Appium
REST Assured
LangChain
LangGraph
AWS
Azure
Docker
Kubernetes
```

---

# 16. RESUME SECTION DETECTION

Detect common sections:

```text
Professional Summary
Summary
Objective
Technical Skills
Skills
Professional Experience
Work Experience
Experience
Projects
Education
Certifications
Achievements
Responsibilities
Tools
Technologies
```

Store section as metadata.

Example:

```json
{
    "section": "Technical Skills",
    "page": 2
}
```

---

# 17. CHUNKING

Do not blindly split every resume into fixed-size chunks.

Use section-aware chunking.

Preferred:

```text
Resume
  ↓
Section
  ↓
Paragraph/Bullet
  ↓
Semantic Chunk
```

Recommended configurable values:

```env
CHUNK_SIZE=700
CHUNK_OVERLAP=100
```

Preserve complete sentences.

Do not split technical terms.

---

# 18. CHROMADB

Use ChromaDB.

Default path:

```text
data/chroma/
```

Collection:

```text
resume_documents
```

Each chunk must store:

```text
chunk_id
document_id
session_id
source
section
page
text
```

Metadata example:

```json
{
    "chunk_id": "chunk_001",
    "document_id": "resume_123",
    "session_id": "abc123",
    "source": "resume.pdf",
    "section": "Professional Experience",
    "page": 3
}
```

---

# 19. SESSION ISOLATION

This is mandatory.

The application is intended for shared Streamlit deployment.

User A must never retrieve User B's resume.

Every ChromaDB record must include:

```text
session_id
document_id
```

Retrieval must filter by the current session/document.

Example conceptual query:

```python
where={
    "session_id": session_id,
    "document_id": document_id
}
```

Do not create a globally shared resume retrieval context.

Use:

```python
st.session_state
```

for session-specific state.

---

# 20. SESSION STATE

Maintain:

```python
st.session_state["session_id"]
st.session_state["resume_processed"]
st.session_state["resume_filename"]
st.session_state["document_id"]
st.session_state["resume_chunks"]
st.session_state["analysis_result"]
```

Do not re-index the same resume on every Streamlit rerun.

---

# 21. JD INPUT

Create a large text area.

```text
Job Description

Paste the complete job description below.

[                                      ]
[                                      ]
[                                      ]

Characters: 0

[ Analyze Resume ]
```

The Analyze button should only be enabled when:

```text
Resume is indexed
AND
JD is not empty
```

---

# 22. OPTIONAL JD FILE

Support optional:

```text
PDF
DOCX
TXT
```

The user may:

- Paste JD
OR
- Upload JD

Do not require both.

---

# 23. JD PARSING

Extract:

### Programming Languages

Examples:

```text
Java
Python
C#
JavaScript
TypeScript
```

### Automation

```text
Selenium
Playwright
Cypress
Appium
Tosca
```

### API

```text
REST API
REST Assured
Postman
SOAP
GraphQL
```

### CI/CD

```text
Jenkins
GitHub Actions
Azure DevOps
GitLab CI
```

### Cloud

```text
AWS
Azure
GCP
```

### DevOps

```text
Docker
Kubernetes
Terraform
Helm
```

### AI

```text
LLM
RAG
LangChain
LangGraph
Prompt Engineering
AI Testing
Agentic AI
```

### Databases

```text
Oracle
SQL Server
PostgreSQL
MongoDB
```

### Test Management

```text
Jira
ALM
Zephyr
Xray
```

### Soft Skills

```text
Leadership
Communication
Stakeholder Management
Team Management
```

---

# 24. SKILL NORMALIZATION

Create:

```text
config/skill_synonyms.yaml
```

Example:

```yaml
selenium:
  canonical: Selenium
  aliases:
    - Selenium WebDriver
    - WebDriver

javascript:
  canonical: JavaScript
  aliases:
    - JS
    - ECMAScript

typescript:
  canonical: TypeScript
  aliases:
    - TS

playwright:
  canonical: Playwright
  aliases:
    - Playwright Test

python:
  canonical: Python
  aliases:
    - Python3

pytest:
  canonical: pytest
  aliases:
    - PyTest

api_testing:
  canonical: API Testing
  aliases:
    - REST API Testing
    - API Automation

rest_assured:
  canonical: REST Assured
  aliases:
    - Rest Assured
    - REST-Assured
```

The dictionary must be configurable.

---

# 25. JD REQUIREMENT CLASSIFICATION

Classify requirements:

```text
MANDATORY
PREFERRED
OPTIONAL
```

Examples:

```text
"Must have Selenium"
→ MANDATORY

"5+ years Python required"
→ MANDATORY

"Playwright preferred"
→ PREFERRED

"Kubernetes is a plus"
→ OPTIONAL
```

---

# 26. EXPERIENCE EXTRACTION

Extract years of experience from JD.

Examples:

```text
5+ years Selenium
3 years Python
2+ years Playwright
```

Store:

```python
required_experience
```

Do not invent experience when JD does not specify it.

---

# 27. RESUME EXPERIENCE EXTRACTION

Extract explicit experience.

Examples:

```text
Selenium – 10 years
Playwright – 5 years
Python – 6 years
```

If duration is not available:

```text
experience_status = "NOT_SPECIFIED"
```

Never infer exact years from employment duration unless explicitly supported.

---

# 28. MATCHING ENGINE

Create:

```text
src/matching/
```

Files:

```text
exact_matcher.py
semantic_matcher.py
experience_matcher.py
hybrid_matcher.py
scoring_engine.py
```

---

# 29. EXACT MATCHING

If the JD requires:

```text
Playwright
```

and resume contains:

```text
Playwright automation
```

return:

```text
MATCHED
```

---

# 30. NORMALIZED MATCHING

If JD:

```text
JavaScript
```

Resume:

```text
JS
```

and synonym dictionary confirms equivalence:

```text
MATCHED
```

---

# 31. SEMANTIC MATCHING

Use ChromaDB retrieval.

Example:

JD:

```text
Browser automation experience
```

Resume:

```text
Developed Selenium and Playwright automation frameworks.
```

Retrieve relevant chunks.

Use similarity as supporting evidence.

Do not automatically convert semantic similarity into an exact skill match.

---

# 32. RELATED TECHNOLOGY RULE

Example:

JD:

```text
Cypress
```

Resume:

```text
Playwright
```

Result:

```text
PARTIAL
```

NOT:

```text
MATCHED
```

Explanation:

```text
The candidate has browser automation experience with Playwright,
but Cypress experience was not explicitly found.
```

---

# 33. MATCH STATUS

Allowed statuses:

```text
MATCHED
PARTIAL
MISSING
```

Experience statuses:

```text
MEETS_REQUIREMENT
BELOW_REQUIREMENT
NOT_SPECIFIED
NOT_REQUIRED
```

---

# 34. CONFIDENCE

Allowed:

```text
HIGH
MEDIUM
LOW
```

High:

- Exact skill match
- Strong resume evidence
- Clear context

Medium:

- Semantic/related evidence

Low:

- Weak contextual similarity

Never mark weak evidence as high confidence.

---

# 35. RESUME EVIDENCE

Every matched or partial skill should contain:

```text
Skill
JD Evidence
Resume Evidence
Source Section
Source Page
Similarity Score
Confidence
```

Example:

```json
{
    "skill": "Playwright",
    "status": "MATCHED",
    "confidence": "HIGH",
    "jd_evidence": "5+ years Playwright",
    "resume_evidence": "5 years of Playwright automation experience",
    "source_section": "Professional Experience",
    "source_page": 3,
    "similarity_score": 0.91
}
```

---

# 36. SCORING

The LLM must NOT calculate the final percentage.

Python must calculate it.

Weights:

```text
MANDATORY = 3
PREFERRED = 2
OPTIONAL = 1
```

Match values:

```text
MATCHED = 1
PARTIAL = 0.5
MISSING = 0
```

Formula:

```text
weighted_score =
sum(skill_weight * match_value)

total_weight =
sum(skill_weight)

overall_match =
weighted_score / total_weight * 100
```

Round to:

```text
1 decimal place
```

---

# 37. EXAMPLE SCORE

JD:

```text
Selenium      Mandatory
Playwright    Mandatory
Python        Preferred
Kubernetes    Mandatory
Docker        Optional
```

Weights:

```text
Selenium = 3
Playwright = 3
Python = 2
Kubernetes = 3
Docker = 1
```

If:

```text
Selenium = MATCHED
Playwright = MATCHED
Python = MATCHED
Kubernetes = MISSING
Docker = PARTIAL
```

Then:

```text
score =
3 + 3 + 2 + 0 + 0.5

total =
3 + 3 + 2 + 3 + 1

percentage =
8.5 / 12 × 100
```

Display the calculation in an expandable UI section.

---

# 38. ADDITIONAL METRICS

Calculate independently:

```text
Overall Match %
Matched Skill %
Partial Skill %
Missing Skill %
Keyword Coverage %
Mandatory Skill Coverage %
Experience Coverage %
```

Do not use the same number for every metric.

---

# 39. KEYWORD ANALYSIS

Extract important JD keywords.

Classify:

```text
PRESENT
MISSING
RELATED
```

Example:

JD:

```text
CI/CD
```

Resume:

```text
Jenkins
```

Result:

```text
RELATED
```

Explanation:

```text
Jenkins is a CI/CD tool, but the exact term CI/CD
is not explicitly present in the resume.
```

---

# 40. MISSING KEYWORDS

Display:

```text
Missing Keywords

Kubernetes
CI/CD
Test Observability
Performance Testing
Terraform
```

For each:

```text
Keyword
Importance
Reason
Related Resume Term
```

---

# 41. RESUME OPTIMIZATION SUGGESTIONS

Provide suggestions such as:

```text
The JD explicitly mentions "CI/CD".
The resume mentions Jenkins.

If accurate, consider explicitly mentioning
"CI/CD" in the relevant experience section.
```

Never recommend adding an untrue skill.

Never fabricate experience.

---

# 42. LEARNING RESOURCE SYSTEM

Create:

```text
config/learning_resources.yaml
```

Example:

```yaml
playwright:
  - name: Playwright Official Documentation
    url: https://playwright.dev/
    type: official

selenium:
  - name: Selenium Official Documentation
    url: https://www.selenium.dev/documentation/
    type: official

python:
  - name: Python Documentation
    url: https://docs.python.org/3/
    type: official

kubernetes:
  - name: Kubernetes Documentation
    url: https://kubernetes.io/docs/
    type: official
```

Use official resources first.

---

# 43. LEARNING ROADMAP

For missing skills show:

```text
Skill
Priority
Why it matters
Learning path
Official documentation
Beginner resource
Advanced resource
```

Example:

```text
Kubernetes

Priority:
HIGH

Why:
Mandatory JD requirement.

Learning path:

1. Kubernetes fundamentals
2. Pods
3. Deployments
4. Services
5. ConfigMaps
6. Secrets
7. Helm
8. CI/CD integration
```

---

# 44. STREAMLIT UI

Create a professional dashboard.

Application name:

```text
Resume AI Match Analyzer
```

Subtitle:

```text
RAG-powered Resume & Job Description Skill Gap Analysis
```

---

# 45. SIDEBAR

Sidebar sections:

```text
Resume
-------
Upload Resume
Resume Status
Document Information

Analysis
--------
Model Status
Vector DB Status

Actions
-------
Re-index Resume
Clear Resume

Settings
--------
AI Reasoning
Similarity Threshold
Top K
```

---

# 46. MAIN PAGE

Initial layout:

```text
----------------------------------------------------
              Resume AI Match Analyzer
      RAG-powered Resume & JD Analysis
----------------------------------------------------

Resume Upload

[ Upload Resume ]

----------------------------------------------------

Job Description

[ Paste Job Description ]

[ Analyze Resume ]

----------------------------------------------------
```

---

# 47. DASHBOARD

After analysis:

```text
----------------------------------------------------
                    ANALYSIS
----------------------------------------------------

Overall Match

82.4%

----------------------------------------------------

Matched     Partial     Missing     Keywords
  18           4           6            8

----------------------------------------------------
```

---

# 48. KPI CARDS

Use:

```python
col1, col2, col3, col4 = st.columns(4)
```

Cards:

```text
Overall Match
Matched Skills
Partial Skills
Missing Skills
```

Additional:

```text
Keyword Coverage
Experience Coverage
Mandatory Skill Coverage
```

---

# 49. TABS

Create:

```text
Overview
Skills Match
Partial Match
Missing Skills
Keywords
Experience
Learning Roadmap
Resume Suggestions
Evidence
```

---

# 50. OVERVIEW TAB

Display:

```text
Resume:
<filename>

Job Title:
<detected title>

Overall Match:
82.4%

Mandatory Skills:
90%

Preferred Skills:
75%

Keyword Coverage:
81%

Experience Coverage:
88%
```

Also display:

```text
Top Matching Skills

Selenium
Playwright
Java
Python
API Testing
Jenkins
```

And:

```text
Key Skill Gaps

Kubernetes
Cypress
Terraform
```

---

# 51. SKILLS MATCH TAB

Table:

```text
Skill
Requirement
Resume Evidence
Experience
Confidence
```

Example:

```text
Selenium
Required
10 years Selenium automation
10 years
High

Playwright
Required
5 years Playwright
5 years
High
```

---

# 52. PARTIAL MATCH TAB

Example:

```text
Cypress

Status:
PARTIAL

Related Skill:
Playwright

Reason:
Both are browser automation technologies,
but Cypress experience was not explicitly found.
```

---

# 53. MISSING SKILLS TAB

Table:

```text
Skill
Requirement
Priority
Evidence
Learning Resource
```

Example:

```text
Kubernetes
Mandatory
High
Not Found
[Learn]
```

---

# 54. KEYWORDS TAB

Display:

```text
Present Keywords
Missing Keywords
Related Keywords
```

Allow filtering.

---

# 55. EXPERIENCE TAB

Display:

| Skill | JD Required | Resume | Status |
|---|---:|---:|---|
| Selenium | 5 years | 10 years | Meets |
| Python | 3 years | 4 years | Meets |
| Kubernetes | 2 years | Not specified | Not Specified |

---

# 56. LEARNING ROADMAP TAB

Display missing skills grouped:

```text
HIGH PRIORITY

Kubernetes
Cypress

MEDIUM PRIORITY

Terraform
Performance Testing

LOW PRIORITY

Other optional skills
```

Each should have clickable resources.

---

# 57. EVIDENCE TAB

Provide traceability:

```text
JD Requirement
      ↓
Retrieved Resume Chunk
      ↓
Skill Match
      ↓
Confidence
      ↓
Decision
```

This is mandatory for explainability.

---

# 58. PLOTLY VISUALIZATIONS

Use Plotly.

Charts:

1. Overall Match Donut
2. Matched vs Partial vs Missing
3. Skill Category Match
4. Keyword Coverage
5. Experience Coverage

Do not use charts for exact individual evidence.

---

# 59. DOWNLOAD REPORT

Provide:

```text
Download JSON
Download CSV
Download Excel
Download PDF
```

Use:

```python
st.download_button()
```

Report must contain:

```text
Resume
Job Description Summary
Overall Match
Matched Skills
Partial Skills
Missing Skills
Missing Keywords
Experience Analysis
Learning Roadmap
Resume Suggestions
```

---

# 60. REPORT GENERATION

Create:

```text
src/reporting/
```

Files:

```text
json_report.py
csv_report.py
excel_report.py
pdf_report.py
```

Do not mix report generation logic with UI code.

---

# 61. PROJECT STRUCTURE

Generate exactly this structure unless there is a strong technical reason to improve it:

```text
resume-jd-rag/

├── app.py
│
├── pages/
│   ├── 01_Resume_Analyzer.py
│   ├── 02_Analysis_History.py
│   └── 03_Settings.py
│
├── src/
│   ├── config/
│   │   └── settings.py
│   │
│   ├── ingestion/
│   │   ├── pdf_loader.py
│   │   ├── docx_loader.py
│   │   ├── txt_loader.py
│   │   ├── document_processor.py
│   │   └── section_detector.py
│   │
│   ├── chunking/
│   │   └── chunker.py
│   │
│   ├── embeddings/
│   │   └── embedding_service.py
│   │
│   ├── vectorstore/
│   │   └── chroma_manager.py
│   │
│   ├── llm/
│   │   └── llm_client.py
│   │
│   ├── jd/
│   │   ├── jd_parser.py
│   │   ├── skill_extractor.py
│   │   ├── keyword_extractor.py
│   │   └── requirement_classifier.py
│   │
│   ├── matching/
│   │   ├── exact_matcher.py
│   │   ├── semantic_matcher.py
│   │   ├── experience_matcher.py
│   │   ├── hybrid_matcher.py
│   │   └── scoring_engine.py
│   │
│   ├── resources/
│   │   └── resource_manager.py
│   │
│   ├── reporting/
│   │   ├── json_report.py
│   │   ├── csv_report.py
│   │   ├── excel_report.py
│   │   └── pdf_report.py
│   │
│   ├── models/
│   │   ├── resume.py
│   │   ├── jd.py
│   │   └── analysis.py
│   │
│   └── services/
│       ├── resume_service.py
│       └── analysis_service.py
│
├── config/
│   ├── skill_synonyms.yaml
│   ├── skill_categories.yaml
│   ├── learning_resources.yaml
│   └── scoring_config.yaml
│
├── prompts/
│   ├── jd_extraction_prompt.txt
│   ├── skill_analysis_prompt.txt
│   ├── match_reasoning_prompt.txt
│   └── resume_suggestion_prompt.txt
│
├── data/
│   └── chroma/
│
├── tests/
│   ├── test_document_processing.py
│   ├── test_chunking.py
│   ├── test_skill_extraction.py
│   ├── test_matching.py
│   ├── test_experience.py
│   ├── test_scoring.py
│   ├── test_resources.py
│   └── test_session_isolation.py
│
├── .streamlit/
│   └── config.toml
│
├── .env.example
├── .gitignore
├── requirements.txt
├── runtime.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
└── PROMPT.md
```

---

# 62. PYDANTIC MODELS

Create:

```python
class ResumeChunk(BaseModel):
    chunk_id: str
    document_id: str
    session_id: str
    text: str
    section: str | None
    page: int | None
```

Create:

```python
class JobRequirement(BaseModel):
    skill: str
    category: str
    priority: str
    required_experience: float | None
    source_text: str
```

Create:

```python
class SkillMatch(BaseModel):
    skill: str
    category: str
    priority: str
    status: str
    confidence: str
    similarity_score: float | None
    jd_evidence: str
    resume_evidence: str
    required_experience: float | None
    resume_experience: float | None
    experience_status: str
```

Create:

```python
class AnalysisResult(BaseModel):
    overall_match_percentage: float
    matched_percentage: float
    partial_percentage: float
    missing_percentage: float
    keyword_match_percentage: float
    mandatory_skill_percentage: float
    experience_match_percentage: float

    matched_skills: list[SkillMatch]
    partial_skills: list[SkillMatch]
    missing_skills: list[SkillMatch]

    present_keywords: list[str]
    missing_keywords: list[str]
    related_keywords: list[str]

    learning_resources: dict
    resume_suggestions: list[str]
```

---

# 63. CONFIGURATION

Create:

```text
src/config/settings.py
```

Support:

```env
MODEL_NAME=qwen/qwen3.7-flash:free

OPENAI_API_BASE=https://api.xkiro.com/v1

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

CHROMA_PERSIST_DIRECTORY=./data/chroma

CHROMA_COLLECTION_NAME=resume_documents

CHUNK_SIZE=700

CHUNK_OVERLAP=100

TOP_K=5

MATCH_THRESHOLD=0.70

PARTIAL_THRESHOLD=0.50

MAX_UPLOAD_SIZE_MB=10

LLM_ENABLED=true
```

---

# 64. CACHING

Use Streamlit caching for expensive resources.

Cache:

- Embedding model
- Chroma client
- LLM client
- Static YAML configuration

Do not globally cache user-specific resume data.

---

# 65. LLM PROMPT FILES

Create prompts as external text files.

Do not hard-code long prompts inside Python.

---

# 66. JD EXTRACTION PROMPT

The prompt must instruct Qwen:

```text
You are a Job Description Requirement Extraction Engine.

Extract only requirements explicitly supported by the job description.

Return structured JSON.

For each requirement identify:

skill
category
priority
required_experience
source_text

Priority must be:
MANDATORY
PREFERRED
OPTIONAL

Never invent a requirement.

Do not infer technologies that are not supported by the JD.
```

---

# 67. MATCH REASONING PROMPT

Use:

```text
You are a Resume Skill Matching Engine.

Compare the job requirement against the supplied resume evidence.

Rules:

1. Never invent candidate experience.
2. Never invent years of experience.
3. Exact skill evidence can be MATCHED.
4. Alias/synonym evidence can be MATCHED.
5. Related technology should normally be PARTIAL.
6. Missing evidence should be MISSING.
7. Every MATCHED result must provide resume evidence.
8. Do not treat semantic similarity alone as proof of experience.
9. Do not fabricate certifications or projects.

Return valid JSON.
```

---

# 68. RESUME SUGGESTION PROMPT

Use:

```text
Provide evidence-based resume improvement suggestions.

Do not add technologies the candidate has not demonstrated.

If the JD contains a keyword related to an existing resume technology,
suggest clearer terminology only when it accurately represents the
candidate's existing experience.

Never fabricate:
- skills
- projects
- years
- certifications
- employers
- responsibilities
```

---

# 69. STRUCTURED LLM OUTPUT

All LLM output must be parsed and validated.

Prefer:

```text
Pydantic
+
JSON
```

If invalid JSON is returned:

1. Attempt safe parsing.
2. Retry once with a correction prompt if appropriate.
3. Fall back to deterministic analysis.
4. Never crash the Streamlit application.

---

# 70. LLM FAILURE FALLBACK

If the XKIRO endpoint is unavailable:

Continue with:

```text
Exact Matching
Normalized Matching
ChromaDB Semantic Search
Keyword Matching
Deterministic Scoring
```

Display:

```text
AI reasoning is currently unavailable.
Showing deterministic RAG-based analysis.
```

The application must remain usable.

---

# 71. API ERROR HANDLING

Handle:

```text
401
403
429
500
502
503
Timeout
ConnectionError
Malformed Response
```

Do not expose technical stack traces to users.

Log technical details server-side without logging resume content.

---

# 72. PRIVACY

Never log:

- Full resume
- Phone number
- Email
- Address
- Personal identifiers
- Complete JD

Log only:

```text
session ID
document ID
file type
processing duration
chunk count
analysis duration
skill counts
```

If AI reasoning is enabled, show:

```text
AI Analysis Notice

Relevant resume and job-description content may be sent to the
configured AI provider for analysis.
```

Do not make claims about external provider retention unless verified.

---

# 73. SESSION CLEANUP

Provide:

```text
Clear Resume
```

This should:

1. Remove current session data.
2. Delete associated ChromaDB documents.
3. Clear analysis results.
4. Reset UI state.

---

# 74. MULTIPLE JD ANALYSIS

The same indexed resume must be reusable.

Workflow:

```text
Upload Resume
     ↓
Index once
     ↓
JD #1
     ↓
Analyze
     ↓
JD #2
     ↓
Analyze
     ↓
JD #3
     ↓
Analyze
```

Do not re-embed the resume for every JD.

---

# 75. ANALYSIS HISTORY

Create an optional session-level analysis history.

Store:

```text
timestamp
job_title
company
overall_match
matched_count
partial_count
missing_count
```

Do not unnecessarily store full resume content.

---

# 76. JOB TITLE EXTRACTION

Attempt to extract:

```text
Job Title
Company
Location
Experience Requirement
```

from the JD.

If not found:

```text
Not detected
```

Do not invent.

---

# 77. COMPANY EXTRACTION

If JD contains:

```text
Company: ABC
```

extract it.

Otherwise:

```text
Not specified
```

---

# 78. DOMAIN ANALYSIS

Optionally classify:

```text
Banking
Financial Services
Healthcare
Insurance
Retail
Technology
Automotive
Other
```

Only when supported by JD/resume content.

---

# 79. SKILL CATEGORIES

Create:

```yaml
programming_languages:
  - Java
  - Python
  - C#
  - JavaScript
  - TypeScript

automation:
  - Selenium
  - Playwright
  - Cypress
  - Appium
  - Tosca

api_testing:
  - REST Assured
  - Postman
  - SOAP UI
  - GraphQL

cloud:
  - AWS
  - Azure
  - GCP

devops:
  - Jenkins
  - GitHub Actions
  - Azure DevOps
  - Docker
  - Kubernetes

ai:
  - LLM
  - RAG
  - LangChain
  - LangGraph
  - Prompt Engineering
  - AI Testing
  - Agentic AI

databases:
  - Oracle
  - SQL Server
  - PostgreSQL
  - MongoDB

test_management:
  - Jira
  - ALM
  - Zephyr
  - Xray
```

Make it configurable.

---

# 80. SECURITY

Implement:

- File extension validation
- MIME validation
- File size validation
- Filename sanitization
- Temporary file cleanup
- Input validation
- JD size limit
- Safe YAML loading
- Safe JSON parsing
- No arbitrary code execution
- No user-provided URL fetching
- No secret exposure

---

# 81. FILE HANDLING

Uploaded files should be processed safely.

Do not trust the original filename.

Generate:

```text
document_id
```

using UUID.

Use a temporary processing location.

Delete unnecessary temporary files after processing.

---

# 82. UI ERROR MESSAGES

Use user-friendly errors.

Example:

```text
Please upload a resume before starting analysis.
```

```text
Unable to extract readable text from this document.
```

```text
The Job Description does not contain enough information for analysis.
```

```text
AI reasoning is temporarily unavailable.
```

---

# 83. EMPTY STATES

Before resume:

```text
Upload your resume to get started.

Your resume will be processed, chunked,
embedded and indexed into ChromaDB.
```

Before JD:

```text
Paste a Job Description to analyze your skill alignment.
```

---

# 84. STREAMLIT DESIGN

Use:

```text
st.set_page_config(
    page_title="Resume AI Match Analyzer",
    page_icon="📄",
    layout="wide"
)
```

Create custom CSS for:

- Cards
- Headers
- Metrics
- Tables
- Tabs
- Buttons
- Progress indicators

Keep design professional.

---

# 85. COLOR SEMANTICS

Use semantic UI styling:

Matched:
positive visual indicator

Partial:
warning visual indicator

Missing:
negative visual indicator

Do not rely on color alone.

Always include text labels.

---

# 86. ACCESSIBILITY

Ensure:

- Text labels accompany colors
- Buttons have clear names
- Tables are readable
- Expanders are understandable
- No essential information is communicated only by color

---

# 87. PERFORMANCE

Optimize:

- Embedding model loading
- ChromaDB connection
- Resume processing
- Vector retrieval
- LLM calls

Do not reprocess unchanged resumes.

Use configurable:

```text
TOP_K
```

Default:

```text
5
```

---

# 88. RETRIEVAL

For each important JD skill:

```text
Skill
 ↓
Embedding
 ↓
ChromaDB
 ↓
Top K chunks
 ↓
Resume evidence
```

Use metadata filters:

```text
session_id
document_id
```

---

# 89. RETRIEVAL THRESHOLDS

Configure:

```env
MATCH_THRESHOLD=0.70
PARTIAL_THRESHOLD=0.50
```

Example:

```text
>= 0.70
strong semantic evidence

0.50 - 0.69
partial evidence

< 0.50
weak/no evidence
```

However, threshold alone must NOT determine factual skill ownership.

Exact/normalized evidence takes precedence.

---

# 90. SCORE EXPLANATION

Provide an expander:

```text
How is the match score calculated?
```

Show:

```text
Mandatory Skills
Preferred Skills
Optional Skills

Matched contribution
Partial contribution
Missing contribution

Final weighted percentage
```

---

# 91. NO HIRING PREDICTIONS

The application must not state:

```text
You will get this job.
You are guaranteed an interview.
You will be selected.
```

It should only analyze resume/JD alignment.

---

# 92. TESTING

Use pytest.

Create unit tests for:

```text
PDF extraction
DOCX extraction
TXT extraction
Text cleaning
Section detection
Chunking
Skill normalization
Skill extraction
Exact matching
Semantic matching
Experience matching
Keyword analysis
Scoring
Learning resources
```

---

# 93. SESSION ISOLATION TEST

Test:

```text
User A uploads Resume A
User B uploads Resume B

User A analyzes JD

Result must contain evidence only from Resume A.

User B analyzes JD

Result must contain evidence only from Resume B.
```

This test is mandatory.

---

# 94. LLM MOCK TESTING

Do not make real XKIRO API calls in unit tests.

Mock:

```text
LLM provider
```

Test:

```text
Valid JSON
Invalid JSON
Timeout
API error
Empty response
```

---

# 95. CHROMADB TESTING

Test:

```text
Insert chunks
Retrieve chunks
Metadata filter
Session isolation
Delete document
Re-index document
```

---

# 96. TEST DATA

Create:

```text
tests/test_data/
```

Include small synthetic resume/JD examples.

Do not include real personal information.

---

# 97. README

Generate complete README.

Include:

```text
Project Overview
Features
Architecture
Tech Stack
Project Structure
Installation
Virtual Environment
Environment Variables
Streamlit Secrets
Running Locally
Running Tests
Docker
Streamlit Deployment
ChromaDB
Embedding Model
XKIRO Model
Security
Privacy
Troubleshooting
Limitations
Future Enhancements
```

---

# 98. LOCAL INSTALLATION

README must contain:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

Install:

```bash
pip install -r requirements.txt
```

Run:

```bash
streamlit run app.py
```

---

# 99. STREAMLIT DEPLOYMENT

Document:

1. Push repository to GitHub.
2. Create Streamlit application.
3. Select repository.
4. Select `app.py`.
5. Configure Python version.
6. Add Streamlit secret:

```toml
XKIRO_API_KEY = "..."
```

7. Deploy.

Do not commit secrets.

---

# 100. STREAMLIT PERSISTENCE WARNING

The application must document that local filesystem storage may not provide durable persistence across hosted application restarts/redeployments.

Therefore design:

```text
VectorStore interface
```

so ChromaDB can later be replaced by a hosted persistent vector store.

Version 1 can use:

```text
ChromaDB local persistence
```

for the initial deployment.

---

# 101. DOCKER

Generate:

```text
Dockerfile
docker-compose.yml
```

The Docker application should run:

```bash
docker compose up --build
```

Persist:

```text
./data/chroma
```

---

# 102. GITIGNORE

Include:

```text
.venv/
__pycache__/
*.pyc
.env
.streamlit/secrets.toml
data/chroma/
uploads/
*.log
.pytest_cache/
.DS_Store
```

---

# 103. REQUIREMENTS

Generate a working:

```text
requirements.txt
```

Use compatible versions.

At minimum:

```text
streamlit
langchain
langchain-openai
langchain-community
chromadb
sentence-transformers
pymupdf
python-docx
pydantic
python-dotenv
pyyaml
plotly
pandas
openpyxl
reportlab
pytest
```

Validate dependency compatibility.

---

# 104. APPLICATION FLOW

Complete flow:

```text
START APPLICATION
       |
       v
CREATE SESSION
       |
       v
UPLOAD RESUME
       |
       v
VALIDATE FILE
       |
       v
EXTRACT TEXT
       |
       v
DETECT SECTIONS
       |
       v
CHUNK RESUME
       |
       v
CREATE EMBEDDINGS
       |
       v
STORE IN CHROMADB
       |
       v
RESUME READY
       |
       v
PASTE JD
       |
       v
PARSE JD
       |
       v
EXTRACT SKILLS
       |
       v
NORMALIZE SKILLS
       |
       v
CLASSIFY REQUIREMENTS
       |
       v
RETRIEVE RESUME EVIDENCE
       |
       v
EXACT MATCH
       |
       v
SEMANTIC MATCH
       |
       v
QWEN CONTEXTUAL ANALYSIS
       |
       v
EXPERIENCE MATCH
       |
       v
KEYWORD ANALYSIS
       |
       v
CALCULATE SCORE
       |
       v
GENERATE LEARNING RESOURCES
       |
       v
GENERATE RESUME SUGGESTIONS
       |
       v
DISPLAY DASHBOARD
       |
       v
EXPORT REPORT
```

---

# 105. CORE BUSINESS RULES

The following rules are mandatory:

### Rule 1

Never invent resume experience.

### Rule 2

Never invent years of experience.

### Rule 3

Never invent certifications.

### Rule 4

Never convert related technology into exact match.

### Rule 5

Vector similarity is evidence, not truth.

### Rule 6

Final score is calculated by Python.

### Rule 7

Every important match must have evidence.

### Rule 8

Missing skills must be clearly identified.

### Rule 9

Learning resources must use curated URLs.

### Rule 10

User sessions must be isolated.

---

# 106. EXAMPLE

Resume:

```text
14+ years of IT experience.

10 years Selenium.

5 years Playwright.

Python automation experience.

Java automation experience.

REST Assured.

Jenkins.

AWS.

LangChain.

LangGraph.
```

JD:

```text
Senior QA Automation Architect

Required:

5+ years Selenium
3+ years Playwright
3+ years Python
Cypress
Kubernetes

Preferred:

AWS
Docker
LangChain
```

Expected analysis:

```text
Selenium
MATCHED

Playwright
MATCHED

Python
MATCHED

Cypress
MISSING

Kubernetes
MISSING

AWS
MATCHED

Docker
MISSING

LangChain
MATCHED
```

Cypress must NOT be marked matched simply because Playwright exists.

---

# 107. EXPECTED UI

The finished UI should look approximately like:

```text
╔════════════════════════════════════════════════════════════╗
║              📄 Resume AI Match Analyzer                  ║
║       RAG-powered Resume & JD Skill Analysis              ║
╚════════════════════════════════════════════════════════════╝

SIDEBAR
────────────────────
Resume
[ Upload Resume ]

✓ Indexed

Chunks: 42

Model
Qwen 3.7 Flash

Vector DB
✓ ChromaDB

────────────────────

MAIN

Resume
✓ Vijay_Kumar_Resume.pdf

Job Description

[ Paste JD here                         ]
[                                      ]
[                                      ]

              [ 🔍 Analyze Resume ]


                    ANALYSIS

        ┌───────────────┐
        │     82.4%     │
        │ Overall Match │
        └───────────────┘


┌──────────┬──────────┬──────────┬──────────┐
│ Matched  │ Partial  │ Missing  │ Keywords │
│   18     │    4     │    6     │    8     │
└──────────┴──────────┴──────────┴──────────┘


[Overview] [Skills] [Partial] [Missing]
[Keywords] [Experience] [Learning] [Evidence]


Top Matching Skills

✓ Selenium
✓ Playwright
✓ Python
✓ Java
✓ API Testing


Key Skill Gaps

! Kubernetes
! Cypress
! Docker


Learning Roadmap

Kubernetes
[Official Documentation]

Cypress
[Official Documentation]
```

---

# 108. CODE QUALITY

All code must:

- Use type hints
- Use docstrings for public functions
- Use meaningful names
- Avoid duplicated code
- Avoid giant functions
- Follow single responsibility
- Separate UI from business logic
- Handle exceptions
- Use structured models
- Use logging
- Be testable

---

# 109. DO NOT

Do NOT:

- Hard-code API keys
- Hard-code the final score
- Put all logic in `app.py`
- Use global resume data for all users
- Send the entire resume to the LLM unnecessarily
- Treat vector similarity as factual proof
- Invent skills
- Invent experience
- Generate fake learning URLs
- Store secrets in Git
- Use real personal information in test data
- Create unnecessary microservices

---

# 110. IMPLEMENTATION ORDER

Build in this order:

## Phase 1

Project setup.

Create:

```text
requirements.txt
.env.example
.gitignore
README.md
```

---

## Phase 2

Resume processing.

Implement:

```text
PDF
DOCX
TXT
Cleaning
Section detection
Chunking
```

---

## Phase 3

Embeddings + ChromaDB.

Implement:

```text
Embedding service
Chroma manager
Metadata
Session isolation
```

---

## Phase 4

Streamlit resume UI.

Implement:

```text
Upload
Progress
Indexing status
Clear resume
```

---

## Phase 5

JD parser.

Implement:

```text
Skill extraction
Keyword extraction
Requirement classification
Experience extraction
Normalization
```

---

## Phase 6

Matching.

Implement:

```text
Exact matching
Normalized matching
Semantic retrieval
Experience matching
Hybrid matching
```

---

## Phase 7

Qwen integration.

Implement:

```text
LLM provider
Prompt files
Structured JSON
Pydantic validation
Fallback
```

---

## Phase 8

Scoring.

Implement:

```text
Weighted score
Skill percentages
Keyword coverage
Experience coverage
Mandatory coverage
```

---

## Phase 9

Dashboard.

Implement:

```text
KPI cards
Plotly charts
Tabs
Evidence
Missing skills
Missing keywords
```

---

## Phase 10

Learning resources.

Implement:

```text
learning_resources.yaml
resource manager
learning roadmap
clickable links
```

---

## Phase 11

Export.

Implement:

```text
JSON
CSV
Excel
PDF
```

---

## Phase 12

Testing.

Implement:

```text
Unit tests
Integration tests
LLM mocks
Chroma tests
Session isolation tests
```

---

## Phase 13

Deployment.

Implement:

```text
Dockerfile
docker-compose.yml
Streamlit configuration
Deployment documentation
```

---

# 111. DEFINITION OF DONE

The project is complete only when all of the following work:

```text
[ ] PDF upload
[ ] DOCX upload
[ ] TXT upload
[ ] Resume extraction
[ ] Section detection
[ ] Resume chunking
[ ] Local embeddings
[ ] ChromaDB indexing
[ ] Session isolation
[ ] JD paste
[ ] JD upload
[ ] JD skill extraction
[ ] Skill normalization
[ ] Requirement classification
[ ] Experience extraction
[ ] Exact matching
[ ] Semantic matching
[ ] Partial matching
[ ] Missing skill detection
[ ] Missing keyword detection
[ ] Experience comparison
[ ] Weighted scoring
[ ] Match percentage
[ ] Keyword percentage
[ ] Experience percentage
[ ] Mandatory skill percentage
[ ] Qwen integration
[ ] LLM fallback
[ ] Evidence display
[ ] Confidence
[ ] Learning resources
[ ] Clickable hyperlinks
[ ] Resume suggestions
[ ] Dashboard
[ ] Plotly charts
[ ] Analysis history
[ ] JSON export
[ ] CSV export
[ ] Excel export
[ ] PDF export
[ ] Unit tests
[ ] Integration tests
[ ] Session isolation tests
[ ] Docker
[ ] README
[ ] Streamlit deployment support
[ ] Secret management
```

---

# 112. FINAL GENERATION INSTRUCTION

Generate the complete application from this specification.

Do not stop after creating the architecture.

Generate:

1. Every Python source file.
2. Every configuration file.
3. Every YAML file.
4. Every prompt file.
5. Every test file.
6. `requirements.txt`.
7. `.env.example`.
8. `.gitignore`.
9. Streamlit configuration.
10. Docker configuration.
11. README.

Ensure imports are correct.

Ensure modules can be executed.

Ensure Streamlit starts successfully.

Ensure tests can run.

Ensure no API key is hard-coded.

Ensure the application gracefully handles missing API credentials.

Ensure the application works in deterministic mode when LLM is unavailable.

After generating the project:

1. Run all tests.
2. Fix import errors.
3. Fix type errors.
4. Fix dependency issues.
5. Run Streamlit.
6. Validate resume processing.
7. Validate ChromaDB indexing.
8. Validate JD analysis.
9. Validate Qwen integration using a mocked test.
10. Validate session isolation.
11. Validate exports.
12. Update README with actual commands.

The final result must be a **complete, runnable, GitHub-ready Streamlit RAG application**, not a conceptual example.