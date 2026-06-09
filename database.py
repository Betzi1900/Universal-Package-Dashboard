import sqlite3

class Database:
    def __init__(self, db_name="dashboard.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Erstellt die Tabelle für deine Pakete
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS packages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tracking_number TEXT UNIQUE NOT NULL,
                carrier TEXT DEFAULT 'DHL',
                status TEXT DEFAULT 'Wartet auf Update...',
                sender TEXT DEFAULT 'Unbekannt'
            )
        ''')
        self.conn.commit()

    def add_package(self, tracking_number, carrier="DHL"):
        try:
            self.cursor.execute('''
                INSERT INTO packages (tracking_number, carrier)
                VALUES (?, ?)
            ''', (tracking_number, carrier))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False # Paketnummer existiert bereits

    def get_all_packages(self):
        self.cursor.execute("SELECT tracking_number, carrier, status, sender FROM packages")
        return self.cursor.fetchall()

    def update_package_status(self, tracking_number, status, sender):
        self.cursor.execute('''
            UPDATE packages 
            SET status = ?, sender = ?
            WHERE tracking_number = ?
        ''', (status, sender, tracking_number))
        self.conn.commit()

    def delete_package(self, tracking_number):
        self.cursor.execute("DELETE FROM packages WHERE tracking_number = ?", (tracking_number,))
        self.conn.commit()