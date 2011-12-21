


def camel_case(input_string):
    return "".join([word.capitalize() for word in input_string.split('_')])


def lower_camel_case(input_string):
    first = True
    result = ""
    for word in input_string.split('_'):
        if first:
            first = False
            result += word.lower()
        else:
            result += word.capitalize()
    return result
            
            
def pluralize(input_string):
    if input_string[-1] != 's':
        input_string += 's'
    return input_string


