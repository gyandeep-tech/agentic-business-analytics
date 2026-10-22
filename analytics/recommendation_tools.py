import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def get_recommendation_evidence():
    """
    Generate deterministic business evidence that can be used
    by the Recommendation Agent.

    This function does not generate recommendations.
    It only identifies measurable business conditions.
    """

    monthly_sales = pd.read_csv(
        PROCESSED_DIR / "monthly_sales.csv"
    )

    forecast = pd.read_csv(
        PROCESSED_DIR / "revenue_forecast.csv"
    )

    anomalies = pd.read_csv(
        PROCESSED_DIR / "monthly_anomaly_detection.csv"
    )

    rfm = pd.read_csv(
        PROCESSED_DIR / "customer_rfm_advanced.csv"
    )

    # ---------------------------------------------------------
    # 1. Latest month performance
    # ---------------------------------------------------------

    monthly_sales["date"] = pd.to_datetime(
        monthly_sales["date"]
    )

    monthly_sales = monthly_sales.sort_values("date")

    latest = monthly_sales.iloc[-1]

    previous = monthly_sales.iloc[-2]

    latest_growth = (
        (latest["revenue"] - previous["revenue"])
        / previous["revenue"]
    ) * 100

    latest_month = {
        "date": str(latest["date"]),
        "revenue": float(latest["revenue"]),
        "orders": int(latest["orders"]),
        "previous_month_revenue": float(previous["revenue"]),
        "growth_pct": float(latest_growth)
    }

   # ---------------------------------------------------------
    # 2. Forecast evidence
    # ---------------------------------------------------------

    forecast["forecast_date"] = pd.to_datetime(
        forecast["forecast_date"]
    )

    forecast = forecast.sort_values("forecast_date")

    first_forecast = forecast.iloc[0]
    last_forecast = forecast.iloc[-1]

    forecast_growth = (
        (
            last_forecast["forecast_revenue"]
            - first_forecast["forecast_revenue"]
        )
        / first_forecast["forecast_revenue"]
    ) * 100

    forecast_evidence = {
        "forecast_months": len(forecast),
        "average_forecast_revenue": float(
            forecast["forecast_revenue"].mean()
        ),
        "first_forecast_date": str(
            first_forecast["forecast_date"]
        ),
        "first_forecast_revenue": float(
            first_forecast["forecast_revenue"]
        ),
        "last_forecast_date": str(
            last_forecast["forecast_date"]
        ),
        "last_forecast_revenue": float(
            last_forecast["forecast_revenue"]
        ),
        "forecast_period_growth_pct": float(
            forecast_growth
        )
    }

    # ---------------------------------------------------------
    # 3. Anomaly evidence
    # ---------------------------------------------------------

    anomaly_rows = anomalies[
        anomalies["anomaly"] == "Anomaly"
    ]

    anomaly_evidence = {
        "months_analyzed": int(len(anomalies)),
        "anomaly_count": int(len(anomaly_rows)),
        "anomaly_months": [
            str(x)
            for x in pd.to_datetime(
                anomaly_rows["order_purchase_timestamp"]
            ).dt.strftime("%Y-%m")
        ]
    }

    # ---------------------------------------------------------
    # 4. RFM segment evidence
    # ---------------------------------------------------------

    segment_counts = (
        rfm["Segment"]
        .value_counts()
        .to_dict()
    )

    largest_segment = max(
        segment_counts,
        key=segment_counts.get
    )

    rfm_evidence = {
        "total_customers": int(len(rfm)),
        "largest_segment": largest_segment,
        "largest_segment_count": int(
            segment_counts[largest_segment]
        ),
        "segment_counts": {
            str(k): int(v)
            for k, v in segment_counts.items()
        }
    }

    # ---------------------------------------------------------
    # 5. Evidence flags
    # ---------------------------------------------------------

    flags = []

    if latest_growth < 0:
        flags.append(
            "Latest month revenue decreased compared "
            "with the previous month."
        )

    if forecast_growth < 0:
        flags.append(
            "Forecast revenue decreases from the first "
            "to the last forecast month."
        )

    if len(anomaly_rows) > 0:
        flags.append(
            "The anomaly detector identified unusual months "
            "requiring investigation."
        )

    if "At Risk" in segment_counts:
        flags.append(
            "An At Risk customer segment is present."
        )

    if "Lost Customers" in segment_counts:
        flags.append(
            "A Lost Customers segment is present."
        )

    return {
        "latest_month": latest_month,
        "forecast": forecast_evidence,
        "anomalies": anomaly_evidence,
        "customers": rfm_evidence,
        "evidence_flags": flags
    }