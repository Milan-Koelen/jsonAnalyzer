def flatten_json(y):
    # src */
    # https://www.geeksforgeeks.org/flattening-json-objects-in-python/ */

    out = {}

    def flatten(
        x,
        name="",
    ):
        # If the Nested key-value
        # pair is of dict type
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + ".")
        # If the Nested key-value
        # pair is of list type
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + ".")
                i += 1
        else:
            out[name[:-1]] = x

    flatten(
        y,
    )
    return {"out": out}
