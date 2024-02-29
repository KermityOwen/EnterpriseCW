import sqlite3
import requests
from flask import Flask, request, jsonify
import db


database = "database.sqlite"
app = Flask(__name__)
app.config["DEBUG"] = True
        

# @app.route("/", methods=["GET"])
# def up_running():
#     return "", 200
        
@app.route("/cells/<string:s>", methods=["PUT"])
def sc_create_cell(s):
    id = s
    code = request.json["id"]
    value = request.json["formula"]
    
    if (id != code):
        return "URL and Content ID mismatch",400 #,{"Bad Request, Cell ID Mismatch"} # Bad Request
    
    if (db.check_exists(code) == 1):
        return "Cell already exists",400 # Already exists
    
    if (value == "" or value == None):
        return "No / Missing Content",400
    
    if (code == "" or code == None):
        return "No / Missing Content",400
    
    db.create_cell(id, value)
    return f"Created Cell - {id} with Value - {value}",201 # Created
    
    
    
@app.route("/cells/<string:s>", methods=["GET"])
def sc_read_cell_single(s):
    cell_data = db.read_cell(s)
    
    if cell_data == None:
        return "",204,{"No Content"} # No Content
    
    # print(cell_data)
    try:
        float(cell_data)
        return {"formula" : cell_data, "id" : s},200 
    except:
        # print(cell_data)
        calc_data = db.calculate_cell(cell_data)
        return {"formula" : calc_data, "id" : s}, 200


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
    return "Cell Not Found", 404

        
def main():
    db.setup_db()
    app.run(host="localhost",port=3000)

if __name__ == "__main__": 
    main ()