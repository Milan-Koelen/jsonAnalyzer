def flatten_json(y):
    # src */
    # https://www.geeksforgeeks.org/flattening-json-objects-in-python/ */
    arrays = []
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
                # print(name)
            # print(x)

            
            print("++")
                
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
            "arrays": arrays}
    
    
def mongoTransformation(y):

    unwind = []
    unwind.append("[")

    for array in flatten_json(y)['arrays']:
        unwind.append(f'{{"$unwind": {{"path": "${array}", "preserveNullAndEmptyArrays": "True"}}}},')
        
    unwind.append("]")
    
    for item in unwind:
        print(item)


    return {"unwind": unwind}

