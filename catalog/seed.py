from db import init_db,connect
import json
init_db()
with connect() as c:
    c.execute("INSERT OR IGNORE INTO platforms VALUES (?,?,?,?,?)",('symbian-9.1','Symbian','9.1','armv5',None))
    c.execute("INSERT OR IGNORE INTO platforms VALUES (?,?,?,?,?)",('dos-3','DOS','3.x','x86',None))
    c.execute("INSERT OR IGNORE INTO devices VALUES (?,?,?,?,?,?)",('nokia-n73','Nokia','N73','symbian-9.1',64,json.dumps({'display':'240x320','formats':['sis','jar','jad']})))
    c.execute("INSERT OR IGNORE INTO devices VALUES (?,?,?,?,?,?)",('ibm-pc-xt','IBM','PC XT','dos-3',0,json.dumps({'formats':['img','dsk','exe','com']})))
    c.execute("INSERT OR IGNORE INTO software VALUES (?,?,?,?,?)",('demo-notepad','Demo Notepad','Universal Store Demo',None,'Reference software record'))
    c.execute("INSERT OR IGNORE INTO releases VALUES (?,?,?,?,?)",('demo-notepad-1','demo-notepad','1.0','1999-01-01','archive'))
    c.execute("INSERT OR IGNORE INTO packages VALUES (?,?,?,?,?,?,?,?)",('demo-notepad-sis','demo-notepad-1','sis','armv5',None,'reconstruction','unknown',None))
print('Seed complete')
