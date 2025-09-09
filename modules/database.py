import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_content TEXT NOT NULL,
            reminder_time DATETIME NOT NULL,
            location TEXT,
            weather_info TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_task_to_db(task_content, reminder_time, location, weather_info):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO tasks (task_content, reminder_time, location, weather_info)
        VALUES (?, ?, ?, ?)
    ''', (task_content, reminder_time, location, weather_info))
    conn.commit()
    conn.close()

def get_all_tasks():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''
        SELECT task_content, reminder_time, location, weather_info 
        FROM tasks 
        ORDER BY reminder_time DESC
    ''')
    
    tasks = []
    for row in c.fetchall():
        task_content, reminder_time, location, weather_info = row
        # 格式化时间
        if isinstance(reminder_time, str):
            try:
                reminder_time = datetime.fromisoformat(reminder_time)
                formatted_time = reminder_time.strftime('%Y-%m-%d %H:%M')
            except ValueError:
                formatted_time = reminder_time
        else:
            formatted_time = reminder_time.strftime('%Y-%m-%d %H:%M')
        
        tasks.append({
            'task_content': task_content,
            'time': formatted_time,
            'location': location or '无地点信息',
            'weather_info': weather_info
        })
    
    conn.close()
    return tasks