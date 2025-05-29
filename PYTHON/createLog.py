import re
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
    has_commit = any(stmt.strip().upper() == 'COMMIT;' for stmt in block)
    cur = conn.cursor()
    txid = None
    try:
        cur.execute('BEGIN;')
        txid = get_current_txid(conn)

        log_event(cur, txid, 'start')

        if has_commit:
            for stmt in block[1:]:
                up = stmt.strip().upper()
                if up == 'COMMIT;':
                    break
                cur.execute(stmt)
            cur.execute('COMMIT;')
            log_event(cur, txid, 'commit')

        else:
            cur.execute('SAVEPOINT sp_dml;')
            operations = []

            for stmt in block[1:]:
                up = stmt.strip().upper()
                cur.execute(stmt)
                if up.startswith('INSERT'):
                    operations.append('insert')
                elif up.startswith('UPDATE'):
                    operations.append('update')
                elif up.startswith('DELETE'):
                    operations.append('delete')

            cur.execute('ROLLBACK TO SAVEPOINT sp_dml;')

            for op in operations:
                log_event(cur, txid, op)

            cur.execute('COMMIT;')

    except Exception as e:
        print(f"Erro no bloco txid={txid}: {e}")
        cur.execute('ROLLBACK;')
    finally:
        cur.close()

if __name__ == '__main__':
    conn = try_connect()
    if conn:
        blocks = read_transactions('C:/Users/Thiago/Desktop/BDII/Log-REDO-BD/SQL/transactions.sql')
        for block in blocks:
            execute_block(conn, block)
        conn.close()
