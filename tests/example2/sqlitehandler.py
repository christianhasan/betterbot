import sqlite3    
import asyncio

class SQL:
    _con = sqlite3.connect("database.db", check_same_thread=False)
    _cur = _con.cursor()
    _cur.execute("CREATE TABLE IF NOT EXISTS banlist(user_id TEXT PRIMARY KEY, roles TEXT, duration INTEGER, time_stamp REAL)")
    _cur.execute("CREATE TABLE IF NOT EXISTS vouches(user_id TEXT PRIMARY KEY, points INTEGER)")
    _lock = asyncio.Lock()
        
    async def insert(self, table: str, columns: str, values: tuple):
        para = ",".join("?" for i in values)
        async with SQL._lock:
            SQL._cur.execute(f"INSERT OR REPLACE INTO {table}({columns}) VALUES ({para})", values)
            SQL._con.commit()

    async def delete(self, table: str, search_column: str = None, values: tuple = None):            
        async with SQL._lock:            
            if search_column:
                if len(values) == 1:
                    para = ",".join("?" for i in values)
                    self._cur.execute(f"DELETE FROM {table} WHERE {search_column} = ({para})", values)
                else:
                    self._cur.execute(f"DELETE FROM {table} WHERE {search_column}", values)
            else:
                self._cur.execute(f"DELETE FROM {table}")
                
            SQL._con.commit()

    async def get(self, table: str, columns: str, search_column: str = None, values: tuple = None):
        async with SQL._lock:
            if search_column is None:
                SQL._cur.execute(f"SELECT {columns} FROM {table}")
            else:
                if len(values) == 1:
                    para = ",".join("?" for i in values)            
                    SQL._cur.execute(f"SELECT {columns} FROM {table} WHERE {search_column} = ({para})", values)
                else:
                    SQL._cur.execute(f"SELECT {columns} FROM {table} WHERE {search_column}", values)

            return SQL._cur.fetchall()