
import os
import pandas as pd


# =========================================================
# File Paths
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MONTHLY_SALES_PATH = os.path.join(
    BASE_DIR, "data", "processed", "monthly_sales.csv"
)

FORECAST_PATH = os.path.join(
    BASE_DIR, "data", "processed", "revenue_forecast.csv"
)

ANOMALY_PATH = os.path.join(
    BASE_DIR, "data", "processed", "monthly_anomaly_detection.csv"
)

RFM_PATH = os.path.join(
    BASE_DIR, "data", "processed", "customer_rfm_advanced.csv"
)


# =========================================================
# Helper Functions
# =========================================================

def load_csv(path, required_columns, dataset_name):
    """Load a CSV file and validate its required columns."""

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"{dataset_name} file not found: {path}"
        )

    df = pd.read_csv(path)

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{dataset_name} is missing columns: "
            f"{missing_columns}"
        )

    return df


def safe_float(value):
    """Convert a value to a JSON-friendly float or None."""

    if pd.isna(value):
        return None

    return float(value)


def safe_int(value):
    """Convert a value to a JSON-friendly integer or None."""

    if pd.isna(value):
        return None

    return int(value)


# =========================================================
# Main Business Summary
# =========================================================

def get_business_summary():
    """
    Generate a deterministic business summary for the Insight Agent.

    Includes:
    - Historical monthly sales
    - Revenue forecast
    - Monthly anomaly detection
    - Customer RFM segmentation

    This function calculates metrics only. It does not generate
    interpretations or recommendations.
    """

    # -----------------------------------------------------
    # 1. Historical Monthly Sales
    # -----------------------------------------------------

    sales_df = load_csv(
        MONTHLY_SALES_PATH,
        ["date", "revenue", "orders"],
        "Monthly sales"
    )

    sales_df["date"] = pd.to_datetime(
        sales_df["date"],
        errors="coerce"
    )

    sales_df["revenue"] = pd.to_numeric(
        sales_df["revenue"],
        errors="coerce"
    )

    sales_df["orders"] = pd.to_numeric(
        sales_df["orders"],
        errors="coerce"
    )

    sales_df = sales_df.dropna(
        subset=["date", "revenue", "orders"]
    )

    sales_df = sales_df.sort_values("date").reset_index(
        drop=True
    )

    if sales_df.empty:
        raise ValueError(
            "Monthly sales dataset contains no valid records."
        )

    total_revenue = sales_df["revenue"].sum()
    total_orders = sales_df["orders"].sum()

    average_monthly_revenue = sales_df["revenue"].mean()

    highest_revenue_row = sales_df.loc[
        sales_df["revenue"].idxmax()
    ]

    latest_row = sales_df.iloc[-1]

    previous_row = (
        sales_df.iloc[-2]
        if len(sales_df) >= 2
        else None
    )

    if (
        previous_row is not None
        and previous_row["revenue"] != 0
    ):
        latest_growth_pct = (
            (
                latest_row["revenue"]
                - previous_row["revenue"]
            )
            / abs(previous_row["revenue"])
        ) * 100
    else:
        latest_growth_pct = None

    sales_summary = {
        "months_analyzed": int(len(sales_df)),
        "total_revenue": float(total_revenue),
        "total_orders": safe_int(total_orders),
        "average_monthly_revenue": float(
            average_monthly_revenue
        ),
        "highest_revenue_month": {
            "date": str(
                highest_revenue_row["date"].date()
            ),
            "revenue": float(
                highest_revenue_row["revenue"]
            ),
            "orders": safe_int(
                highest_revenue_row["orders"]
            ),
        },
        "latest_month": {
            "date": str(latest_row["date"].date()),
            "revenue": float(latest_row["revenue"]),
            "orders": safe_int(latest_row["orders"]),
            "growth_pct": safe_float(latest_growth_pct),
        },
    }

    # -----------------------------------------------------
    # 2. Revenue Forecast
    # -----------------------------------------------------

    forecast_df = load_csv(
        FORECAST_PATH,
        ["forecast_date", "forecast_revenue"],
        "Revenue forecast"
    )

    forecast_df["forecast_date"] = pd.to_datetime(
        forecast_df["forecast_date"],
        errors="coerce"
    )

    forecast_df["forecast_revenue"] = pd.to_numeric(
        forecast_df["forecast_revenue"],
        errors="coerce"
    )

    forecast_df = forecast_df.dropna(
        subset=["forecast_date", "forecast_revenue"]
    )

    forecast_df = forecast_df.sort_values(
        "forecast_date"
    ).reset_index(drop=True)

    if forecast_df.empty:
        raise ValueError(
            "Revenue forecast dataset contains no valid records."
        )

    forecast_total = forecast_df[
        "forecast_revenue"
    ].sum()

    forecast_average = forecast_df[
        "forecast_revenue"
    ].mean()

    first_forecast = forecast_df.iloc[0]
    last_forecast = forecast_df.iloc[-1]

    if first_forecast["forecast_revenue"] != 0:
        forecast_growth_pct = (
            (
                last_forecast["forecast_revenue"]
                - first_forecast["forecast_revenue"]
            )
            / abs(first_forecast["forecast_revenue"])
        ) * 100
    else:
        forecast_growth_pct = None

    forecast_summary = {
        "forecast_months": int(len(forecast_df)),
        "total_forecast_revenue": float(forecast_total),
        "average_forecast_revenue": float(
            forecast_average
        ),
        "first_forecast": {
            "date": str(
                first_forecast["forecast_date"].date()
            ),
            "revenue": float(
                first_forecast["forecast_revenue"]
            ),
        },
        "last_forecast": {
            "date": str(
                last_forecast["forecast_date"].date()
            ),
            "revenue": float(
                last_forecast["forecast_revenue"]
            ),
        },
        "forecast_period_growth_pct": safe_float(
            forecast_growth_pct
        ),
    }

    # -----------------------------------------------------
    # 3. Monthly Anomaly Detection
    # -----------------------------------------------------

    anomaly_df = load_csv(
        ANOMALY_PATH,
        ["order_purchase_timestamp", "anomaly"],
        "Anomaly detection"
    )

    anomaly_df["order_purchase_timestamp"] = pd.to_datetime(
        anomaly_df["order_purchase_timestamp"],
        errors="coerce"
    )

    anomaly_df = anomaly_df.dropna(
        subset=["order_purchase_timestamp"]
    )

    anomaly_df["anomaly"] = (
        anomaly_df["anomaly"]
        .astype("string")
        .str.strip()
    )

    anomaly_count = int(
        anomaly_df["anomaly"]
        .str.casefold()
        .eq("anomaly")
        .sum()
    )

    total_anomaly_months = int(len(anomaly_df))

    anomaly_percentage = (
        (anomaly_count / total_anomaly_months) * 100
        if total_anomaly_months > 0
        else 0.0
    )

    anomaly_summary = {
        "total_months": total_anomaly_months,
        "anomaly_count": anomaly_count,
        "anomaly_percentage": float(anomaly_percentage),
    }

    # -----------------------------------------------------
    # 4. Customer RFM Segmentation
    # -----------------------------------------------------

    rfm_df = load_csv(
        RFM_PATH,
        ["Monetary", "Recency", "Frequency", "Segment"],
        "Customer RFM"
    )

    for column in ["Monetary", "Recency", "Frequency"]:
        rfm_df[column] = pd.to_numeric(
            rfm_df[column],
            errors="coerce"
        )

    rfm_df["Segment"] = (
        rfm_df["Segment"]
        .astype("string")
        .str.strip()
    )

    # Keep rows with valid RFM metrics and a segment.
    rfm_df = rfm_df.dropna(
        subset=[
            "Monetary",
            "Recency",
            "Frequency",
            "Segment",
        ]
    )

    rfm_df = rfm_df[
        rfm_df["Segment"] != ""
    ].copy()

    if rfm_df.empty:
        raise ValueError(
            "Customer RFM dataset contains no valid records."
        )

    # Count unique customers when the identifier is available.
    if "customer_unique_id" in rfm_df.columns:
        total_customers = int(
            rfm_df["customer_unique_id"].nunique()
        )
    else:
        total_customers = int(len(rfm_df))

    segment_counts = (
        rfm_df["Segment"]
        .value_counts()
        .to_dict()
    )

    largest_segment = (
        max(segment_counts, key=segment_counts.get)
        if segment_counts
        else None
    )

    customers_summary = {
        "total_customers": total_customers,
        "average_monetary": safe_float(
            rfm_df["Monetary"].mean()
        ),
        "average_recency": safe_float(
            rfm_df["Recency"].mean()
        ),
        "average_frequency": safe_float(
            rfm_df["Frequency"].mean()
        ),
        "segment_counts": {
            str(key): int(value)
            for key, value in segment_counts.items()
        },
        "largest_segment": largest_segment,
    }

    # -----------------------------------------------------
    # 5. Final Summary
    # -----------------------------------------------------

    summary = {
        "sales": sales_summary,
        "forecast": forecast_summary,
        "anomalies": anomaly_summary,
        "customers": customers_summary,
    }

    return summary

