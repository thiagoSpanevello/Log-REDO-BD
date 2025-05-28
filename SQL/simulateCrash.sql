DROP TABLE IF EXISTS clientes;

CREATE UNLOGGED TABLE clientes (
    id SERIAL PRIMARY KEY,
    nome TEXT,
    saldo NUMERIC
);