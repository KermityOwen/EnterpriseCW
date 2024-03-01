from flask import Flask, request, jsonify
import db_sqlite

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
    id = s
    try:
        code = request.json["id"]
        value = request.json["formula"]
    except:
        return "", 400 # Bad Request, Code
    
    if (id != code):
        return "",400 # Bad Request, Cell ID Mismatch
    
    if (db_sqlite.check_exists(code) == 1):
        db_sqlite.update_cell(id, value)
        return "",204 # Already exists
    
    if (value == "" or value == None):
        return "",400 # Content Missing
    
    if (code == "" or code == None):
        return "",400 # Content Missing
    
    db_sqlite.create_cell(id, value)
    return "",201 # Created
    
    
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
    cell_data = db_sqlite.read_cell(s)
    
    if (cell_data == None or cell_data == ""):
        return "", 404 # Cell Not found
    
    try:
        float(cell_data)
        return {"formula" : str(cell_data), "id" : s},200 # Cell as float
    except:
        parsed_data = db_sqlite.parse_formula(cell_data)
        calc_data = db_sqlite.calculate_formula(parsed_data)
        print(cell_data)
        return {"formula" : str(calc_data), "id" : s}, 200


"""GET Request Handler (All Cells)
Returns a list of all existing cells.

Returns:
    200 - Returns List of Cells
    500 - Internal Server Error
"""
@app.route("/cells", methods=["GET"])
def list_cells():
    cells = db_sqlite.get_cells()
    if cells == None:
        return "",204 # No Content
    else:
        return jsonify(cells), 200


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
    cell = s
    if (db_sqlite.check_exists(cell) == 1):   
        db_sqlite.delete_cell(cell)
        return "",204 # Cell Deleted
    return "", 404 # Cell not found

        
def main():
    db_sqlite.setup_db()
    app.run(host="localhost",port=3000)


if __name__ == "__main__": 
    main ()