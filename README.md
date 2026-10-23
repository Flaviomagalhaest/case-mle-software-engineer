# Case técnico: Agente de IA conversacional sobre modelo de propensão (AWS)

## Contexto e objetivo

O case avalia se você transforma a saída de um modelo preditivo pronto em uma experiência conversacional útil, com uma arquitetura AWS que você consiga defender em uma discussão técnica.

O foco **não** é treinar modelo. Você recebe o binário treinado e precisa desenhar tudo ao redor dele: como servir o modelo, como o agente de IA (GenAI) consome o score, como a estratégia é montada e como o sistema é operado com segurança.

O que o case permite observar:

- Raciocínio de arquitetura: serviços escolhidos, trade-offs e custo.
- Integração de ML com GenAI: onde termina o modelo e onde começa o agente.
- Uso responsável de IA: alucinação, privacidade (LGPD), limites de oferta e rastreabilidade.
- Comunicação: clareza para explicar o desenho e defender decisões.

## Enunciado

**Cenário.** Uma instituição financeira tem um modelo que estima a propensão de cada cliente a contratar o Produto A (por exemplo, um seguro ou um investimento). Hoje o score fica em uma planilha e o gerente de relacionamento não sabe o que fazer com ele.

**Desafio.** Projete uma solução na AWS em que um gerente converse com um agente de IA e receba, em linguagem natural, uma estratégia de abordagem adequada ao nível de propensão do cliente. Exemplo de pergunta: "Como devo abordar o cliente 4821 sobre o Produto A?"

**O que é fornecido**

- O modelo treinado em formato binário (`propensity_model.pkl`, scikit-learn), com a descrição das variáveis de entrada e da saída.
- Uma amostra com 20 clientes fictícios (CSV) para testes.
- A política de abordagem por faixa de propensão (tabela na seção de contratos).

**O que NÃO é pedido:** treinar, ajustar ou avaliar o modelo.

**O que se espera:** que você explique, em desenho e conversa, como resolveria o problema de ponta a ponta, incluindo segurança, custo, observabilidade e riscos de uso de IA generativa.

## Entregáveis

**Obrigatório:** um desenho de arquitetura (draw.io, Excalidraw, PowerPoint ou papel), acompanhado de uma explicação oral. Depois dela, seguimos com uma discussão sobre as suas escolhas.

**Opcional (diferencial, nunca eliminatório):** qualquer parte de uma implementação básica da arquitetura.

| Entregável opcional | Exemplo do que mostrar |
| --- | --- |
| Infraestrutura como código | Terraform com API, função de inferência, tabela de dados e permissões mínimas |
| Contratos de API | Especificação OpenAPI das rotas de chat e de score |
| Código de backend | Handler de inferência e orquestração do agente |
| Prompt do agente | System prompt com regras, tom e limites de oferta |
| Testes | Casos para cada faixa de propensão e para entradas inválidas |

Quem entrega só o desenho não é penalizado. O código serve para aprofundar a conversa, não para substituí-la.

## Requisitos

**Funcionais**

- O gerente pergunta em linguagem natural e recebe uma estratégia coerente com a faixa de propensão do cliente.
- O agente obtém o score chamando o modelo, nunca "adivinhando" o valor.
- A resposta cita os fatores que sustentam a recomendação (por exemplo, renda e tempo de relacionamento).
- A conversa mantém contexto: o gerente pode pedir "e se o cliente recusar?" sem repetir o ID.
- Clientes sem dados suficientes recebem uma resposta honesta, sem score inventado.

**Não funcionais**

- Latência: resposta de chat em poucos segundos; a inferência isoladamente deve ser muito mais rápida que a geração de texto.
- Segurança e LGPD: dados pessoais protegidos, acesso por perfil, nada sensível em logs.
- Governança de IA: ofertas limitadas por política, registro de cada recomendação e do score usado.
- Custo: previsível, com consumo que cresce com o uso (sem servidores ociosos como padrão).
- Observabilidade: métricas, logs e rastreio de cada pergunta até o score e a resposta.
- Evolução: trocar a versão do modelo sem reescrever o agente.

## Contratos e política de exemplo

A política abaixo é fictícia e pode ser ajustada ao seu contexto. O ponto é o agente aplicá-la de forma consistente.

| Faixa | Score do modelo | Estratégia esperada |
| --- | --- | --- |
| Alta | 0,70 ou mais | Abordagem direta, oferta objetiva, próximo passo com data |
| Média | 0,40 a 0,69 | Abordagem consultiva, tirar dúvidas, educar sobre benefícios |
| Baixa | Menos de 0,40 | Sem venda ativa; nutrir relacionamento e reavaliar depois |

**Entrada do modelo** (variáveis fictícias):

```json
{
  "customer_id": "4821",
  "age": 41,
  "monthly_income_brl": 9500,
  "tenure_months": 36,
  "products_held": 3,
  "app_logins_30d": 12,
  "has_active_credit": true
}
```

**Saída do modelo:**

```json
{
  "customer_id": "4821",
  "propensity_score": 0.82,
  "model_version": "1.3.0",
  "top_features": ["tenure_months", "products_held", "app_logins_30d"]
}
```

**Exemplo de pergunta ao agente e resposta (resumida):**

```json
{
  "session_id": "abc-123",
  "message": "Como devo abordar o cliente 4821 sobre o Produto A?"
}
```

```json
{
  "reply": "Propensão alta (0,82). Cliente antigo e engajado no app. Sugiro contato direto, oferta objetiva e proposta de próximo passo ainda esta semana.",
  "tier": "high",
  "score": 0.82,
  "model_version": "1.3.0",
  "trace_id": "f1c2-..."
}
```
