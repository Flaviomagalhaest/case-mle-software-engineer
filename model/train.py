"""Treina o modelo de propensão do case (didático, dados sintéticos).

Uso:  python model/train.py
Gera: model/propensity_model.pkl e data/sample_customers.csv
"""
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent.parent
SEED = 42
MODEL_VERSION = "1.3.0"
FEATURES = [
    "age",
    "monthly_income_brl",
    "tenure_months",
    "products_held",
    "app_logins_30d",
    "has_active_credit",
]


def make_customers(n: int, rng: np.random.Generator) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "age": rng.integers(18, 75, n),
            "monthly_income_brl": rng.integers(1500, 25000, n),
            "tenure_months": rng.integers(1, 180, n),
            "products_held": rng.integers(1, 7, n),
            "app_logins_30d": rng.integers(0, 40, n),
            "has_active_credit": rng.integers(0, 2, n),
        }
    )


def make_labels(df: pd.DataFrame, rng: np.random.Generator) -> np.ndarray:
    """Regra sintética: mais relacionamento e engajamento => mais propensão."""
    z = (
        -3.9
        + 0.025 * df["tenure_months"]
        + 0.45 * df["products_held"]
        + 0.07 * df["app_logins_30d"]
        + 0.00006 * df["monthly_income_brl"]
        + 0.2 * df["has_active_credit"]
        + 0.01 * df["age"]
    )
    p = 1 / (1 + np.exp(-z))
    return (rng.random(len(df)) < p).astype(int)


def main() -> None:
    rng = np.random.default_rng(SEED)
    X = make_customers(5000, rng)
    y = make_labels(X, rng)

    model = Pipeline(
        [("scale", StandardScaler()), ("clf", LogisticRegression(max_iter=1000))]
    )
    model.fit(X[FEATURES], y)
    model.model_version = MODEL_VERSION
    model.feature_names = FEATURES

    with open(ROOT / "model" / "propensity_model.pkl", "wb") as f:
        pickle.dump(model, f)

    sample = make_customers(17, np.random.default_rng(7))
    # metade da amostra com perfil de baixo relacionamento, para cobrir as 3 faixas
    low = slice(0, 8)
    sample.loc[low, "tenure_months"] = sample.loc[low, "tenure_months"] // 6 + 1
    sample.loc[low, "products_held"] = 1
    sample.loc[low, "app_logins_30d"] = sample.loc[low, "app_logins_30d"] // 6
    sample.insert(0, "customer_id", [str(4800 + i) for i in range(17)])
    fixed = pd.DataFrame(
        [
            # cliente do exemplo do enunciado
            {"customer_id": "4821", "age": 41, "monthly_income_brl": 9500,
             "tenure_months": 72, "products_held": 3, "app_logins_30d": 14,
             "has_active_credit": 1},
            # perfis de borda: dados incompletos (o agente não deve inventar score)
            {"customer_id": "5001", "age": 29, "monthly_income_brl": np.nan,
             "tenure_months": 8, "products_held": 1, "app_logins_30d": 3,
             "has_active_credit": 0},
            {"customer_id": "5002", "age": np.nan, "monthly_income_brl": 4200,
             "tenure_months": np.nan, "products_held": 2, "app_logins_30d": 9,
             "has_active_credit": 1},
        ]
    )
    sample = pd.concat([fixed, sample], ignore_index=True)
    sample.to_csv(ROOT / "data" / "sample_customers.csv", index=False)
    print("ok:", MODEL_VERSION)


if __name__ == "__main__":
    main()
