from utils import sanitize_arrays, set_to_array, poly_string, clear_leading_zeroes  # pylint: disable=no-name-in-module

INPUTFILE = "input.txt"
OUTPUTFILE = "output.txt"


def main():
    """
    Main routine controlling the main tasks of the program
    """
    # Read Input
    # For each block of calculations do
    # # Generate result
    # # Add result to object
    # # Return object
    # Parse output in right format
    # Print output to file
    objects = read_input()
    for obj in objects:
        obj = generate_answer(obj)
        print(obj)  # TODO: Remove before production

    print_output(objects)


def read_input():
    # Define return object
    objects = []

    # Check if input file exists in folder, else notify user and exit with error.
    try:
        input_file = open(INPUTFILE, 'r')
    except FileNotFoundError:
        print(
            "Input file {} not found in current directory. Make sure the file is in the same directory!"
                .format(INPUTFILE))
        exit(1)

    for line in input_file:
        obj = {}

        if line.startswith("[mod]"):
            a_original = None
            b_original = None
            f_original = None
            g_original = None
            h_original = None
            deg_original = None
            additional_data = None

            obj['mod'] = int(line.split()[1])
            obj['operation'] = input_file.readline()[1:-2]

            if '{' in obj['operation']:
                operation = obj['operation'].split()
                obj['operation'] = operation[0].strip(']')
                obj['operation_values'] = set_to_array(operation[1])

            # Parse rest
            for current_line in input_file:
                if current_line == '\n':  # If we find an empty line, the block is finished
                    break

                key = current_line.split()[0][1:-1]

                if key == 'a':
                    a_original = current_line[:-1]
                elif key == 'b':
                    b_original = current_line[:-1]
                elif key == 'f':
                    f_original = current_line[:-1]
                elif key == 'g':
                    g_original = current_line[:-1]
                elif key == 'h':
                    h_original = current_line[:-1]
                elif key == 'deg':
                    deg_original = current_line[:-1]
                elif '[' not in key and key != '':
                    additional_data = key

            if a_original:
                a = set_to_array(a_original.split()[1])
                obj['a_original'] = a_original
                obj['a'] = a

            if b_original:
                b = set_to_array(b_original.split()[1])
                obj['b_original'] = b_original
                obj['b'] = b

            if f_original:
                f = set_to_array(f_original.split()[1])
                obj['f_original'] = f_original
                obj['f'] = f

            if g_original:
                g = set_to_array(g_original.split()[1])
                obj['g_original'] = g_original
                obj['g'] = g

            if h_original:
                h = set_to_array(h_original.split()[1])
                obj['h_original'] = h_original
                obj['h'] = h

            if deg_original:
                obj['deg_original'] = deg_original
                obj['deg'] = int(deg_original.split()[1])

            if additional_data:
                obj['additional_data'] = additional_data

            objects.append(obj)
        else:
            continue

    return objects


def generate_answer(obj):
    op = obj.get('operation')

    if op == "display-poly":
        obj = display_poly(obj)
    elif op == "add-poly":
        obj = add_sub_poly(obj, 'add')
    elif op == "subtract-poly":
        obj = add_sub_poly(obj, 'sub')
    elif op == "multiply-poly":
        obj = mul_poly(obj)  # Janneke
    elif op == "long-div-poly":
        obj = div_poly(obj)  # Pol
    elif op == "euclid-poly":
        obj = euclid_poly(obj)  # Pol
    elif op == "equals-poly-mod":
        obj = equals_poly_mod(obj)  # Janneke
    elif op == "irreducible":
        obj = is_irreducible(obj)  # Edwin
    elif op == "find-irred":
        obj = find_irred(obj)  # Edwin
    elif op == "mod-poly":
        obj = mod_poly(obj)

    return obj


def print_output(objects):
    output_file = open(OUTPUTFILE, 'w')

    for obj in objects:
        output_file.write("[mod] {}\n".format(obj['mod']))
        output_file.write("[{}]\n".format(obj['operation']))
        if obj['operation'] == "mod-poly":
            output_file.write("[{}]\n".format(obj['additional_data']))

        if 'f_original' in obj:
            output_file.write(obj['f_original'] + '\n')
        if 'g_original' in obj:
            output_file.write(obj['g_original'] + '\n')
        if 'h_original' in obj:
            output_file.write(obj['h_original'] + '\n')
        if 'deg_original' in obj:
            output_file.write(obj['deg_original'] + '\n')
        if 'a_original' in obj:
            output_file.write(obj['a_original'] + '\n')
        if 'b_original' in obj:
            output_file.write(obj['b_original'] + '\n')
        if 'answer' in obj:
            output_file.write('[answer] {}\n'.format(obj['answer']))

        output_file.write('\n')

    output_file.close()


