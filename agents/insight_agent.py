
import re
from datetime import date
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from analytics.business_insight_tools import (
    get_business_summary,
    format_business_facts,
)

load_dotenv()


# =========================================================
# LLM Configuration
# =========================================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
)


# =========================================================
# Insight Agent Prompts
# =========================================================


OBSERVATION_PROMPT = """
You are a careful e-commerce business analyst.

Analyze the supplied factual report and answer the user's
question with observations and cautious interpretations.

RULES:

EVIDENCE AND ACCURACY:
1. Use the supplied factual report as your only source of
   business evidence.
2. Do not repeat the factual report unnecessarily.
3. Do not introduce dates, numerical values, percentages,
   or ratios that are not explicitly supplied.
4. Do not calculate new metrics.
5. A single monthly decline does not establish a long-term trend.
6. Forecasts are estimates, not guaranteed outcomes.
7. Do not infer causation from aggregate statistics.
8. Do not claim that customer churn or inactivity is proven
   solely by average RFM metrics or segment sizes.
9. Do not invent explanations involving promotions, pricing,
   inventory, seasonality, customer behavior, or supply constraints.
10. Distinguish observed facts from possible interpretations.
11. State clearly when the available data cannot establish a cause.
12. Do not claim that forecasted revenue implies increased sales
    volume, higher average order value, or improved customer
    behavior unless the supplied evidence directly supports it.
13. Do not claim that a customer segment guarantees future revenue
    growth or a particular business outcome.

DATE AND FORECAST INTERPRETATION:
14. The current date will be provided with the user's question.
15. Check forecast dates against the supplied current date.
16. If a forecast period is entirely in the past, describe it as
    a historical forecast period recorded in the dataset.
17. Do not call historical forecast dates upcoming or future months.
18. If the forecast period is in the future, describe it as an
    estimate rather than an observed business result.
19. Do not assume that actual results are available for a forecast
    period unless the supplied report contains them.

FORMATTING AND OUTPUT:
20. Use readable Markdown headings and bullet points.
21. Do not use HTML tags.
22. Check spacing between words before responding.
23. Include a space after punctuation where grammatically appropriate.
24. Avoid merged words, missing spaces, and inconsistent formatting.
25. Use clear, grammatically correct English.
26. Avoid repeating numerical facts unnecessarily.
27. Do not present unsupported assumptions as established facts.
28. Do not treat correlations, averages, or segment labels as
    proof of customer behavior or business causes.
29. Do not claim that a forecast is accurate or reliable unless
    forecast evaluation metrics are supplied.
30. Describe forecasts using terms such as "the model projected"
    or "the forecast estimated."
31. Recommendations must be presented as potential actions to
    investigate, not guaranteed ways to improve revenue.
32. Do not infer repeat-purchase behavior from average purchase
    frequency without supporting distribution or cohort data.
33. When the dataset's dates are historical, clearly identify
    them as historical dates and never describe them as the
    next six months from the current date.
34. Ensure every interpretation is directly supported by the
    supplied facts or explicitly labeled as a possibility.

Return only these sections:

## OBSERVATIONS

## INTERPRETATION

End with a concise, evidence-based takeaway.
"""



