# Console – Protheus Send (Meep)

Este console executa o reprocessamento unitário de pedidos no endpoint de envio para o Protheus, utilizando a API da Meep.

O objetivo é permitir a execução controlada de reenvios, a partir de uma lista de identificadores obtidos diretamente do banco de dados ou sistemas internos.

---

## Finalidade

Executar chamadas HTTP POST para o endpoint de envio de notas para o Protheus.

com intervalo fixo entre as requisições, exibindo integralmente o retorno no console.

---

## Arquivo do console

`protheus_send.py`

---

## Fonte dos pedidos

Os pedidos devem ser informados no arquivo:

`invoiceOrderId.txt`

**Localização**: raiz do projeto

**Formato esperado**:

```
3A203277-9465-4C00-8AB7-9ED1FED7A8E9
530FC928-CAC7-432B-82FC-1FD01BB0CB9F
```

Cada linha representa um identificador de pedido.

---

## Configuração de ambiente

Este console utiliza exclusivamente variáveis de ambiente para definição de rotas.

Arquivo `.env`:

MEEP_BASE_URL=https://third-api.meep.cloud/api/

MEEP_PROTHEUS_SEND_PATH= `endpoint para envio das notas`

---

## Funcionamento

O fluxo de execução é:

1. leitura do arquivo `invoiceOrderId.txt`
2. montagem dinâmica da URL a partir do `.env`
3. envio unitário de cada pedido
4. espera de 2 segundos entre requisições
5. exibição do retorno da API no console

---

## Regras técnicas

- não há persistência de resultado
- não há mapeamentos auxiliares
- não há leitura de dados externos além do arquivo de entrada
- não há enriquecimento de payload
- não há dependência de regras de negócio

---

## Tratamento de erros

O console trata explicitamente:

- falhas de conexão
- timeout
- respostas que não estejam em formato JSON

Falhas de comunicação não interrompem o processamento dos demais pedidos.

---

## Indicação de uso

Este console é indicado para:

- reprocessamentos pontuais
- validações de integração
- suporte operacional
- troubleshooting técnico

---

## Extensão

Novos consoles neste repositório devem seguir:

- leitura de dados de entrada via arquivo
- configuração de rotas via `.env`
- documentação própria em `docs/<nome_console>.md`