import os
import time
from datetime import datetime
from typing import List

import requests
from dotenv import load_dotenv


class StartOnOrderCreatedProcessor:

    def __init__(
        self,
        input_file: str = "input/OrdersWithoutInvoice.txt",
        sleep_seconds: float = 5.0,
        timeout: int = 30
    ):
        load_dotenv()

        self.sleep_seconds = sleep_seconds
        self.timeout = timeout

        self.base_url = self._get_env("MEEP_BASE_URL")
        self.path_template = self._get_env("MEEP_START_ON_ORDER_CREATED")
        self.token = self._get_env("TOKEN_MEEP")

        self.input_file = self._resolve_input_path(input_file)
        self.order_ids = self._load_order_ids()

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": self.token
        })

        if not self.order_ids:
            raise RuntimeError("Nenhum pedido encontrado no arquivo.")

    def _get_env(self, key: str) -> str:
        value = os.getenv(key)
        if not value:
            raise RuntimeError(f"Variável de ambiente obrigatória não definida: {key}")
        return value.strip()

    def _resolve_input_path(self, filename: str) -> str:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, filename)

    def _load_order_ids(self) -> List[str]:
        with open(self.input_file, encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]

    def _build_url(self, order_id: str) -> str:
        """
        Suporta dois formatos de endpoint:

        PedidoPOS/StartOnOrderCreated/{{PedidoID}}
        ou
        PedidoPOS/StartOnOrderCreated
        """

        path = self.path_template

        if "{{PedidoID}}" in path:
            path = path.replace("{{PedidoID}}", order_id)
            return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

        return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}/{order_id}"

    def processar(self) -> None:
        for index, order_id in enumerate(self.order_ids, start=1):

            self._enviar(order_id)

            if index < len(self.order_ids):
                time.sleep(self.sleep_seconds)

    def _enviar(self, order_id: str) -> None:
        url = self._build_url(order_id)

        try:
            response = self.session.post(url, timeout=self.timeout)
        except requests.RequestException as exc:
            self._print_erro(order_id, exc)
            return

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(
            f"[{now}] "
            f"Pedido={order_id} "
            f"HTTP={response.status_code}"
        )

    def _print_erro(self, order_id: str, exc: Exception) -> None:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(
            f"[{now}] "
            f"Pedido={order_id} "
            f"Erro={str(exc)}"
        )


def run() -> None:
    print("Console – Meep StartOnOrderCreated")
    processor = StartOnOrderCreatedProcessor()
    processor.processar()


if __name__ == "__main__":
    run()