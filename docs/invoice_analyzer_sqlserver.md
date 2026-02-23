> Esse console é basicamente um pipeline determinístico.

# invoice_analyzer_sqlserver

Console de análise avançada de pedidos utilizando SQL Server com autenticação MFA.

## Objetivo

A partir de uma lista de chaves de acesso, identificar:

- pedido relacionado
- se o pedido é pré-pago ou pós-pago
- se é pedido splitado
- se existe invoice válida para envio ao Protheus

O console gera um arquivo de saída para posterior tratamento manual ou
execução dos outros consoles do projeto.

## Entrada

Arquivo:

input/access_keys.txt

Formato:

- uma chave de acesso por linha

## Saída

Arquivo:

output/invoice_analysis_result.txt

Formato:

InvoiceID prontos para envio  
Pedidos sem invoiceID  
Chaves não notificadas no sistema Integrado e/ou status inválido

## Conexão com banco

Autenticação via Azure AD MFA (interativa).

Variáveis no .env:

SQLSERVER_DRIVER  
SQLSERVER_SERVER  
SQLSERVER_DATABASE  

## Regras de validação

- protocolo não pode ser nulo nem "000000000000000"
- NFCEStatus deve ser igual a 2
- pedidos sem correspondência na vwPedidoPosNfce são classificados como inválidos

## Execução

Via gerenciador:

python console_manager.py invoice-analyzer-sqlserver