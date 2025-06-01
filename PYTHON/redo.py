from pathlib import Path
from dbConection import try_connect
from createLog import run_setup_sql

con = try_connect()
if (
    con and True
):  # o segundo parâmetro é só pra decidir se vai rodar ou não, mudando pra true ou false
    parent_folder = Path(__file__).parent.parent.resolve() / "SQL"

    path = parent_folder / "simulateCrash.sql"
    run_setup_sql(con, path)
    print("A simulação de crash foi executada.")

if con and True:
    cursor = con.cursor()
    res = cursor.execute(
        """
        SELECT * FROM transactionslog
        """
    )
    res = cursor.fetchall()

    ids = []
    for r in res:
        if r[2] == "commit":
            ids.append(r[1])

    # printando as transações que devem realizar REDO
    print("Operações a ser realizadas:")
    for r in res:
        if r[1] in ids:
            # print(r[2])
            if r[2] != "start" and r[2] != "commit":
                print(f"Realizar um {r[2]} no cliente com id={r[0]}")
                print(f"Na transação={r[1]}")
                print("")

    for r in res:
        if r[1] not in ids:
            continue

        match (r[2]):
            case "insert":
                newData = r[4]

                cursor.execute(
                    """INSERT INTO clientes (id, nome, saldo) VALUES (%s, %s, %s)""",
                    (newData["id"], newData["nome"], newData["saldo"]),
                )

            case "update":
                oldData = r[3]
                newData = r[4]

                cursor.execute(
                    """UPDATE clientes SET nome = %s, saldo = %s 
                        WHERE id = %s""",
                    (newData["nome"], newData["saldo"], oldData["id"]),
                )

            case "delete":
                oldData = r[3]

                cursor.execute(
                    """DELETE FROM clientes WHERE id = %s""", (oldData["id"])
                )

    con.commit()
    # print("Os dados foram restaurados")
    cursor.close()
    con.close()
