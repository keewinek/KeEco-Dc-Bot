from sqlite3worker import Sqlite3Worker

c = None

def start_db():
    global c

    c = Sqlite3Worker("database.db")

    create_values_table()

def create_values_table():
    try: #check if table exists
        c.execute("""CREATE TABLE vals (vid TEXT, value TEXT)""")
        print("> Created vals table.")
    except:
        print("Vals table exists.")

def get_value(vid, starting_value=""):
    starting_value = str(starting_value)

    for row in c.execute(f'SELECT * FROM vals WHERE vid = ?', (vid,)):
        if vid == row[0]:
            return row[1]

    c.execute(f'INSERT INTO vals VALUES (?, ?)', (vid, starting_value))
    return starting_value

def set_value(vid, value):
    value = str(value)

    for row in c.execute(f'SELECT * FROM vals WHERE vid = ?', (vid,)):
        if vid == row[0]:
            c.execute(f'UPDATE vals SET value = ? WHERE vid = ?', (value, vid))
            return value

    c.execute(f'INSERT INTO vals VALUES (?, ?)', (vid, value))
    return value

start_db()