from pathlib import Path
from dbConection import try_connect
from createLog import run_setup_sql

con = try_connect()
if (con and True): # o segundo parâmetro é só pra decidir se vai rodar ou não, mudando pra true ou false
    parent_folder = Path(__file__).parent.parent.resolve() / "SQL"

    path = parent_folder / "simulateCrash.sql"
    run_setup_sql(con, path)
    print("A simulação de crash foi executada.")

