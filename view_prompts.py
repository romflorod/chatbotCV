import sqlite3

def view_prompts():
    conn = sqlite3.connect('prompts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM prompts')
    rows = cursor.fetchall()
    conn.close()
    
    for row in rows:
        print(f"ID: {row[0]}, Prompt: {row[1]}")

if __name__ == '__main__':
    view_prompts()