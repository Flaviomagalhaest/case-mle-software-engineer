# Case técnico: Agente de IA conversacional sobre modelo de propensão (AWS)

## Contexto e objetivo

O case avalia se você transforma a saída de um modelo preditivo pronto em um **produto de software bem projetado**: uma experiência conversacional útil, sustentada por uma arquitetura AWS que você consiga defender em uma discussão técnica.

O foco **não** é treinar modelo, e sim **engenharia de software**. Você recebe o binário treinado e precisa desenhar tudo ao redor dele: contratos de API, fluxo síncrono e assíncrono, eventos, padrões de arquitetura, como o agente de IA (GenAI) consome o score, como a estratégia é montada e como o sistema é testado, operado e evoluído com segurança.

O que o case permite observar:

- Raciocínio de arquitetura: estilo arquitetural (API, eventos ou híbrido), padrões adotados, serviços escolhidos, trade-offs e custo.
- Design de software: separação de responsabilidades, contratos, acoplamento, testabilidade e evolução.
- Integração de ML com GenAI: onde termina o modelo e onde começa o agente.
- Uso responsável de IA: alucinação, privacidade (LGPD), limites de oferta e rastreabilidade.
- Comunicação: clareza para explicar o desenho e defender decisões.

## Enunciado

**Cenário.** Uma instituição financeira tem um modelo que estima a propensão de cada cliente a contratar o Produto A (por exemplo, um seguro ou um investimento). Hoje o score fica em uma planilha e o gerente de relacionamento não sabe o que fazer com ele.

**Desafio.** Projete uma solução na AWS em que um gerente converse com um agente de IA e receba, em linguagem natural, uma estratégia de abordagem adequada ao nível de propensão do cliente. Exemplo de pergunta: "Como devo abordar o cliente 4821 sobre o Produto A?"

**O que é fornecido**

- O modelo treinado em formato binário (`model/propensity_model.pkl`, scikit-learn), com a descrição das variáveis de entrada e da saída em `model/README.md`.
- Uma amostra com 20 clientes fictícios (`data/sample_customers.csv`) para testes.
- A política de abordagem por faixa de propensão (tabela na seção de contratos).

**O que NÃO é pedido:** treinar, ajustar ou avaliar o modelo.

**O que se espera:** que você explique, em desenho e conversa, como resolveria o problema de ponta a ponta, incluindo estilo de arquitetura e padrões escolhidos, segurança, custo, observabilidade e riscos de uso de IA generativa.

## Arquivos do repositório

| Caminho | Conteúdo |
| --- | --- |
| `model/propensity_model.pkl` | Modelo treinado (scikit-learn), versão `1.3.0` |
| `model/predict.py` | Exemplo de carga do `.pkl` e cálculo de score e fatores |
| `model/train.py` | Script que gerou o modelo (referência; não é preciso rodar) |
| `model/README.md` | Documentação do modelo: entrada, saída, uso e limitações |
| `data/sample_customers.csv` | 20 clientes fictícios para testes, incluindo casos com dados faltantes |

## Padrões e estilo de arquitetura a explorar

Queremos ver como você **escolhe e justifica** o desenho, não uma lista de siglas. Escolha o que fizer sentido, diga o que descartou e por quê. Pontos para pensar:

- **Estilo de comunicação:** API síncrona (REST, WebSocket ou streaming) para o chat, mensageria e eventos para o que não precisa bloquear o gerente, ou um híbrido. Onde cada um se aplica e qual o custo de misturá-los?
- **Arquitetura orientada a eventos:** quais eventos de domínio existem (por exemplo, recomendação gerada, score calculado, oferta recusada)? Quem publica e quem consome? Como garantir entrega, idempotência, ordenação e reprocessamento? O que fazer com mensagens que falham?
- **Estrutura interna do serviço:** camadas, arquitetura hexagonal (portas e adaptadores), separação entre domínio, orquestração e infraestrutura. Onde ficam o modelo, o LLM e a política de faixas em relação ao domínio?
- **Padrões de integração e resiliência:** gateway/BFF, camada anticorrupção, circuit breaker, retry com backoff, timeout, bulkhead, cache, fallback.
- **Dados e consistência:** separação entre escrita e leitura (CQRS), registro imutável de decisões (event log ou event sourcing), padrão outbox, consistência eventual.
- **Contratos e evolução:** versionamento de API e de eventos, contratos explícitos (OpenAPI, AsyncAPI, schemas), compatibilidade ao trocar a versão do modelo, rollout gradual e feature flags.
- **Qualidade:** estratégia de testes (unitário, contrato, integração, avaliação do agente com casos fixos), CI/CD, ambientes e infraestrutura como código.

Quando apresentar, registre as decisões mais importantes (por exemplo, em ADRs curtos) com contexto, alternativas e consequências.

## Entregáveis

**Obrigatório:** um desenho de arquitetura (draw.io, Excalidraw, PowerPoint ou papel), acompanhado de uma explicação oral. Depois dela, seguimos com uma discussão sobre as suas escolhas.

**Opcional (diferencial, nunca eliminatório):** qualquer parte de uma implementação básica da arquitetura.

| Entregável opcional | Exemplo do que mostrar |
| --- | --- |
| Infraestrutura como código | Terraform com API, função de inferência, tabela de dados e permissões mínimas |
| Contratos de API | Especificação OpenAPI das rotas de chat e de score |
| Contratos de eventos | Especificação AsyncAPI ou JSON Schema dos eventos de domínio |
| Decisões de arquitetura | ADRs curtos com contexto, alternativas e consequências |
| Diagramas | Visão de contexto e contêineres (C4) e diagrama de sequência do fluxo principal |
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
- Resiliência: tolerar falha ou lentidão do modelo, do LLM e dos consumidores de eventos, sem perder registros nem duplicar efeitos.
- Qualidade de engenharia: contratos versionados, código testável e implantação automatizada e repetível.

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
  "tenure_months": 72,
  "products_held": 3,
  "app_logins_30d": 14,
  "has_active_credit": true
}
```

**Saída do modelo:**

```json
{
  "customer_id": "4821",
  "propensity_score": 0.81,
  "model_version": "1.3.0",
  "top_features": ["has_active_credit", "age", "products_held"]
}
```

**Exemplo de evento de domínio** (formato ilustrativo; você pode propor outro):

```json
{
  "event_id": "9b1e-...",
  "event_type": "recommendation.generated",
  "event_version": 1,
  "occurred_at": "2026-01-15T14:32:10Z",
  "trace_id": "f1c2-...",
  "data": {
    "customer_id": "4821",
    "manager_id": "g-102",
    "tier": "high",
    "score": 0.81,
    "model_version": "1.3.0"
  }
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
  "reply": "Propensão alta (0,81). Cliente com várias contratações, crédito ativo e engajado no app. Sugiro contato direto, oferta objetiva e proposta de próximo passo ainda esta semana.",
  "tier": "high",
  "score": 0.81,
  "model_version": "1.3.0",
  "trace_id": "f1c2-..."
}
```
