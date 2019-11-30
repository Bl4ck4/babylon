from graphql_relay.node.node import from_global_id


def input_to_dictionary(input):
    dictionary = {}
    for key in input:
        if key[-2:] == "id":
            if isinstance(input[key], list):
                input[key] = [from_global_id(key)[1] for key in input[key]]
            else:
                input[key] = from_global_id(input[key])[1]
        dictionary[key] = input[key]
    return dictionary
