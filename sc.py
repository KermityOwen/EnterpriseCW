import sqlite3
import requests
from flask import Flask, request, jsonify
import db


database = "database.sqlite"
app = Flask(__name__)
app.config["DEBUG"] = True

        
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
    
    if (db.check_exists(code) == 1):
        db.update_cell(id, value)
        return "",204 # Already exists
    
    if (value == "" or value == None):
        return "",400 # Content Missing
    
    if (code == "" or code == None):
        return "",400 # Content Missing
    
    db.create_cell(id, value)
    return "",201 # Created
    
    
    
@app.route("/cells/<string:s>", methods=["GET"])
def sc_read_cell_single(s):
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
        return {"formula" : str(calc_data), "id" : s}, 200


@app.route("/cells", methods=["GET"])
def list_cells():
    cells = db.get_cells()
    if cells == None:
        return "",204 # No Content
    else:
        return jsonify(cells), 200


@app.route("/cells/<string:s>", methods=["DELETE"])
def delete_cell(s):
    cell = s
    if (db.check_exists(cell) == 1):   
        db.delete_cell(cell)
        return "",204 # Cell Deleted
    return "", 404 # Cell not found

        
def main():
    db.setup_db()
    app.run(host="localhost",port=3000)

if __name__ == "__main__": 
    main ()