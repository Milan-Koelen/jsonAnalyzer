from flask import request


def flatten_json(json):
    # https://www.geeksforgeeks.org/flattening-json-objects-in-python/ */
    arrays = []
    nullValues = []
    name = ""
    out = {}

    def flatten(
        x,
        arrays: set,
        name,
    ):
        # If the Nested key-value
        # pair is of dict type
        if type(x) is dict:
            # CHECK FOR EMPTY DICTIONARY
            if len(x) == 0:
                nullValues.append(name[:-1])
            for a in x:
                flatten(x[a], arrays, name + a + ".")
        # If the Nested key-value
        # pair is of list type
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, arrays, name)
                i += 1
                if name[:-1] not in arrays:
                    arrays.append(name[:-1])
        else:
            out[name[:-1]] = x

    flatten(json, arrays, name)
    print("===---===---   ARRAYS  ===---===---===")
    for array in arrays:
        print(array)
    print("===---===---===---===---===---===---===\n")
    print("===---===---   FIELDS   ===---===---===")
    for item in out:
        print(item)
    print("===---===---===---===---===---===---===\n")
    print("===---===   NULL  VALUES  ---===---===")
    for field in nullValues:
        print(field)
    print("===---===---===---===---===---===---===\n")

    return {"out": out, "arrays": arrays, "nullValues": nullValues}


def mongoTransformation(json):
    unwind = []
    project = []
    flat_json = flatten_json(json)

    # UNWIND STAGE
    for array in flat_json["arrays"]:
        unwind.append(
            f'{{"$unwind": {{"path": "${array}", "preserveNullAndEmptyArrays": "True"}}}},'
        )

    # PROJECTION STAGE
    project.append(f'{{"$project":{{')

    for key in flat_json["out"]:

        collumn = key.replace(".", "_")

        data_type = type(flat_json["out"][key]).__name__
        if data_type == "str":
            null = '""'
        if data_type == "int":
            null = 0
        if data_type == "float":
            null = 0.0
        if data_type == "bool":
            null = "false"

        ifNull = f'{{"$ifNull": ["${key}", {null}]}}'

        if key not in flat_json["nullValues"]:

            project.append(f'"{collumn}": {ifNull},')

        # Cond statement for emtpy object null values
        else:
            project.append(
                f'"{collumn}": {{ "$cond": {{"$if": {{  "$eq": [ "{key}", "object"]}}, "then": "", "else": {ifNull}}}}},'
            )

    project.append(f"}}}}")

    return {"unwind": unwind, "project": project}

def fieldValues(json, field):
    values = []
    def getValues(json):
        if type(json) is dict:
            for key in json:
                if field in key:
                    if type(json[key]) is list:
                        for item in json[key]:
                            if item not in values:    
                                values.append(item)
                    else:
                        if json[key] not in values:
                            values.append(json[key])
                else:
                    getValues(json[key])
        elif type(json) is list:
            for item in json:
                getValues(item)    
                            
    getValues(json)
    # print("values", values)

    return {"fieldValues": values}