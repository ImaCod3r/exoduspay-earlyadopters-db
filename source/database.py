import sqlitecloud
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

CONN_STR = os.getenv("CONNECTION_STRING")

if not CONN_STR or not CONN_STR.startswith("sqlitecloud://"):
    raise ValueError(
        "CONNECTION_STRING environment variable must be set to a sqlitecloud:// URL. "
        "Example: sqlitecloud://api-key@host:8860/dbname?apikey=your_api_key"
    )
\
try:
    conn = sqlitecloud.connect(CONN_STR)
except Exception as e:
    raise ConnectionError(f"Failed to connect to SQLite Cloud: {e}")
else:
    print(f"✓ Connected to SQLite Cloud.")

class Email:
    TABLE_NAME = "emails"
    
    def __init__(self, email: str, time: datetime = None):
        self.email = email
        self.time = time or datetime.now()
    
    @staticmethod
    def create_table():
        cursor = conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {Email.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                time DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        print(f"✓ Table '{Email.TABLE_NAME}' ready")
    
    @staticmethod
    def create(email: str):
        now = datetime.now().isoformat()

        conn.execute(
        f"INSERT INTO {Email.TABLE_NAME} (email, time) VALUES (?, ?)",
        (email, now)
    )
        conn.commit()

        created = conn.execute(
            f"SELECT email, time FROM {Email.TABLE_NAME} WHERE email = ?",
            (email,)
        ).fetchone()

        if created:
            email_obj = Email(created[0])
            email_obj.time = datetime.fromisoformat(created[1])
            return email_obj

        return None

    
    @staticmethod
    def select():
        cursor = conn.execute(f"SELECT email, time FROM {Email.TABLE_NAME} ORDER BY time DESC")
        rows = cursor.fetchall()
        
        emails = []
        for row in rows:
            email_obj = Email(row[0])
        
            if isinstance(row[1], str):
                email_obj.time = datetime.fromisoformat(row[1])
            else:
                email_obj.time = row[1]
            emails.append(email_obj)
        
        return emails
    
    @staticmethod
    def delete(email: str):
        cursor = conn.execute(
            f"DELETE FROM {Email.TABLE_NAME} WHERE email = ?",
            (email,)
        )
        conn.commit()
        return cursor.rowcount > 0
    
    @staticmethod
    def get_stats():
        cursor = conn.execute(f"SELECT email, time FROM {Email.TABLE_NAME}")
        rows = cursor.fetchall()
        
        by_day = {}
        by_hour = {}
        
        for row in rows:
            if isinstance(row[1], str):
                dt = datetime.fromisoformat(row[1])
            else:
                dt = row[1]
            
            day_str = dt.strftime("%Y-%m-%d")
            by_day[day_str] = by_day.get(day_str, 0) + 1
            
            hour_str = dt.strftime("%H")
            by_hour[hour_str] = by_hour.get(hour_str, 0) + 1
        
        by_day_list = sorted([{"date": k, "count": v} for k, v in by_day.items()])
        by_hour_list = [{"hour": f"{i:02d}", "count": by_hour.get(f"{i:02d}", 0)} for i in range(24)]
        
        return {
            "byDay": by_day_list,
            "byHour": by_hour_list,
            "total": len(rows)
        }
    
    @property
    def formatted_time(self):
        if isinstance(self.time, str):
            dt = datetime.fromisoformat(self.time)
        else:
            dt = self.time
        return dt.strftime("%d/%m/%Y %H:%M:%S")

# Initialize database
Email.create_table()