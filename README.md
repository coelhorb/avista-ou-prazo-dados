# avista-ou-prazo-dados

Dados públicos lidos pelo app À Vista ou a Prazo em `docs/rates.json`.

- `params.json`: parâmetros editados à mão, como as regras do Mercado Pago.
- O workflow diário junta esses parâmetros à cotação do AUPO11.
- O workflow precisa do secret `BRAPI_TOKEN`. Sem ele, ou se a consulta falhar, mantém a última cotação conhecida.
