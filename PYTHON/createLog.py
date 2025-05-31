from pathlib import Path
from dbConection import try_connect

def log_event(cur, txid, operation):
    cur.execute(
        """
        INSERT INTO transactionsLog(
            idTransaction, operation, prevData, afterData, transactionStatus
        ) VALUES (%s, %s, NULL, NULL, %s)
        """,
        (txid, operation, operation.upper())
    )

def get_current_txid(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT txid_current()")
        return str(cur.fetchone()[0])

def read_transactions(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    blocks, current, in_tx = [], [], False
    for line in lines:
        stmt = line.strip()
        if stmt.upper() == 'BEGIN;':
            if in_tx and current:
                blocks.append(current)
            current, in_tx = ['BEGIN;'], True
        elif stmt.upper() == 'COMMIT;':
            if in_tx:
                current.append('COMMIT;')
                blocks.append(current)
                current, in_tx = [], False
        else:
            if in_tx and stmt:
                current.append(stmt)
    if in_tx and current:
        blocks.append(current)
    return blocks

def execute_block(conn, block):
    cur = conn.cursor()
    txid = None
    try:
        in_transaction = False

        for stmt in block:
            up = stmt.strip().upper()
            print(f"DEBUG: stmt raw: '{stmt}' | up: '{up}'")
            if up == 'BEGIN;':
                cur.execute('BEGIN;')
                txid = get_current_txid(conn)
                log_event(cur, txid, 'start')
                in_transaction = True

            elif up == 'END;':
                if in_transaction:
                    log_event(cur, txid, 'commit')
                    cur.execute('COMMIT;')
                    conn.commit()
                    in_transaction = False

            else:
                cur.execute(stmt)
        if in_transaction:
            cur.execute('COMMIT;')
            conn.commit()
    except Exception as e:
        print(f"Erro no bloco txid={txid}: {e}")
        cur.execute('ROLLBACK;')
        conn.commit()

    finally:
        cur.close()


def run_setup_sql(conn, path):
    with conn.cursor() as cur:
        with open(path, 'r') as f:
            cur.execute(f.read())
        conn.commit()

if __name__ == '__main__':
    conn = try_connect()
    if conn:
        parent_folder = Path(__file__).parent.parent.resolve()/"SQL"
        
        path = parent_folder / "createTables.sql"
        run_setup_sql(conn, path)

        path = parent_folder / "transactions.sql"
        blocks = read_transactions(path)
        for block in blocks:
            execute_block(conn, block)
        conn.close()

