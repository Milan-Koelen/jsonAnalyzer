from flask import request


def flatten_json(json):
    # Function to flatten JSON objects
    arrays = []
    nullValues = []
    name = ""
    out = {}

    def flatten(x, arrays: set, name):
        if type(x) is dict:
            if len(x) == 0:
                nullValues.append(name[:-1])
            for a in x:
                flatten(x[a], arrays, name + a + ".")
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
        else:
            project.append(
                f'"{collumn}": {{ "$cond": {{"$if": {{"$eq": [ "{key}", "object"]}}, "then": "", "else": {ifNull}}}}},'
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

    return {"fieldValues": values}


def generate_typescript_declarations(json):
    flat_json = flatten_json(json)
    interfaces = []

    def generate_interface(name, properties):
        interface = f"export interface {name} {{\n"
        for prop in properties:
            interface += f"    {prop}\n"
        interface += "}"

        return interface

    def generate_nested_interfaces(name, obj):
        properties = []

        for key, value in obj.items():
            data_type = type(value).__name__

            if data_type == "dict":
                nested_interface_name = f"{name}_{key}"
                properties.append(f"{key}: {nested_interface_name};")
                nested_interface = generate_interface(nested_interface_name, [])
                interfaces.append(nested_interface)
                generate_nested_interfaces(nested_interface_name, value)
            elif data_type == "list":
                if len(value) > 0:
                    list_item_type = type(value[0]).__name__
                    if list_item_type == "dict":
                        nested_interface_name = f"{name}_{key}_Item"
                        properties.append(f"{key}: {nested_interface_name}[];")
                        nested_interface = generate_interface(nested_interface_name, [])
                        interfaces.append(nested_interface)
                        generate_nested_interfaces(nested_interface_name, value[0])
                    else:
                        properties.append(f"{key}: {list_item_type}[];")
                else:
                    properties.append(f"{key}: any[];")
            else:
                properties.append(f"{key}: {data_type};")

        interface = generate_interface(name, properties)
        interfaces.append(interface)

    generate_nested_interfaces("Root", flat_json["out"])

    return "\n\n".join(interfaces)
