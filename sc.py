# Imports
from flask import Flask, request, jsonify
import optparse


# Conditional imports
p = optparse.OptionParser()
p.add_option('--r', '-r', default="firebase")
options, arguments = p.parse_args()

if (options.r == "sqlite"):
    print("sqlite")
    import db_sqlite as db
else:
    print("firebase")
    import db_firebase as db


# Initializing variables
app = Flask(__name__)
app.config["DEBUG"] = True


"""PUT Request Handler
Handles PUT requests by checking for request's content's validity
and inserts or updates to the database

Returns:
    201 - Creating Cell
    204 - Updating Exisiting Cell
    400 - Bad Request (Cell ID Mismatch)
          Bad Request (Missing Content)
          Bad Request (Invalid Content)
    500 - Internal Server Error
"""
@app.route("/cells/<string:s>", methods=["PUT"])
def sc_create_cell(s):
    try:
        id = s
        try:
            code = request.json["id"]
            value = request.json["formula"]
        except:
            return "", 400 # Bad Request, Code
        
        if (id != code):
            return "",400 # Bad Request, Cell ID Mismatch
        
        if (db.check_exists(id) == 1):
            db.update_cell(id, value)
            return "",204 # Already exists
        
        if (db.check_valid_code(id)):
            return "",400 # Code invalid
        
        db.create_cell(id, value)
        return "",201 # Created
    except:
        return "",500 # Internal Server Error
    
    
"""GET Request Handler (Single Cell)
Handles GET requests to specific cells by using their cell 
code, evaluates their value recursively and returns them.

Returns:
    200 - Returning Evaluated Cell
    404 - Invalid Cell Code (Cell Not Found)
    500 - Internal Server Error
"""
@app.route("/cells/<string:s>", methods=["GET"])
def sc_read_cell_single(s):
    try:
        cell_data = db.read_cell(s)
        
        if (cell_data == None or cell_data == ""):
            return "", 404 # Cell Not found
        
        try:
            float(cell_data)
            return {"formula" : str(cell_data), "id" : s},200 # Cell as float
        except:
            parsed_data = db.parse_formula(cell_data)
            calc_data = db.calculate_formula(parsed_data)
            print(cell_data)
            return {"formula" : str(calc_data), "id" : s}, 200 # Cell as float
    except:
        return "", 500 # Internal Server Error


"""GET Request Handler (All Cells)
Returns a list of all existing cells.

Returns:
    200 - Returns List of Cells
    500 - Internal Server Error
"""
@app.route("/cells", methods=["GET"])
def list_cells():
    # try:
    cells = db.get_cells()
    if cells == None:
        return "",204 # No Content
    else:
        return jsonify(cells), 200 # List of all cell
    # except Exception as e:
    #     print(e)
    #     return "", 500 # Internal Server Error


"""DELETE Request Handler
Handles DELETE requests to specific cells by using their cell
code to identify and delete specified cells from the database.

Returns:
    204 - Cell Deleted
    404 - Cell Not Found
    500 - Internal Server Error
"""
@app.route("/cells/<string:s>", methods=["DELETE"])
def delete_cell(s):
    try:
        cell = s
        if (db.check_exists(cell) == 1):   
            db.delete_cell(cell)
            return "",204 # Cell Deleted
        return "", 404 # Cell not found
    except:
        return "", 500 # Internal Server Error


"""Main Function
"""
def main():
    db.setup_db()
    app.run(host="localhost",port=3000)


if __name__ == "__main__": 
    main ()