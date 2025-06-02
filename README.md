# Log-REDO-BD
Trabalho de Banco de Dados II, que tem como objetivo simular o uso do REDO.

## Pacotes necessários
- pyscopg2
- pathlib

## Ordem de execução
Primeiro é necessário executar o arquivo createLog.py. Com isso, os clientes e transações serão inseridos no banco.
Com isso, é possível executar o arquivo redo.py, que irá simular um crash no banco de dados, apagando a tabela de clientes. Em seguida, a tabela de transações será lida, fazendo com que todas as transações válidas sejam restauradas no banco.