def display_poly(obj):
    # Get the values we need from the object
    f = obj.get('f')
    m = obj.get('mod')

    # Set local variables
    result = ''  # Final string that will be returned as answer
    index_string = 0  # Index of place in result

    # # For each number in reversed input
    # for index, i in enumerate(reversed(f)):
    #     # Calculate coefficient for each exponent. If 1 then ignore before X, but return when at the beginning of the
    #     # answer.
    #     if i % m == 1 and index == 0:
    #         coef = '1'
    #     elif i % m == 1:
    #         coef = ''
    #     else:
    #         coef = str(i % m)
    #
    #     # Coefficient is 0, ignore whole piece
    #     if i % m == 0:
    #         continue
    #
    #     # If at the beginning make sure to ignore '+' because this will mess up the answer
    #     if index_string == 0:
    #         index_string += 1
    #
    #         if index == 0:
    #             result = coef + result
    #         elif index == 1:
    #             result = coef + 'X' + result
    #         else:
    #             result = coef + 'X^' + str(index) + result
    #
    #     # Regular case
    #     else:
    #         index_string += 1
    #
    #         if index == 0:
    #             result = coef + '+' + result
    #         elif index == 1:
    #             result = coef + 'X' + '+' + result
    #         else:
    #             result = coef + 'X^' + str(index) + '+' + result
    #
    # # If nothing gets added to result then we should just return 0
    # if result == '':
    #     result = '0'

    result = poly_string(f)
    # Return Object
    obj['answer'] = result
    return obj


def add_sub_poly(obj, op='add'):
    # Get the values we need from the object
    f_orig = obj.get('f')
    f_new = f_orig.copy()
    g_orig = obj.get('g')
    g_new = g_orig.copy()
    m = obj.get('mod')

    # Make sure the lengths are equal by inserting at the front
    sanitize_arrays(f_new, g_new)

    # If operand is addition then add
    if op == 'add':
        result = add_poly(f_new, g_new, m)
    elif op == 'sub':
        result = subtract_poly(f_new, g_new, m)
    else:
        raise Exception('Invalid operator ', op)

    # Add result to obj
    obj['f'] = result
    obj['answer_original'] = result

    # Get the string copy of result by calling display_poly
    obj = display_poly(obj)

    # Return object to initial state
    obj['f'] = f_orig
    obj['g'] = g_orig

    # Return object which now includes an answer key-value pair
    return obj


def add_poly(a_remote, b_remote, m):
    a = a_remote.copy()
    b = b_remote.copy()

    sanitize_arrays(a, b)

    result = []
    # Add numbers with same index and modulo m them. Add to result
    for x, y in zip(a, b):
        result.append((x + y) % m)

    return result


def subtract_poly(a_remote, b_remote, m):
    a = a_remote.copy()
    b = b_remote.copy()

    sanitize_arrays(a, b)

    result = []
    # Subtract numbers with same index and modulo m them. Add to result
    for x, y in zip(a, b):
        result.append((x - y) % m)

    return result


def mul_poly(obj):
    f_orig = obj.get('f')
    f_new = f_orig.copy()
    g_new = obj.get('g')
    m = obj.get('mod')

    # Set local variable
    result = mult(f_new, g_new, m)

    # result.reverse()
    obj['f'] = result
    obj['answer_original'] = result

    # Get the string copy of result by calling display_poly
    obj = display_poly(obj)

    # Return object to initial state
    obj['f'] = f_orig

    # Return object which now includes an answer key-value pair
    return obj


def mult(a, b, m):
    result = [0] * (len(a) + len(b)-1)

    for i in range(0, len(a)):
        for j in range(0, len(b)):
            result[i + j] = result[i + j] + (a[i] * b[j])
            while result[i + j] < 0:  # TODO als meer dan een keer modulo erbij moet
                result[i + j] = result[i + j] + m
            result[i + j] = result[i + j] % m

    return result


def div_poly(obj):
    a = obj.get('f')
    b = obj.get('g')
    m = obj.get('m')

    answer_q, answer_r = long_div_poly(a, b, m)

    obj['answ-q'] = answer_q
    obj['answ-r'] = answer_r

    # Get the string copy of result by calling display_poly
    obj = display_poly(obj)  # TODO: doesn't work for these answers, due to no abstraction in display_poly

    return obj


def long_div_poly(a_remote, b_remote, m):
    a = a_remote.copy()
    b = b_remote.copy()

    # TODO: modular reduction of a and b

    q = [0]
    r = a
    while len(r) >= len(b):
        x = [mod_div(r[0], b[0], m)] + [0] * (len(r) - len(b))
        q = add_poly(q, x, m)
        w = mult(x, b, m)
        r = subtract_poly(r, w, m)
        r = clear_leading_zeroes(r)

    # TODO: modular reduction of q and r
    return q, r


# Modular division of integers a and b mod m
def mod_div(a, b, m):
    a = a % m
    b = b % m

    while a % b != 0:
        a += m

    return int((a / b) % m)


def euclid_poly(obj):
    a = obj.get('f')
    b = obj.get('g')
    m = obj.get('m')

    obj['answ-a'], obj['answ-b'] = euclid_extended_poly(a, b, m)

    # Get the string copy of result by calling display_poly
    obj = display_poly(obj)

    return obj


def euclid_extended_poly(a_remote, b_remote, m):
    a = a_remote.copy()
    b = b_remote.copy()

    # TODO: reduce polynomials

    x = 1,
    v = 1,
    y = 0,
    u = 0,
    while b != [0]:  # TODO: likely faulty comparison, as addresses get compared
        q, r = long_div_poly(a, b, m)
        a = b
        b = r
        x_ = x
        y_ = y
        x = u
        y = v
        u = subtract_poly(x_, mult(q, u, m), m)  # TODO: assumes proper abstraction
        v = subtract_poly(y_, mult(q, v, m), m)
    # TODO: need to figure out how to invert, and need helper function to calculate function
    return inv(x(a[0])), inv(y(a[0]))


def equals_poly_mod(obj):
    return obj


def is_irreducible(obj):
    return obj


def find_irred(obj):
    return obj


def mod_poly(obj):
    return obj


if __name__ == "__main__":
    main()
