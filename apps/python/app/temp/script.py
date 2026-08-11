from pathlib import Path
import sqlite3

import sqlite_vec


DB_PATH = Path(
    "/home/jegan/Desktop/Anvil/apps/python/anvil.db"
)


connection = sqlite3.connect(DB_PATH)

try:
    connection.enable_load_extension(True)
    sqlite_vec.load(connection)
    connection.enable_load_extension(False)

    connection.execute(
        "DELETE FROM chunk_vectors"
    )

    connection.commit()

    print("Vector table cleared.")

finally:
    connection.close()