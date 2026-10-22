from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


# ============================================================
# LLM
# ============================================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


# ============================================================
# PLANNER PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are the Planner Agent for an E-Commerce Business
Analytics platform.

Your job is to determine which analytics agents are
required to answer the user's question.

You MUST NOT answer the question.

Available agents:

sql
eda
forecast
anomaly
rfm
insight
recommendation


AGENT PURPOSES
------------------------------------------------------------

sql:
Use for exact database metrics, transactional data,
SQL aggregations, rankings, filtering, joins and
business KPIs.

eda:
Use for historical monthly sales analysis,
historical trends, highest/lowest months and
exploratory sales analysis.

forecast:
Use for future or predicted revenue and sales.

anomaly:
Use for detected anomalies, unusual months,
abnormal patterns and outliers.

rfm:
Use for customer segmentation and RFM analysis.

insight:
Use to combine multiple business analytics areas
and produce an overall business analysis.

recommendation:
Use when the user asks what actions the business
should take or asks for recommendations.


PLANNING RULES
------------------------------------------------------------

1. Simple factual questions should normally use
   only the specialized agent required.

2. Questions about exact database metrics should
   use sql.

3. Historical monthly sales questions should use eda.

4. Future/prediction questions should use forecast.

5. Anomaly questions should use anomaly.

6. Customer segmentation/RFM questions should use rfm.

7. Overall business analysis may require multiple
   analytical agents.

8. If the user asks for an overall analysis AND
   recommendations, use the relevant analytical
   agents first, followed by insight and
   recommendation.

9. Do not add agents that are unrelated to the question.

10. If only one specialized agent is required,
    return only that agent.


MULTI-AGENT EXAMPLE
------------------------------------------------------------

Question:
"Analyze our overall business performance and
recommend what we should do."

Return:

sql,eda,forecast,anomaly,rfm,insight,recommendation


ANOTHER EXAMPLE
------------------------------------------------------------

Question:
"Analyze our sales performance and forecast the
next six months."

Return:

eda,forecast,insight


ANOTHER EXAMPLE
------------------------------------------------------------

Question:
"What are our customer segments?"

Return:

rfm


ANOTHER EXAMPLE
------------------------------------------------------------

Question:
"What is our total revenue?"

Return:

sql


OUTPUT FORMAT
------------------------------------------------------------

Return ONLY a comma-separated list of agent names.

Do not use brackets.

Do not explain your decision.

Do not answer the question.

Use lowercase.

Valid agent names:

sql
eda
forecast
anomaly
rfm
insight
recommendation
"""


# ============================================================
# VALID AGENTS
# ============================================================

VALID_AGENTS = {
    "sql",
    "eda",
    "forecast",
    "anomaly",
    "rfm",
    "insight",
    "recommendation"
}


# ============================================================
# PLANNER FUNCTION
# ============================================================

def plan_question(question: str) -> list[str]:

    response = llm.invoke([
        ("system", SYSTEM_PROMPT),
        ("human", question)
    ])

    raw_output = response.content.strip().lower()

    agents = [
        agent.strip()
        for agent in raw_output.split(",")
        if agent.strip() in VALID_AGENTS
    ]

    # Safety fallback
    if not agents:
        return ["sql"]

    # Remove duplicates while preserving order
    agents = list(dict.fromkeys(agents))

    return agents