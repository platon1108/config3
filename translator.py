import yaml
import sys

def add_list(name, values, IDs):
    output = []
    for elem in values:
        if type(elem) == int:
            output.append(f"{elem}")
        if type(elem) == str:
            if elem in IDs:
                output.append(f"{elem}")
            else:
                output.append(f"'{elem}'")
        if type(elem) == dict:
            for key in elem.keys():
                output.append(add_list(key, elem[key], IDs))
    return '(' + ', '.join(output) + ')'
            

inputpath, outputpath = sys.argv[1:3]
with open(inputpath) as stream:
    try:
        inputdata = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
IDs = []
output = []
for key in inputdata.keys():
    elem = inputdata[key]
    if type(elem) == dict:
        output.append('{' + f'?{elem["operator"]} {elem["operand1"]} {elem["operand2"]}' + '}')
    elif type(elem) == str:
        if elem in IDs:
            output.append(f"def {key} = {elem}")
        else:
            output.append(f"def {key} = '{elem}'")
        IDs.append(key)
    elif type(elem) == int:
        output.append(f"def {key} = {elem}")
        IDs.append(key)
    elif type(elem) == list:
        output.append(add_list(key, elem, IDs))
with open(outputpath, 'w') as file:
    for line in output:
        print(line, file=file)                                   
