from sqlalchemy.engine import create_engine
import sys
import sqlite3 as lite


con = None

try:
    con = lite.connect('test.db')
    
    cur = con.cursor()    
    #cur.execute('SELECT SQLITE_VERSION()')
    cur.execute("create table if not exists server(Id INT, Name TEXT, Value TEXT)")
    cur.execute("INSERT INTO server VALUES(1,'IsDisabled','False')")
    con.commit()
    #data = cur.fetchone()
    
    #print "SQLite version: %s" % data                
    
except lite.Error, e:
    
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
    
    if con:
        con.close()

