# Console – meep_start_on_order_created

Console responsável por reexecutar o evento
StartOnOrderCreated no Meep para pedidos que não
geraram nota ou integração posterior.

---

## Objetivo

Disparar manualmente o endpoint do Meep responsável
pela recriação do evento de criação do pedido no POS.

---

## Arquivo de entrada

OrdersWithoutInvoice.txt

Formato:

Um ID de pedido por linha.

---

## Variáveis de ambiente

Obrigatórias no .env:

MEEP_BASE_URL  
MEEP_START_ON_ORDER_CREATED  
TOKEN_MEEP  

Exemplo:

MEEP_START_ON_ORDER_CREATED=PedidoPOS/StartOnOrderCreated/{{PedidoID}}

O placeholder {{PedidoID}} é substituído automaticamente.

---

## Funcionamento

- Leitura do arquivo OrdersWithoutInvoice.txt
- Envio individual de cada pedido via POST
- Aguardar 5 segundos entre cada envio
- Impressão no terminal:

- ID do pedido
- data e hora do envio
- status HTTP retornado

---

## Execução

A execução é realizada via console manager:

python console_manager.py meep-start-on-order-created

---

## Observações técnicas

- O console não interrompe o processamento em caso de erro de um pedido.
- As requisições são feitas usando requests.Session.
- O timeout padrão de requisição é de 60 segundos.
