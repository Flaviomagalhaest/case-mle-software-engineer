# Modelo de propensão (Produto A)

Modelo **didático** que estima a propensão de um cliente a contratar o Produto A. Foi treinado com dados **sintéticos** e serve apenas para o case: não reflete nenhum comportamento real.

- Algoritmo: regressão logística (`StandardScaler` + `LogisticRegression`, em um `Pipeline` do scikit-learn)
- Versão: `1.3.0`
- Arquivo: `propensity_model.pkl` (serializado com `pickle`)
- Dependências: veja `requirements.txt` (o `.pkl` foi gerado com scikit-learn 1.9.1; use a mesma versão para carregar)

> Segurança: arquivos `pickle` executam código ao serem carregados. Carregue apenas arquivos de origem confiável, como este.

## Entrada

Um cliente por chamada. **Todas** as variáveis são obrigatórias; valores ausentes não são aceitos pelo modelo.

| Variável | Tipo | Descrição |
| --- | --- | --- |
| `customer_id` | texto | Identificador do cliente (não é usado pelo modelo) |
| `age` | inteiro | Idade em anos |
| `monthly_income_brl` | número | Renda mensal em reais |
| `tenure_months` | inteiro | Meses de relacionamento com a instituição |
| `products_held` | inteiro | Quantidade de produtos contratados |
| `app_logins_30d` | inteiro | Acessos ao aplicativo nos últimos 30 dias |
| `has_active_credit` | 0 ou 1 | Possui crédito ativo |

## Saída

O modelo devolve apenas a probabilidade da classe positiva, via `predict_proba`. O script `predict.py` monta o formato do contrato do case:

```json
{
  "customer_id": "4821",
  "propensity_score": 0.81,
  "model_version": "1.3.0",
  "top_features": ["has_active_credit", "age", "products_held"]
}
```

- `propensity_score`: número entre 0 e 1.
- `top_features`: as 3 variáveis que mais elevaram o score do cliente em relação à média (coeficiente × valor padronizado). É uma explicação simples e aproximada.
- A **faixa** (alta, média, baixa) **não** faz parte do modelo. Ela é definida pela política descrita no `README.md` da raiz.

## Como usar

```bash
pip install -r model/requirements.txt
python model/predict.py 4821
```

Em código:

```python
from model.predict import load_model, predict

model = load_model()
predict(model, {
    "customer_id": "4821", "age": 41, "monthly_income_brl": 9500,
    "tenure_months": 72, "products_held": 3, "app_logins_30d": 14,
    "has_active_credit": 1,
})
```

Se faltar alguma variável, `predict` levanta `ValueError("dados insuficientes: [...]")`. Os clientes `5001` e `5002` da amostra exercitam esse caso.

## Dados de exemplo

`data/sample_customers.csv` tem 20 clientes fictícios: o `4821` do enunciado, dois com dados faltantes (`5001`, `5002`) e 17 gerados aleatoriamente (`4800` a `4816`), cobrindo as três faixas da política.

## Reprodução e limitações

`python model/train.py` regenera o `.pkl` e o CSV (semente fixa). O modelo é linear, sem validação de qualidade e treinado em dados artificiais. Use-o apenas como caixa-preta para desenhar a solução.
