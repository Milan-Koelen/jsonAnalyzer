def flatten_json(y):
    # src */
    # https://www.geeksforgeeks.org/flattening-json-objects-in-python/ */
    arrays = []
    nullValues = []
    name=""
    out = {}

    def flatten(
        x,
        arrays:set,
        name,
    ):
        # If the Nested key-value
        # pair is of dict type
        if type(x) is dict:
            # CHECK FOR EMPTY DICTIONARY
            if len(x) == 0:
                nullValues.append(name)
                print(f"EPMTY DICT: {name}")
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

    flatten(
        y,
        arrays,
        name
    )
    print("===---===--- ARRAYS ===---===---===")
    for array in arrays:
        print(array)
    print("===---===---===---===---===---===---===\n")
    return {"out": out,
            "arrays": arrays,
            "nullValues": nullValues}
    
    
def mongoTransformation(y):

    unwind = []

    for array in flatten_json(y)['arrays']:
        unwind.append(f'{{"$unwind": {{"path": "${array}", "preserveNullAndEmptyArrays": "True"}}}},')
        
    
    for item in unwind:
        print(item)



    return {"unwind": unwind}


def project(y):
    project = []
    project.append(f'{{"$project":')
    
    for key in y:

        # Replace all dots with underscores
        collumn = key.replace(".", "_")
        
        project.append(f'"{collumn}": {{ "$ifNull": [ "${key}", "" ] }},')
    
    
    
    # PROJECT ALL FIELDS WITH IFNULL AND COND FOR EPTY STATEMENTS
    
    
    project.append(f'}}')
    for item in project:
        print(item)

    return{"project": project}