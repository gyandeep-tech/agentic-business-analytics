from typing import TypedDict, Optional, List


class BusinessAgentState(TypedDict, total=False):

    # ========================================================
    # USER QUESTION
    # ========================================================

    question: str


    # ========================================================
    # ROUTING
    # ========================================================

    route: str

    # Multiple agents selected by planner
    planned_agents: List[str]


    # ========================================================
    # AGENT RESULTS
    # ========================================================

    sql_result: Optional[dict]

    eda_result: Optional[dict]

    forecast_result: Optional[dict]

    anomaly_result: Optional[dict]

    rfm_result: Optional[dict]

    insight_result: Optional[dict]

    recommendation_result: Optional[dict]


    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    final_answer: str


    # ========================================================
    # TRACKING
    # ========================================================

    agents_used: List[str]