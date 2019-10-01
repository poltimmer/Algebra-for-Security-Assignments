def set_to_array(original_set):
    result = []
    split_set = original_set.split(',')
    for group in split_set:
        if '{' or '}' in group:
            group = group.strip('{}')

        if group is not '':
            result.append(int(group))

    return result


def sanitize_arrays(f, g):
    while len(f) > len(g):
        g.insert(0, 0)

    while len(g) > len(f):
        f.insert(0, 0)


# Converts a polynomial to a string representing that polynomial. Assumes positive coefficients.
def poly_string(x):
    result = ''

    for power, coefficient in enumerate(reversed(x)):
        if coefficient > 1:
            result = str(coefficient) + result
        elif coefficient == 1:
            if power > 0:
                pass
            else:
                result = str(coefficient) + result
        else:
            continue

        if power > 1:
            result = 'X^' + str(power) + '+' + result
        elif power == 1:
            result = 'X' + '+' + result
        else:
            result += '+'


    # If nothing gets added to result then we should just return 0
    if result == '':
        return '0'
    else:
        return result[:-1]  # Removes '+' at the end

