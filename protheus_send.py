import os
import time
import json
from datetime import datetime
from typing import List

import requests
from dotenv import load_dotenv


class PedidoProcessor:
    def __init__(
        self,
        input_file: str = "invoiceOrderId.txt",
        sleep_seconds: float = 2.0,
        timeout: int = 30
    ):
        load_dotenv()

        self.sleep_seconds = sleep_seconds
        self.timeout = timeout

        self.base_url = self._get_env("MEEP_BASE_URL")
        self.send_path = self._get_env("MEEP_PROTHEUS_SEND_PATH")

        self.endpoint = self._build_endpoint()

        self.input_file = self._resolve_input_path(input_file)
        self.invoice_ids = self._load_invoice_ids()

        self.session = requests.Session()

        if not self.invoice_ids:
            raise RuntimeError("Nenhum invoiceOrderId encontrado no arquivo.")

    def _get_env(self, key: str) -> str:
        value = os.getenv(key)
        if not value:
            raise RuntimeError(f"Variável de ambiente obrigatória não definida: {key}")
        return value.strip()

    def _build_endpoint(self) -> str:
        return f"{self.base_url.rstrip('/')}/{self.send_path.lstrip('/')}"

    def _resolve_input_path(self, filename: str) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, filename)

    def _load_invoice_ids(self) -> List[str]:
        with open(self.input_file, encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]

    def processar(self) -> None:
        for invoice_id in self.invoice_ids:
            self._enviar(invoice_id)
            time.sleep(self.sleep_seconds)

    def _enviar(self, invoice_id: str) -> None:
        url = f"{self.endpoint}/{invoice_id}"

        inicio = datetime.now()

        try:
            response = self.session.post(url, timeout=self.timeout)
        except requests.RequestException as exc:
            self._print_erro(invoice_id, exc)
            return

        fim = datetime.now()

        try:
            payload = response.json()
        except ValueError:
            payload = response.text

        self._print_resultado(
            invoice_id=invoice_id,
            url=url,
            status_code=response.status_code,
            inicio=inicio,
            fim=fim,
            payload=payload
        )

    def _print_erro(self, invoice_id: str, exc: Exception) -> None:
        print("=" * 80)
        print(f"Invoice ID : {invoice_id}")
        print("Erro de comunicação com a API")
        print(str(exc))

    def _print_resultado(
        self,
        invoice_id: str,
        url: str,
        status_code: int,
        inicio: datetime,
        fim: datetime,
        payload
    ) -> None:
        print("=" * 80)
        print(f"InvoiceID : {invoice_id}")
        #print(f"Endpoint  : {url}")
        print(f"HTTP      : {status_code}")
        #print(f"Início    : {inicio:%d/%m/%Y %H:%M:%S}")
        print(f"Envio     : {fim:%d/%m/%Y %H:%M:%S}")

        print("Resposta:")

        if isinstance(payload, (dict, list)):
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            print(payload)


if __name__ == "__main__":
    print("Console de reprocessamento – Meep / Protheus")

    processor = PedidoProcessor()
    processor.processar()