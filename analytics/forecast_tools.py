import os
import pandas as pd


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

FORECAST_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "revenue_forecast.csv"
)


def load_revenue_forecast():
    """
    Load the processed revenue forecast dataset.
    """

    if not os.path.exists(FORECAST_PATH):
        raise FileNotFoundError(
            f"Revenue forecast file not found: {FORECAST_PATH}"
        )

    df = pd.read_csv(FORECAST_PATH)

    if df.empty:
        raise ValueError(
            "revenue_forecast.csv is empty."
        )

    required_columns = [
        "forecast_date",
        "forecast_revenue"
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

    df["forecast_date"] = pd.to_datetime(
        df["forecast_date"],
        errors="coerce"
    )

    df["forecast_revenue"] = pd.to_numeric(
        df["forecast_revenue"],
        errors="coerce"
    )

    df = df.dropna(
        subset=[
            "forecast_date",
            "forecast_revenue"
        ]
    )

    if df.empty:
        raise ValueError(
            "No valid forecast records found."
        )

    return df.sort_values(
        "forecast_date"
    ).reset_index(drop=True)


def get_revenue_forecast_summary():
    """
    Generate deterministic summary statistics
    from the revenue forecast dataset.
    """

    df = load_revenue_forecast()

    total_forecast_months = len(df)

    total_forecast_revenue = df[
        "forecast_revenue"
    ].sum()

    average_forecast_revenue = df[
        "forecast_revenue"
    ].mean()

    highest_forecast_row = df.loc[
        df["forecast_revenue"].idxmax()
    ]

    lowest_forecast_row = df.loc[
        df["forecast_revenue"].idxmin()
    ]

    first_forecast_row = df.iloc[0]

    last_forecast_row = df.iloc[-1]

    # Growth from first forecast month
    # to last forecast month.
    first_revenue = first_forecast_row[
        "forecast_revenue"
    ]

    last_revenue = last_forecast_row[
        "forecast_revenue"
    ]

    if first_revenue != 0:
        forecast_period_growth_pct = (
            (last_revenue - first_revenue)
            / first_revenue
        ) * 100
    else:
        forecast_period_growth_pct = None

    forecast_records = []

    for _, row in df.iterrows():
        forecast_records.append(
            {
                "date": row["forecast_date"],
                "forecast_revenue": float(
                    row["forecast_revenue"]
                )
            }
        )

    summary = {
        "total_forecast_months": int(
            total_forecast_months
        ),
        "total_forecast_revenue": float(
            total_forecast_revenue
        ),
        "average_forecast_revenue": float(
            average_forecast_revenue
        ),
        "highest_forecast_month": {
            "date": highest_forecast_row[
                "forecast_date"
            ],
            "forecast_revenue": float(
                highest_forecast_row[
                    "forecast_revenue"
                ]
            )
        },
        "lowest_forecast_month": {
            "date": lowest_forecast_row[
                "forecast_date"
            ],
            "forecast_revenue": float(
                lowest_forecast_row[
                    "forecast_revenue"
                ]
            )
        },
        "first_forecast_month": {
            "date": first_forecast_row[
                "forecast_date"
            ],
            "forecast_revenue": float(
                first_forecast_row[
                    "forecast_revenue"
                ]
            )
        },
        "last_forecast_month": {
            "date": last_forecast_row[
                "forecast_date"
            ],
            "forecast_revenue": float(
                last_forecast_row[
                    "forecast_revenue"
                ]
            )
        },
        "forecast_period_growth_pct": (
            None
            if forecast_period_growth_pct is None
            else float(
                forecast_period_growth_pct
            )
        ),
        "forecast": forecast_records
    }

    return summary