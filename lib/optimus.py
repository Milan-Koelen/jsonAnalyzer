def flatten_json(y):
    # src */
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

    flatten(y, arrays, name)
    print("===---===--- ARRAYS ===---===---===")
    for array in arrays:
        print(array)
    print("===---===---===---===---===---===---===\n")

    print("===---===   NULL  VALUES  ---===---===")
    for field in nullValues:
        print(field)
    print("===---===---===---===---===---===---===\n")
    return {"out": out, "arrays": arrays, "nullValues": nullValues}


def mongoTransformation(y):

    unwind = []
    project = []

    flat_json = flatten_json(y)

    # UNWIND STAGE
    for array in flat_json["arrays"]:
        unwind.append(
            f'{{"$unwind": {{"path": "${array}", "preserveNullAndEmptyArrays": "True"}}}},'
        )

    # PRINT UNWIND STAGE
    for item in unwind:
        print(item)

    # PROJECTION STAGE
    project.append(f'{{"$project":{{')

    for key in flat_json["out"]:
        # Replace all dots with underscores
        collumn = key.replace(".", "_")

        if key in flat_json["nullValues"]:
            # Empty object possible
            project.append(
                f'"{collumn}": {{ "$cond": {{"$if": {{"{key}", "object",""}}, {{ "$ifNull": [ "${key}", "" ] }}}}}},'
            )
        #  { $cond: { if: <boolean-expression>, then: <true-case>, else: <false-case> } }

        project.append(f'"{collumn}": {{ "$ifNull": [ "${key}", "" ] }},')

    project.append(f"}}}}")

    # PRINT PROJECTION STAGE
    for item in project:
        print(item)

    return {"unwind": unwind, "project": project}
