import json

from langchain_core.tools import tool

from analytics.recommendation_tools import (
    get_recommendation_evidence
)


@tool
def get_recommendation_evidence_tool() -> str:
    """
    Get deterministic business evidence for generating
    business recommendations.

    The tool provides measurable business conditions.
    It does not generate recommendations itself.
    """

    result = get_recommendation_evidence()

    return json.dumps(
        result,
        default=str
    )