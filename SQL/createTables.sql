-- Remove o trigger e a função se já existirem

DROP TABLE transactionsLog;
DROP TABLE clientes;

-- Criação da tabela de log
CREATE TABLE transactionsLog (
    id SERIAL PRIMARY KEY,
    idTransaction TEXT,
    operation TEXT,  -- insert, update, delete, start, commit
    prevData JSONB,
    afterData JSONB,
    transactionStatus TEXT,     -- commit ou rollback
    moment TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criação da tabela clientes
CREATE UNLOGGED TABLE clientes (
    id SERIAL PRIMARY KEY,
    nome TEXT,
    saldo NUMERIC
);


-- Função de log
CREATE OR REPLACE FUNCTION log_transition() RETURNS trigger AS $$
DECLARE
    v_txid TEXT := txid_current()::TEXT;
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO transactionsLog(idTransaction, operation, prevData, afterData, transactionStatus)
        VALUES (v_txid, 'insert', NULL, to_jsonb(NEW), NULL);
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO transactionsLog(idTransaction, operation, prevData, afterData, transactionStatus)
        VALUES (v_txid, 'update', to_jsonb(OLD), to_jsonb(NEW), NULL);
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO transactionsLog(idTransaction, operation, prevData, afterData, transactionStatus)
        VALUES (v_txid, 'delete', to_jsonb(OLD), NULL, NULL);
    END IF;
    RETURN new;
END;
$$ LANGUAGE plpgsql;

-- Criação do trigger
CREATE TRIGGER trigger_log_event
BEFORE INSERT OR UPDATE OR DELETE ON clientes
FOR EACH ROW
EXECUTE FUNCTION log_transition();
