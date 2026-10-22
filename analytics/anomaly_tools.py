import os
import pandas as pd


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

ANOMALY_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "monthly_anomaly_detection.csv"
)


def load_anomaly_data():
    """
    Load the processed monthly anomaly detection dataset.
    """

    if not os.path.exists(ANOMALY_PATH):
        raise FileNotFoundError(
            f"Anomaly detection file not found: {ANOMALY_PATH}"
        )

    df = pd.read_csv(ANOMALY_PATH)

    if df.empty:
        raise ValueError(
            "monthly_anomaly_detection.csv is empty."
        )

    required_columns = [
        "order_purchase_timestamp",
        "revenue",
        "orders",
        "average_order_value",
        "average_delivery_days",
        "late_orders",
        "anomaly_prediction",
        "anomaly"
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

    df["order_purchase_timestamp"] = pd.to_datetime(
        df["order_purchase_timestamp"],
        errors="coerce"
    )

    numeric_columns = [
        "revenue",
        "orders",
        "average_order_value",
        "average_delivery_days",
        "late_orders",
        "anomaly_prediction"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    df = df.dropna(
        subset=[
            "order_purchase_timestamp",
            "revenue",
            "anomaly"
        ]
    )

    if df.empty:
        raise ValueError(
            "No valid anomaly records found."
        )

    return df.sort_values(
        "order_purchase_timestamp"
    ).reset_index(drop=True)


def get_anomaly_summary():
    """
    Generate deterministic anomaly detection summary.
    """

    df = load_anomaly_data()

    anomaly_df = df[
        df["anomaly"] == "Anomaly"
    ].copy()

    normal_df = df[
        df["anomaly"] == "Normal"
    ].copy()

    total_months = len(df)

    total_anomalies = len(anomaly_df)

    total_normal_months = len(normal_df)

    anomaly_percentage = (
        (total_anomalies / total_months) * 100
        if total_months > 0
        else 0
    )

    # -----------------------------------------------------
    # Highest anomaly revenue
    # -----------------------------------------------------

    highest_anomaly = None

    if not anomaly_df.empty:

        highest_anomaly_row = anomaly_df.loc[
            anomaly_df["revenue"].idxmax()
        ]

        highest_anomaly = {
            "date": highest_anomaly_row[
                "order_purchase_timestamp"
            ],
            "revenue": float(
                highest_anomaly_row["revenue"]
            ),
            "orders": float(
                highest_anomaly_row["orders"]
            ),
            "average_order_value": float(
                highest_anomaly_row[
                    "average_order_value"
                ]
            ),
            "average_delivery_days": float(
                highest_anomaly_row[
                    "average_delivery_days"
                ]
            ),
            "late_orders": float(
                highest_anomaly_row[
                    "late_orders"
                ]
            )
        }

    # -----------------------------------------------------
    # Lowest anomaly revenue
    # -----------------------------------------------------

    lowest_anomaly = None

    if not anomaly_df.empty:

        lowest_anomaly_row = anomaly_df.loc[
            anomaly_df["revenue"].idxmin()
        ]

        lowest_anomaly = {
            "date": lowest_anomaly_row[
                "order_purchase_timestamp"
            ],
            "revenue": float(
                lowest_anomaly_row["revenue"]
            ),
            "orders": float(
                lowest_anomaly_row["orders"]
            ),
            "average_order_value": float(
                lowest_anomaly_row[
                    "average_order_value"
                ]
            ),
            "average_delivery_days": float(
                lowest_anomaly_row[
                    "average_delivery_days"
                ]
            ),
            "late_orders": float(
                lowest_anomaly_row[
                    "late_orders"
                ]
            )
        }

    # -----------------------------------------------------
    # Individual anomaly records
    # -----------------------------------------------------

    anomalies = []

    for _, row in anomaly_df.iterrows():

        anomalies.append(
            {
                "date": row[
                    "order_purchase_timestamp"
                ],
                "revenue": float(
                    row["revenue"]
                ),
                "orders": float(
                    row["orders"]
                ),
                "average_order_value": float(
                    row["average_order_value"]
                ),
                "average_delivery_days": float(
                    row["average_delivery_days"]
                ),
                "late_orders": float(
                    row["late_orders"]
                )
            }
        )

    summary = {
        "total_months": int(total_months),

        "total_anomalies": int(
            total_anomalies
        ),

        "total_normal_months": int(
            total_normal_months
        ),

        "anomaly_percentage": float(
            anomaly_percentage
        ),

        "highest_anomaly": highest_anomaly,

        "lowest_anomaly": lowest_anomaly,

        "anomalies": anomalies
    }

    return summary