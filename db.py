import sqlite3 

class Database:
    def __init__(self, file):
        self.conn = sqlite3.connect(file)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS spendings(
            id INTEGER PRIMARY KEY, 
            date text,
            food real,
            transport real, 
            shopping real,
            total real);
        """)
        self.conn.commit()
    
    def fetch(self):
        self.cur.execute("SELECT * FROM spendings")
        rows = self.cur.fetchall()
        return rows

    def insert(self, date, food, transport, shopping):
        total = sum([float(food), float(transport), float(shopping)])
        self.cur.execute("INSERT INTO spendings VALUES(NULL, ?, ?, ?, ?, ?)", (date, food, transport, shopping, total))
        self.conn.commit()
    
    def remove(self, id):
        self.cur.execute("DELETE FROM spendings WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, date, food, transport, shopping):
        total = sum([float(food), float(transport), float(shopping)])
        self.cur.execute("UPDATE spendings SET date=?, food=?, transport=?, shopping=?, total=? WHERE id=?",
            (date, food, transport, shopping, total, id)
        )
        self.conn.commit()

    def get_id(self, date):
        res = self.cur.execute("SELECT id FROM spendings WHERE date=?", (date,))
        id = res.fetchone()[0]
        return id

    def __del__(self):
        self.conn.close()
    