RECOMMENDATION_PROMPT = """
You are a cautious e-commerce business analytics advisor.

Your task is to propose practical, measurable business
experiments using only the supplied factual report.

EVIDENCE RULES:
1. Use the supplied report as your only source of business evidence.
2. Do not repeat or rewrite the numerical facts unnecessarily.
3. Do not introduce new dates, numerical values, percentages,
   ratios, or calculated metrics.
4. Do not invent customer histories, campaign results,
   acquisition costs, product-level findings, or preferences.
5. Do not infer causes from correlations or aggregate data.
6. Do not claim that customers are inactive, have churned, or
   have not purchased recently unless the evidence establishes it.
7. Do not claim that any customer segment has the highest
   monetary value unless the report explicitly confirms it.
8. Do not assume anomalies were caused by promotions, pricing,
   inventory, seasonality, or supply constraints.
9. Do not treat forecasts as guaranteed outcomes.
10. Do not interpret one monthly decline as proof of a long-term trend.
11. Do not recommend pricing, inventory, referral, or product-specific
    strategies without supporting evidence.
12. Distinguish observed facts from proposed hypotheses.
13. Do not invent baselines, targets, or expected improvements.

RECOMMENDATION RULES:
14. Provide no more than four recommendations.
15. Prioritize experiments connected directly to a supplied
    metric or customer segment.
16. Use customer segment names exactly as shown in the report.
17. Frame each recommendation as a test, not a guaranteed solution.
18. Explain the evidence motivating the experiment without
    repeating numerical facts.
19. Explain how the experiment should be evaluated.
20. Do not claim that an experiment will definitely improve
    sales, revenue, retention, or customer engagement.
21. If additional data is needed, identify what should be collected.
22. Avoid repetitive recommendations and generic advice.
23. Use clear, grammatically correct English with proper spacing.
24. Use readable Markdown only. Do not use HTML tags.
25. Do not describe a customer segment as dormant, inactive,
    or close to disengagement unless the supplied evidence
    explicitly establishes that behavior.

26. Do not treat segment size alone as proof of an opportunity
    or likely business impact.

27. Before describing a forecast period as upcoming, check
    whether its dates are actually in the future relative
    to the current date. Otherwise, call it the forecast
    period recorded in the dataset.

28. Leave spaces between all words, after punctuation,
    and before parenthetical examples where grammatically
    appropriate.

29. Do not claim that additional variables explain anomalies
    unless the analysis actually tests that relationship.

30. Describe statistical testing as a proposed evaluation
    method, not as a test that has already been performed.

OUTPUT FORMAT:

## RECOMMENDATIONS

For each recommendation, use this structure:

### Recommendation: [Short title]

- **Action:** Describe the proposed experiment.
- **Evidence:** Identify the supplied fact motivating it.
- **Measurement:** Explain how its outcome should be evaluated.

Leave a blank line between recommendations.

Finish with a brief, cautious takeaway.

If the evidence is insufficient to support a specific
recommendation, state what additional data is needed.
"""


# =========================================================
# Request Classification
# =========================================================

def wants_recommendations(question: str) -> bool:
    """
    Determine whether the user requests recommendations,
    suggestions, or an action plan.
    """

    question_lower = question.casefold()

    recommendation_keywords = (
        "recommend",
        "recommendation",
        "suggest",
        "suggestion",
        "improve sales",
        "increase sales",
        "boost sales",
        "grow revenue",
        "action plan",
        "strategies",
        "what should we do",
        "how can we improve",
        "how to improve",
        "ways to improve",
        "how can the business grow",
        "improve business performance",
        "business recommendations",
    )

    return any(
        keyword in question_lower
        for keyword in recommendation_keywords
    )


# =========================================================
# Narrative Cleaning
# =========================================================

def clean_narrative(text: str) -> str:
    """
    Normalize whitespace and remove common formatting issues.

    This function does not modify the deterministic FACTS
    section or attempt to rewrite business claims.
    """

    # Normalize line endings and unusual spaces.
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")
    text = text.replace("\u00a0", " ")
    text = text.replace("\u200b", "")

    # Remove HTML tags.
    text = re.sub(r"<[^>]+>", "", text)

    # Remove trailing spaces from individual lines.
    text = "\n".join(
        line.strip()
        for line in text.splitlines()
    )

    # Reduce excessive blank lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# =========================================================
# Narrative Validation
# =========================================================

