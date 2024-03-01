import requests
import re
import json

database_url = "https://ecm3408-b5bf7-default-rtdb.europe-west1.firebasedatabase.app"

def setup_db():
    return

def check_exists(cell_code):
    url = f"{database_url}/cells/{str(cell_code)}.json"
    r = requests.get(url)
    if r.text == "null":
        return False
    return True

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
    
    
def create_cell(cell_code, cell_value):
    url = f"{database_url}/cells/{str(cell_code)}.json"
    payload = f'"{str(cell_value)}"'
    r = requests.put(url, data=payload)
    print(r.content)
    
    
def update_cell(cell_code, cell_value):
    create_cell(cell_code, cell_value)


def read_cell(cell_code):
    url = f"{database_url}/cells/{str(cell_code)}.json"
    r = requests.get(url)
    # print(r.text)
    result = r.text.replace('"', "")
    return result


def calculate_formula(tokens):
    formula = "".join(tokens)
    print(formula)
    return eval(formula)


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
                result = read_cell(token)
                # print("row" + result)
                subtoken = parse_formula(result)
                # print("subtoken" + str(subtoken))
                subtoken.insert(0,"(")
                subtoken.append(")")
                tokens[counter:counter + 1] = subtoken
            counter += 1
            
        # print("tokens" + str(tokens) + "\n")
        return tokens
    except:
        return ["0"]
    

def get_cells():
    url = f"{database_url}/cells.json"
    r = requests.get(url)
    ret_cells = json.loads(r.text)
    try:
        return list(ret_cells.keys())
    except:
        return []


def delete_cell(cell_code):
    url = f"{database_url}/cells/{str(cell_code)}.json"
    r = requests.delete(url)
    print(r)
    # result = r.text.replace('"', "")
    # return result
