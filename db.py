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


def check_valid_code(cell_code):
    return bool(re.match(r'^[A-Z]\d$', cell_code))

# def check_valid_value(cell_value):
#     formula = formula.replace(" ","")
#     pattern = re.compile(r'([-+*/()])')
#     tokens = re.split(pattern, formula)
#     tokens = list(filter(None, tokens))
    
    

        
def create_cell(cell_code, cell_value):
    with sqlite3.connect("database.sqlite") as connection:
        cursor = connection.cursor() 
        cursor.execute(
        "INSERT INTO cells(cell_code, cell_value) VALUES (?,?)",
        (cell_code, cell_value)
        )
        connection.commit()
        print(cursor.rowcount > 0)
        
        
def update_cell(cell_code, cell_value):
    with sqlite3.connect("database.sqlite") as connection:
        cursor = connection.cursor() 
        cursor.execute(
        "UPDATE cells SET cell_value=? WHERE cell_code=?",
        (cell_value, cell_code)
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
    print(formula)
    return eval(formula)


def parse_formula(formula):
    formula = formula.replace(" ","")
    pattern = re.compile(r'([-+*/()])')
    tokens = re.split(pattern, formula)
    tokens = list(filter(None, tokens))
    # print("pretoken" + str(tokens))

    counter = 0
    for token in tokens:
        if bool(re.match(r"^[\d.]+|[-+*/()]{1}$", token)): # regex magic
            # print("pass")
            pass
        else:
            with sqlite3.connect("database.sqlite") as connection:
                cursor = connection.cursor() 
                cursor.execute(
                "SELECT cell_code, cell_value FROM cells WHERE cell_code=?", (token,)
                )
                connection.commit()
                row = cursor.fetchone()
                # print("row" + str(row))
                subtoken = parse_formula(row[1])
                # print("subtoken" + str(subtoken))
                subtoken.insert(0,"(")
                subtoken.append(")")
                tokens[counter:counter + 1] = subtoken
        counter += 1
        
    # print("tokens" + str(tokens) + "\n")
    return tokens
    

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
        
# print(parse_formula("(3 + 4)"))