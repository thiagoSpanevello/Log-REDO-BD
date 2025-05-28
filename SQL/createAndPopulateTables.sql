create UNLOGGED table if not exists clientes (
    id SERIAL PRIMARY KEY,
    nome TEXT,
    saldo NUMERIC
);

create table if not exists transactionsLog (
    id SERIAL PRIMARY KEY,
    idTransaction TEXT,
    operation TEXT,  -- insert, update, delete
    prevData JSONB,
    afterData JSONB,
    transactionStatus TEXT,     -- commit ou rollback
    moment TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

create or replace function log_transition() returns trigger as $$
declare 
    v_txid text;
begin
    v_txid := txid_current()::text;

    if TG_OP = 'INSERT' then
        insert into transactionsLog(idTransaction, operation, prevData, afterData, transactionStatus)
        values (v_txid, 'insert', NULL, to_jsonb(NEW), 'COMMIT');
    
    elsif TG_OP = 'UPDATE' then 
        insert into transactionsLog(idTransaction, operation, prevData, afterData, transactionStatus)
        values(v_txid, 'update', to_jsonb(OLD), to_jsonb(NEW), 'COMMIT');

    elsif TG_OP = 'DELETE' then
        insert into transactionsLog(idTransaction, operation, prevData, afterData, transactionStatus)
        values(v_txid, 'delete', to_jsonb(OLD), NULL, 'COMMIT');
    
    end if;

    return NULL;
end;
$$ LANGUAGE plpgsql;

create trigger trigger_log_insert 
after insert on clientes 
for each row execute function log_transition();

create trigger trigger_log_update
after update on clientes
for each row execute function log_transition();

create trigger trigger_log_delete
after delete on clientes
for each row execute function log_transition();

BEGIN;
INSERT INTO clientes (nome, saldo) VALUES ('Cliente 1', 1000.00);
UPDATE clientes SET saldo = saldo + 50 WHERE id = 1;
COMMIT;

BEGIN;
INSERT INTO clientes (nome, saldo) VALUES ('Cliente 2', 100.00);
UPDATE clientes SET saldo = saldo + 50 WHERE id = 2;
COMMIT;

BEGIN;
INSERT INTO clientes (nome, saldo) VALUES ('Cliente 3', 900.00);
UPDATE clientes SET saldo = saldo + 50 WHERE id = 3;
COMMIT;

BEGIN;
INSERT INTO clientes (nome, saldo) VALUES ('Cliente 4', 123.00);
UPDATE clientes SET saldo = saldo + 50 WHERE id = 4;
COMMIT;

BEGIN;
INSERT INTO clientes (nome, saldo) VALUES ('Cliente 6', 3210.00);
COMMIT;
