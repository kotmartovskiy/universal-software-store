import sqlite3
from pathlib import Path
DB=Path(__file__).resolve().parent.parent/'store.db'

def migrate():
    con=sqlite3.connect(DB)
    try:
        cols={r[1] for r in con.execute("PRAGMA table_info(platforms)")}
        for name,typ in [("memory_min_mb","INTEGER"),("runtimes_json","TEXT")]:
            if name not in cols: con.execute(f"ALTER TABLE platforms ADD COLUMN {name} {typ}")
        cols={r[1] for r in con.execute("PRAGMA table_info(packages)")}
        additions=[("min_os_version","TEXT"),("max_os_version","TEXT"),("abi","TEXT"),("min_ram_mb","INTEGER"),("runtime","TEXT"),("compatibility_layer","TEXT"),("emulator","TEXT")]
        for name,typ in additions:
            if name not in cols: con.execute(f"ALTER TABLE packages ADD COLUMN {name} {typ}")
        con.executescript("""CREATE TABLE IF NOT EXISTS dependencies(id INTEGER PRIMARY KEY AUTOINCREMENT,package_id TEXT NOT NULL,depends_on_package_id TEXT,software_id TEXT,version_constraint TEXT,kind TEXT DEFAULT 'runtime',optional INTEGER DEFAULT 0,FOREIGN KEY(package_id) REFERENCES packages(id),FOREIGN KEY(depends_on_package_id) REFERENCES packages(id),FOREIGN KEY(software_id) REFERENCES software(id));
CREATE TABLE IF NOT EXISTS compatibility_tools(id TEXT PRIMARY KEY,name TEXT NOT NULL,kind TEXT NOT NULL,source_url TEXT,description TEXT);
CREATE INDEX IF NOT EXISTS idx_dependencies_package ON dependencies(package_id);
CREATE INDEX IF NOT EXISTS idx_dependencies_software ON dependencies(software_id);""")
        con.commit()
    finally: con.close()

if __name__=='__main__': migrate(); print('migration ok')
