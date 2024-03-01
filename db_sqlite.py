import sqlite3
import re

# Intialising variables
database = "database.sqlite"


"""Sets Up SQLite3 Database
"""
def setup_db():
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        cursor.execute(
        "CREATE TABLE IF NOT EXISTS cells" +
        "(cell_code TEXT PRIMARY KEY, cell_value TEXT)"
        )
        connection.commit()
        

"""Checks If Cell Already Exists

Argument:
    Cell Code
    
Returns:
    Boolean - If Cell Already Exists
"""
def check_exists(cell_code):
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor() 
        cursor.execute(
        "SELECT EXISTS(SELECT cell_code FROM cells WHERE cell_code=?)", (cell_code,)
        )
        connection.commit()
        row = cursor.fetchone()
        return row[0]


"""Checks If Cell Code is Valid

Argument:
    Cell Code
    
Returns:
    Boolean - If Cell Code is Valid
"""
def check_valid_code(cell_code: str):
    if not bool(re.match(r"[A-Z]",cell_code[0])):
        return False
    number = cell_code[1:]
    try:
        int(number)
        if (number > 999) or (number < 1):
            return False
        return True
    except:
        return False
        
        
"""Creates Cell

Argument:
    Cell Code, Cell Value
"""
def create_cell(cell_code, cell_value):
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor() 
        cursor.execute(
        "INSERT INTO cells(cell_code, cell_value) VALUES (?,?)",
        (cell_code, cell_value)
        )
        connection.commit()
        print(cursor.rowcount > 0)
        
        
"""Updates Cell

Argument:
    Cell Code, Cell Value
"""
def update_cell(cell_code, cell_value):
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor() 
        cursor.execute(
        "UPDATE cells SET cell_value=? WHERE cell_code=?",
        (cell_value, cell_code)
        )
        connection.commit()
        print(cursor.rowcount > 0)


"""Reads Simple Cells

Argument:
    Cell Code

Returns:
    Float - Cell Value
"""
def read_cell(cell_code):
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor() 
        cursor.execute(
        "SELECT cell_code, cell_value FROM cells WHERE cell_code=?", (cell_code,)
        )
        connection.commit()
        row = cursor.fetchone()
        return row[1] # Value part
    

"""Evaluates Value from a Formula

Argument:
    string[] - Array of tokens representing a formula
    
Return:
    float - Evaluated result
"""
def calculate_formula(tokens):
    formula = "".join(tokens)
    print(formula)
    return eval(formula)


"""Parses Formula into Token
Gets a string and recursively parses the formula into an
array of tokens that represent an equation. Resolves all
cell links (codes) recursively

Argument:
    string - Representing formula

Return:
    string[] - Representing processed formula as an
               array of tokens.
"""
def parse_formula(formula):
    try:
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
                with sqlite3.connect(database) as connection:
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
    except:
        return ["0"]
    

"""Get List of Cells

Returns:
    string[] - Array containing cell codes of all
               existing cells
"""
def get_cells():
    with sqlite3.connect(database) as connection:
        connection.row_factory = lambda cursor, row: row[0]
        cursor = connection.cursor() 
        cursor.execute(
        "SELECT * FROM cells"
        )
        connection.commit()
        cells = cursor.fetchall()
        print(cells)
        return cells
    
    
"""Deletes Cell

Argument:
    Cell code
"""
def delete_cell(cell_code):
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor() 
        cursor.execute(
        "DELETE FROM cells WHERE cell_code=?", (cell_code,)
        )
        connection.commit()
