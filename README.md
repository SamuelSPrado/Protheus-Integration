# Protheus Integration – Consoles Meep

Este repositório concentra consoles técnicos de integração com a API da Meep, voltados a operações de suporte, reprocessamentos e validações de integração com sistemas como Protheus, ERP e PDV.

O repositório é estruturado para conter múltiplos consoles independentes, cada um documentado de forma isolada.

---

## Objetivo

Centralizar ferramentas de execução técnica para:

- reprocessamento de integrações
- validação de endpoints
- apoio a operações e suporte
- automação futura de rotinas

---

## Estrutura do repositório atual

````
├── protheus_send.py
├── invoiceOrderId.txt
├── .env
├── .gitignore
├── README.md
└── docs
└── protheus_send.md
````

---

## Consoles disponíveis

| Console | Descrição |
|------|--------
| protheus_send | Reenvio de pedidos para o Protheus via API Meep |

A documentação detalhada de cada console encontra-se na pasta `docs`.

---

## Padrões do projeto

- cada console possui arquivo próprio
- cada console possui documentação própria em `docs`
- o arquivo `.env` é utilizado exclusivamente para configuração de rotas e parâmetros
- arquivos de entrada são utilizados para dados operacionais
- não há persistência de saída
- não há regras de negócio implementadas

---

## Organização da documentação

A documentação detalhada de cada console está localizada em:

`docs/<nome_console>.md`

Este arquivo README é mantido apenas como visão geral do repositório.

