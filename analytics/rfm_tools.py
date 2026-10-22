import os
import pandas as pd


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

RFM_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "customer_rfm_advanced.csv"
)


def load_rfm_data():
    """
    Load the processed advanced RFM customer dataset.
    """

    if not os.path.exists(RFM_PATH):
        raise FileNotFoundError(
            f"RFM file not found: {RFM_PATH}"
        )

    df = pd.read_csv(RFM_PATH)

    if df.empty:
        raise ValueError(
            "customer_rfm_advanced.csv is empty."
        )

    required_columns = [
        "customer_unique_id",
        "Recency",
        "Frequency",
        "Monetary",
        "R_score",
        "F_score",
        "M_score",
        "RFM_score",
        "Segment"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    numeric_columns = [
        "Recency",
        "Frequency",
        "Monetary",
        "R_score",
        "F_score",
        "M_score",
        "RFM_score"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    df = df.dropna(
        subset=[
            "customer_unique_id",
            "Recency",
            "Frequency",
            "Monetary",
            "Segment"
        ]
    )

    if df.empty:
        raise ValueError(
            "No valid RFM customer records found."
        )

    return df


def get_rfm_summary():
    """
    Generate deterministic RFM customer analytics.

    Returns aggregated customer and segment-level metrics.
    Individual customer records are intentionally excluded
    to keep the LLM tool response compact.
    """

    df = load_rfm_data()

    # ---------------------------------------------------------
    # Overall customer metrics
    # ---------------------------------------------------------

    total_customers = len(df)

    total_monetary = df["Monetary"].sum()
    average_monetary = df["Monetary"].mean()
    average_recency = df["Recency"].mean()
    average_frequency = df["Frequency"].mean()

    # ---------------------------------------------------------
    # Segment-level analysis
    # ---------------------------------------------------------

    segment_summary = (
        df.groupby("Segment")
        .agg(
            customers=("customer_unique_id", "count"),
            average_recency=("Recency", "mean"),
            average_frequency=("Frequency", "mean"),
            average_monetary=("Monetary", "mean"),
            total_monetary=("Monetary", "sum")
        )
        .reset_index()
    )

    # Largest segments first
    segment_summary = segment_summary.sort_values(
        "customers",
        ascending=False
    )

    segments = []

    for _, row in segment_summary.iterrows():

        segments.append(
            {
                "segment": row["Segment"],
                "customers": int(row["customers"]),
                "average_recency": float(
                    row["average_recency"]
                ),
                "average_frequency": float(
                    row["average_frequency"]
                ),
                "average_monetary": float(
                    row["average_monetary"]
                ),
                "total_monetary": float(
                    row["total_monetary"]
                )
            }
        )

    # ---------------------------------------------------------
    # Largest customer segment
    # ---------------------------------------------------------

    largest_segment_row = segment_summary.iloc[0]

    largest_segment = {
        "segment": largest_segment_row["Segment"],
        "customers": int(
            largest_segment_row["customers"]
        )
    }

    # ---------------------------------------------------------
    # Highest average monetary segment
    # ---------------------------------------------------------

    highest_monetary_row = segment_summary.loc[
        segment_summary["average_monetary"].idxmax()
    ]

    highest_monetary_segment = {
        "segment": highest_monetary_row["Segment"],
        "average_monetary": float(
            highest_monetary_row["average_monetary"]
        ),
        "total_monetary": float(
            highest_monetary_row["total_monetary"]
        )
    }

    # ---------------------------------------------------------
    # Final summary
    # ---------------------------------------------------------

    summary = {

        "total_customers": int(total_customers),

        "total_monetary": float(
            total_monetary
        ),

        "average_monetary": float(
            average_monetary
        ),

        "average_recency": float(
            average_recency
        ),

        "average_frequency": float(
            average_frequency
        ),

        "largest_segment": largest_segment,

        "highest_monetary_segment":
            highest_monetary_segment,

        "segments": segments
    }

    return summary


def get_customer_rfm(customer_unique_id):
    """
    Retrieve RFM information for a specific customer.
    """

    df = load_rfm_data()

    customer_unique_id = str(customer_unique_id).strip()

    customer = df[
        df["customer_unique_id"] == customer_unique_id
    ]

    if customer.empty:
        return {
            "found": False,
            "message": "Customer not found."
        }

    row = customer.iloc[0]

    return {
        "found": True,
        "customer_unique_id": row["customer_unique_id"],
        "recency": float(row["Recency"]),
        "frequency": float(row["Frequency"]),
        "monetary": float(row["Monetary"]),
        "rfm_score": int(row["RFM_score"]),
        "segment": row["Segment"]
    }