def format_business_facts(summary):
    """
    Format business metrics directly from the deterministic summary.
    The LLM does not generate or rewrite these facts.
    """

    sales = summary["sales"]
    forecast = summary["forecast"]
    anomalies = summary["anomalies"]
    customers = summary["customers"]

    def money(value):
        return (
            f"${value:,.2f}"
            if value is not None
            else "N/A"
        )

    def number(value):
        return (
            f"{value:,.2f}"
            if value is not None
            else "N/A"
        )

    def percent(value):
        return (
            f"{value:+.2f}%"
            if value is not None
            else "N/A"
        )

    def month(date_value):
        return pd.Timestamp(date_value).strftime("%B %Y")

    highest = sales["highest_revenue_month"]
    latest = sales["latest_month"]
    first = forecast["first_forecast"]
    last = forecast["last_forecast"]

    lines = [
        "## FACTS",
        "",
        "### Historical Sales",
        f"- Months analyzed: {sales['months_analyzed']}",
        f"- Total revenue: {money(sales['total_revenue'])}",
        f"- Total orders: {sales['total_orders']:,}",
        f"- Average monthly revenue: "
        f"{money(sales['average_monthly_revenue'])}",
        f"- Highest-revenue month: {month(highest['date'])}",
        f"  - Revenue: {money(highest['revenue'])}",
        f"  - Orders: {highest['orders']:,}",
        f"- Latest month: {month(latest['date'])}",
        f"  - Revenue: {money(latest['revenue'])}",
        f"  - Orders: {latest['orders']:,}",
        f"  - Month-over-month growth: "
        f"{percent(latest['growth_pct'])}",
        "",
        "### Revenue Forecast",
        f"- Forecast months: {forecast['forecast_months']}",
        f"- Total forecast revenue: "
        f"{money(forecast['total_forecast_revenue'])}",
        f"- Average forecast revenue per month: "
        f"{money(forecast['average_forecast_revenue'])}",
        f"- First forecast month: {month(first['date'])}",
        f"  - Estimated revenue: {money(first['revenue'])}",
        f"- Last forecast month: {month(last['date'])}",
        f"  - Estimated revenue: {money(last['revenue'])}",
        f"- First-to-last forecast change: "
        f"{percent(forecast['forecast_period_growth_pct'])}",
        "",
        "### Anomaly Detection",
        f"- Months analyzed: {anomalies['total_months']}",
        f"- Anomalies detected: {anomalies['anomaly_count']}",
        f"- Anomaly percentage: "
        f"{anomalies['anomaly_percentage']:.2f}%",
        "",
        "### Customer Analysis",
        f"- Total customers: {customers['total_customers']:,}",
        f"- Average monetary value: "
        f"{money(customers['average_monetary'])}",
        f"- Average recency: "
        f"{number(customers['average_recency'])} days",
        f"- Average purchase frequency: "
        f"{number(customers['average_frequency'])}",
        f"- Largest customer segment: "
        f"{customers['largest_segment']}",
        "- Customer segment counts:",
    ]

    for segment, count in sorted(
        customers["segment_counts"].items(),
        key=lambda item: item[1],
        reverse=True,
    ):
        lines.append(f"  - {segment}: {count:,}")

    return "\n".join(lines)
