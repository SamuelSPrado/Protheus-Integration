import os
from typing import List, Tuple

from infra.sqlserver import get_connection


class InvoiceAnalyzer:

    def __init__(
        self,
        input_file: str = "access_keys.txt",
        output_file: str = "invoice_analysis_result.txt"
    ):
        self.input_path = self._resolve_input_path(input_file)
        self.output_path = self._resolve_output_path(output_file)

        self.access_keys = self._load_access_keys()

        if not self.access_keys:
            raise RuntimeError("Nenhuma chave de acesso encontrada no arquivo.")

        self.conn = get_connection()

        self.invoice_ids: List[str] = []
        self.orders_without_invoice: List[str] = []
        self.invalid_keys: List[str] = []

    # ----------------------------
    # paths
    # ----------------------------

    def _resolve_input_path(self, filename: str) -> str:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base, "input", filename)

    def _resolve_output_path(self, filename: str) -> str:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base, "output", filename)

    # ----------------------------
    # load
    # ----------------------------

    def _load_access_keys(self) -> List[str]:
        with open(self.input_path, encoding="utf-8") as f:
            return [l.strip() for l in f if l.strip()]

    # ----------------------------
    # main
    # ----------------------------

    def processar(self) -> None:
        cursor = self.conn.cursor()

        for chave in self.access_keys:
            try:
                self._processar_chave(cursor, chave)
            except Exception:
                self.invalid_keys.append(chave)

        self._salvar_resultado()

    # ----------------------------
    # core
    # ----------------------------

    def _processar_chave(self, cursor, chave: str) -> None:

        pedido_nfce = self._buscar_pedido_nfce(cursor, chave)

        if not pedido_nfce:
            self.invalid_keys.append(chave)
            return

        pedido_id, protocolo, nfce_status, conta_id = pedido_nfce

        if not self._pedido_valido(protocolo, nfce_status):
            self.invalid_keys.append(chave)
            return

        historico_associacao_id = self._buscar_historico_associacao(cursor, pedido_id)

        # pré-pago
        if historico_associacao_id is None:
            self._processar_pre_pago(cursor, pedido_id)
            return

        # pós-pago
        if conta_id:
            rows = self._buscar_pos_pago_por_conta(cursor, pedido_id)
        else:
            rows = self._buscar_pos_pago_por_historico(cursor, pedido_id)

        self._processar_lista_pos_pago(rows)

    # ----------------------------
    # queries
    # ----------------------------

    def _buscar_pedido_nfce(self, cursor, chave: str):

        cursor.execute(
            """
            select id, protocolo, NFCEStatus, contaid
            from vwPedidoPosNfce
            where ChaveDeAcesso = ?
            """,
            chave
        )

        return cursor.fetchone()

    def _buscar_historico_associacao(self, cursor, pedido_id: str):

        cursor.execute(
            """
            select historicoassociacaoid
            from vwPedidoPos
            where id = ?
            """,
            pedido_id
        )

        row = cursor.fetchone()
        return row[0] if row else None

    def _buscar_pos_pago_por_conta(self, cursor, pedido_id: str):

        cursor.execute(
            """
            select pp.id, iv.id
            from vwHistoricoAssociacao h 
            inner join vwPedidoPos pp on h.id = pp.HistoricoAssociacaoId 
            inner join vwPedidoPOSDetalhe pd on pp.id = pd.PedidoPOSId
            left join vwInvoiceOrder iv on pp.id = iv.id
            where h.id = (
                select ContaId
                from vwPedidoPosNfce
                where id = ?
            )
            """,
            pedido_id
        )

        return cursor.fetchall()

    def _buscar_pos_pago_por_historico(self, cursor, pedido_id: str):

        cursor.execute(
            """
            select pp.id, iv.id
            from vwHistoricoAssociacao h 
            inner join vwPedidoPos pp on h.id = pp.HistoricoAssociacaoId 
            inner join vwPedidoPOSDetalhe pd on pp.id = pd.PedidoPOSId
            left join vwInvoiceOrder iv on pp.id = iv.id
            where h.id = (
                select HistoricoAssociacaoId
                from vwPedidoPos
                where id = ?
            )
            """,
            pedido_id
        )

        return cursor.fetchall()

    def _buscar_invoice_pre_pago(self, cursor, pedido_id: str):

        cursor.execute(
            """
            select iv.id
            from vwinvoiceorder iv
            where iv.id = ?
            """,
            pedido_id
        )

        row = cursor.fetchone()
        return row[0] if row else None

    # ----------------------------
    # business rules
    # ----------------------------

    def _pedido_valido(self, protocolo, status) -> bool:

        if protocolo is None:
            return False

        if str(protocolo).strip() == "000000000000000":
            return False

        if status != 2:
            return False

        return True

    def _processar_pre_pago(self, cursor, pedido_id: str) -> None:

        invoice_id = self._buscar_invoice_pre_pago(cursor, pedido_id)

        if invoice_id:
            self.invoice_ids.append(invoice_id)
        else:
            self.orders_without_invoice.append(pedido_id)

    def _processar_lista_pos_pago(self, rows: List[Tuple]) -> None:

        if not rows:
            return

        invoices = [r[1] for r in rows if r[1] is not None]

        if invoices:
            for inv in invoices:
                self.invoice_ids.append(inv)
        else:
            for r in rows:
                self.orders_without_invoice.append(r[0])

    # ----------------------------
    # output
    # ----------------------------

    def _salvar_resultado(self) -> None:

        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        with open(self.output_path, "w", encoding="utf-8") as f:

            f.write("InvoiceID prontos para envio\n")
            for i in self.invoice_ids:
                f.write(f"{i}\n")

            f.write("\nPedidos sem invoiceID\n")
            for p in self.orders_without_invoice:
                f.write(f"{p}\n")

            f.write("\nChaves não notificadas no sistema Integrado e/ou status inválido\n")
            for k in self.invalid_keys:
                f.write(f"{k}\n")


def run() -> None:
    print("Console – Invoice Analyzer (SQL Server)")
    analyzer = InvoiceAnalyzer()
    analyzer.processar()
    print("Processamento finalizado.")


if __name__ == "__main__":
    run()