def validate_narrative(
    narrative: str,
    facts: str,
    is_recommendation: bool,
) -> tuple[bool, str]:
    """
    Perform basic formatting checks and block selected
    unsupported recommendation types.

    These checks cannot guarantee that every business claim
    is correct. The facts argument is retained for future
    fact-level validation.
    """

    narrative = clean_narrative(narrative)

    if not narrative:
        return False, ""

    # Detect known merged-word issues and suspicious patterns.
    merged_word_patterns = (
        r"\bomittedto\b",
        r"\bsectionabove\b",
        r"\bfromthe\b",
        r"\bofthe\b",
        r"\bwiththe\b",
        r"\bandthe\b",
        r"\binthe\b",
        r"\bforthe\b",
        r"\breceivesno\b",
        r"\bexpectationofcontinued\b",
        r"\brevenuefromthe\b",
        r"\bandsegment\b",
        # Number directly followed by a long word.
        r"\b\d+[a-zA-Z]{4,}\b",
        # Common function words merged with following words.
        r"\b(?:the|and|with|from|for|to)(?:customer|revenue|sales|segment|month|business|forecast|data|result|trend|report)\b",
    )

    for pattern in merged_word_patterns:
        if re.search(
            pattern,
            narrative,
            flags=re.IGNORECASE,
        ):
            return False, narrative

    # Block selected recommendation types requiring evidence
    # that is not available in the current business summary.
    unsupported_recommendations = (
        "abandoned-cart",
        "abandoned cart",
        "referral incentive",
        "referral incentives",
        "referral program",
        "referral programmes",
        "dynamic pricing",
        "inventory reallocation",
        "bundle offer",
        "bundle offers",
    )

    if is_recommendation:
        narrative_lower = narrative.casefold()

        if any(
            phrase in narrative_lower
            for phrase in unsupported_recommendations
        ):
            return False, narrative

    return True, narrative


# =========================================================
# Fallback Narrative
# =========================================================

def get_validation_fallback() -> str:
    """
    Provide a safe message when narrative validation fails.
    The deterministic factual report is still returned.
    """

    return (
        "## Additional Analysis\n\n"
        "The generated narrative did not pass the basic "
        "formatting and reliability checks. It has been "
        "omitted to avoid presenting potentially unsupported "
        "conclusions. Please use the verified FACTS section "
        "above."
    )


# =========================================================
# Insight Agent
# =========================================================

def ask_insight_agent(question: str) -> dict:
    """
    Generate business facts deterministically with Python,
    then use Groq for observations or recommendations.

    The FACTS section is generated independently of the LLM.
    """

    # -----------------------------------------------------
    # Step 1: Retrieve the deterministic business summary
    # -----------------------------------------------------

    try:
        summary = get_business_summary()
        facts = format_business_facts(summary)

    except Exception as exc:
        return {
            "question": question,
            "answer": (
                "I could not retrieve the business summary. "
                "Please check the processed datasets and "
                "business-summary configuration. "
                f"Error: {exc}"
            ),
            "tool_called": True,
        }

    # -----------------------------------------------------
    # Step 2: Classify the request
    # -----------------------------------------------------

    is_recommendation = wants_recommendations(question)

    if is_recommendation:
        task_prompt = RECOMMENDATION_PROMPT
    else:
        task_prompt = OBSERVATION_PROMPT

    # -----------------------------------------------------
    # Step 3: Generate the narrative with Groq
    # -----------------------------------------------------

    try:
        response = llm.invoke(
            [
                ("system", task_prompt),
                (
                    "human",
                    f"Current date: {date.today().isoformat()}\n\n"
                    "Use the following factual report as your "
                    "only source of business evidence.\n\n"
                    f"{facts}\n\n"
                    f"User question: {question}",
                ),
            ]
        )

        narrative = response.content

        if not isinstance(narrative, str):
            narrative = str(narrative)

        # -------------------------------------------------
        # Step 4: Clean and validate the narrative
        # -------------------------------------------------

        is_valid, narrative = validate_narrative(
            narrative=narrative,
            facts=facts,
            is_recommendation=is_recommendation,
        )

        if not is_valid:
            print("\n[DEBUG] Insight narrative failed validation.")
            print("[DEBUG] Rejected narrative:")
            print(narrative)

            narrative = get_validation_fallback()

        # -------------------------------------------------
        # Step 5: Combine deterministic facts and narrative
        # -------------------------------------------------

        answer = f"{facts}\n\n{narrative}"

        return {
            "question": question,
            "answer": answer,
            "tool_called": True,
        }

    except Exception as exc:
        # Preserve the factual report even if Groq fails.
        return {
            "question": question,
            "answer": (
                f"{facts}\n\n"
                "## Additional Analysis\n\n"
                "The factual report was generated successfully, "
                "but the LLM analysis failed. "
                f"Error: {exc}"
            ),
            "tool_called": True,
        }
