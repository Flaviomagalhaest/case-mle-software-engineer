"""Exemplo de uso do modelo: carrega o .pkl e calcula score + fatores.

Uso:  python model/predict.py 4821
O modelo só devolve score e fatores; a faixa (alta/média/baixa) NÃO faz parte dele.
"""
import pickle
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent


def load_model(path: Path = ROOT / "model" / "propensity_model.pkl"):
    with open(path, "rb") as f:
        return pickle.load(f)


def predict(model, row: dict) -> dict:
    cols = model.feature_names
    missing = [c for c in cols if row.get(c) is None or pd.isna(row.get(c))]
    if missing:
        raise ValueError(f"dados insuficientes: {missing}")

    X = pd.DataFrame([row])[cols]
    score = float(model.predict_proba(X)[0, 1])

    # contribuição de cada variável = coeficiente * valor padronizado
    scaled = model.named_steps["scale"].transform(X)[0]
    contrib = model.named_steps["clf"].coef_[0] * scaled
    top = [cols[i] for i in sorted(range(len(cols)), key=lambda i: -contrib[i])[:3]]

    return {
        "customer_id": str(row["customer_id"]),
        "propensity_score": round(score, 2),
        "model_version": model.model_version,
        "top_features": top,
    }


if __name__ == "__main__":
    df = pd.read_csv(ROOT / "data" / "sample_customers.csv", dtype={"customer_id": str})
    row = df[df.customer_id == sys.argv[1]].iloc[0].to_dict()
    print(predict(load_model(), row))
