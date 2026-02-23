import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    driver = os.getenv("SQLSERVER_DRIVER")
    server = os.getenv("SQLSERVER_SERVER")
    database = os.getenv("SQLSERVER_DATABASE")

    if not driver:
        raise RuntimeError("SQLSERVER_DRIVER não definido")

    conn_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        "Authentication=ActiveDirectoryInteractive;"
        "ApplicationIntent=ReadOnly;"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
    )

    return pyodbc.connect(conn_str, timeout=30)