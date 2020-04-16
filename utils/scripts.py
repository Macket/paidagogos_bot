import ast


def get_call_data(call):
    return ast.literal_eval(call.data.split('/')[1])
