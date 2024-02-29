import sqlite3
import re

database = "database.sqlite"

def setup_db():
    with sqlite3.connect("database.sqlite") as connection:
        cursor = connection.cursor()
        cursor.execute(
        "CREATE TABLE IF NOT EXISTS cells" +
        "(cell_code TEXT PRIMARY KEY, cell_value TEXT)"
        ) 
        connection.commit()
        

def check_exists(cell_code):
    with sqlite3.connect("database.sqlite") as connection:
        cursor = connection.cursor() 
        cursor.execute(
        "SELECT EXISTS(SELECT cell_code FROM cells WHERE cell_code=?)", (cell_code,)
        )
        connection.commit()
        row = cursor.fetchone()
        return row[0]

        
def create_cell(cell_code, cell_value):
    with sqlite3.connect("database.sqlite") as connection:
        cursor = connection.cursor() 
        cursor.execute(
        "INSERT INTO cells(cell_code, cell_value) VALUES (?,?)",
        (cell_code, cell_value)
        )
        connection.commit()
        print(cursor.rowcount > 0)
        

def read_cell(cell_code):
    with sqlite3.connect("database.sqlite") as connection:
        cursor = connection.cursor() 
        cursor.execute(
        "SELECT cell_code, cell_value FROM cells WHERE cell_code=?", (cell_code,)
        )
        connection.commit()
        row = cursor.fetchone()
        return row[1] # Value part
    

def calculate_formula(tokens):
    formula = "".join(tokens)
    return eval(formula)


def calculate_cell(formula):
    formula = formula.replace(" ","")
    pattern = re.compile(r'([-+*/()])')
    tokens = re.split(pattern, formula)
    tokens = list(filter(None, tokens))
    
    # print(tokens)

    for i in range(0, len(tokens)):
        if re.match(r'^[+\-*/()]+$', tokens[i]):
            print("pass")
            pass
        else:
            with sqlite3.connect("database.sqlite") as connection:
                cursor = connection.cursor() 
                cursor.execute(
                "SELECT cell_code, cell_value FROM cells WHERE cell_code=?", (tokens[i],)
                )
                connection.commit()
                row = cursor.fetchone()
                # print(row[1])
                tokens[i] = row[1]
            
    # print(tokens)
    return calculate_formula(tokens)
    

def get_cells():
    with sqlite3.connect("database.sqlite") as connection:
        connection.row_factory = lambda cursor, row: row[0]
        cursor = connection.cursor() 
        cursor.execute(
        "SELECT * FROM cells"
        )
        connection.commit()
        cells = cursor.fetchall()
        print(cells)
        return cells
    
    
def delete_cell(cell_code):
    with sqlite3.connect("database.sqlite") as connection:
        cursor = connection.cursor() 
        cursor.execute(
        "DELETE FROM cells WHERE cell_code=?", (cell_code,)
        )
        connection.commit()
        