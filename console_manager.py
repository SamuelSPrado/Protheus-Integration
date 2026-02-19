import argparse
import sys

from consoles.protheus_send import run as protheus_send_run
from consoles.meep_start_on_order_created import run as meep_start_on_order_created_run


CONSOLES = {
    "protheus-send": protheus_send_run,
    "meep-start-on-order-created": meep_start_on_order_created_run,
}


def show_menu() -> str:
    print("\nSelecione o console para executar:\n")

    keys = list(CONSOLES.keys())

    for i, name in enumerate(keys, start=1):
        print(f"{i} - {name}")

    print()

    try:
        option = int(input("Opção: ").strip())
    except ValueError:
        raise RuntimeError("Opção inválida.")

    if option < 1 or option > len(keys):
        raise RuntimeError("Opção fora do intervalo.")

    return keys[option - 1]


def main():
    parser = argparse.ArgumentParser(
        description="Console manager – Protheus / Meep"
    )

    parser.add_argument(
        "console",
        nargs="?",
        choices=CONSOLES.keys(),
        help="Console a ser executado"
    )

    args = parser.parse_args()

    if args.console:
        console_name = args.console
    else:
        console_name = show_menu()

    try:
        CONSOLES[console_name]()
    except KeyboardInterrupt:
        print("\nExecução interrompida.")
        sys.exit(130)


if __name__ == "__main__":
    main()