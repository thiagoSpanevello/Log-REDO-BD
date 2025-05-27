import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
try:
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    conn.set_client_encoding('UTF8')
    print("Conexão com o banco de dados bem-sucedida!")
    conn.close()
except Exception as e:
    print("Erro ao conectar com o banco de dados:", e)
