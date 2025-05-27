Create unlogged table if not exists products(
    id serial primary key,
    prodName text,
    price numeric
)

create table if not exists transactionsLog (
    id SERIAL PRIMARY KEY,
    idTransaction TEXT,
    operation TEXT,  -- insert, update, delete
    prevData JSONB,
    afterData JSONB,
    transactionStatus TEXT,     -- commit ou rollback
    moment TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)