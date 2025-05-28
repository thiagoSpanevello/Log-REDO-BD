from dbConection import try_connect


def run_sql_file(filepath):
    with open(filepath, 'r') as f:
        sql = f.read()

    conn = try_connect()
    cur = conn.cursor()
    try:
        cur.execute(sql)
        conn.commit()
        print("Script SQL executado com sucesso!")
    except Exception as e:
        print(f"Erro ao executar script SQL: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    run_sql_file('C:/Users/Thiago/Desktop/BDII/Log-REDO-BD/SQL/createAndPopulateTables.sql')
