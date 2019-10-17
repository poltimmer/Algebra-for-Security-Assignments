from utils import sanitize_arrays, set_to_array, poly_string, clear_leading_zeroes, \
    reduce_poly, find_prime_factors, find_all_elements_field  # pylint: disable=no-name-in-module

import random

INPUTFILE = "input.txt"
OUTPUTFILE = "output.txt"


def main():
    """
    Main routine controlling the main flow of the program.
    """
    # Read input from file, returns all objects
    objects = read_input()
    for obj in objects:
        try:
            # Generate the objects answer, yields new object
            obj = generate_answer(obj)
        except Exception:
            # If an error might occur that is not covered, catch it here! Continue where left off
            print('ERROR: An unrecoverable error occured during the processing of ' + obj.get('operation') + '. Continuing...')
            obj['answer'] = 'ERROR'

        print(obj)  # TODO: Remove before production
    # Generate an output file
    print_output(objects)


def read_input():
    """
    Converts an input file (in a predefined layout) to objects usable by the program.
    """
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

    # Start generating the object with values from the input file
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
                obj['operation_values_original'] = operation[1] + '}'
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
                elif '[' not in key and key != '' and key != 'answer':
                    additional_data = key
            
            # Convert given values to arrays, keeping the old values
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
    """
    Call the correct function according to the operation required and complete the computation.
    """
    # Initialize variables
    answer = None
    answer_table = None
    answer_q = None
    answer_r = None
    answer_a = None
    answer_b = None
    answer_d = None

    # Get object values
    op = obj.get('operation')
    m = obj.get('mod')
    f = obj.get('f')
    g = obj.get('g')
    h = obj.get('h')
    a = obj.get('a')
    b = obj.get('b')
    deg = obj.get('deg')
    additional_data = obj.get('additional_data')
    poly_mod = obj.get('operation_values')

    # Operation switch
    if op == "display-poly":
        answer = f # Luke
    elif op == "add-poly":
        answer = add_poly(f, g, m) # Luke
    elif op == "subtract-poly":
        answer = subtract_poly(f, g, m) # Luke
    elif op == "multiply-poly":
        answer = mult(f, g, m)  # Janneke
    elif op == "long-div-poly":
        answer_q, answer_r = long_div_poly(f, g, m)  # Pol
    elif op == "euclid-poly":
        answer_a, answer_b, answer_d = euclid_extended_poly(f, g, m)  # Pol
    elif op == "equals-poly-mod":
        answer = equals_poly_mod(f, g, h, m)  # Janneke
    elif op == "irreducible":
        answer = is_irreducible(f, m)  # Edwin
    elif op == "find-irred":
        answer = find_irred(deg, m)  # Edwin
    elif op == "mod-poly":
        if additional_data == 'add-table':  # Edwin
            answer_table = add_table_field(m, poly_mod)
        elif additional_data == 'mult-table':  # Edwin
            answer_table = multiply_table_field(m, poly_mod)
        elif additional_data == 'display-field':  # Luke
            answer = display_field(a, m, poly_mod)
        elif additional_data == 'add-field':  # Janneke
            answer = add_field(poly_mod, m, a, b)
        elif additional_data == 'subtract-field':  # Janneke
            answer = subtract_field(poly_mod, m, a, b)
        elif additional_data == 'multiply-field':  # Janneke
            answer = multiply_field(poly_mod, m, a, b)
        elif additional_data == 'inverse-field':  # Luke
            answer = inverse_field(a, m, poly_mod)
        elif additional_data == 'division-field':  # Pol
            answer = [1]
        elif additional_data == 'equals-field':  # Luke
            answer = equals_field(a, b, m, poly_mod)
        elif additional_data == 'primitive':  # Pol# Different Answer
            answer = is_primitive(a, m, poly_mod)
        elif additional_data == 'find-prim':  # Pol
            answer = find_primitive(m, poly_mod)
        else:
            answer = 'Operation not Supported.'
    else:
        answer = 'Operation not Supported.'

    # Parse result to a valid polynomial
    if answer:
        obj['answer'] = display_poly(answer, m)
    if answer_table:
        obj['answer'] = display_table(answer_table, m)
    if answer_q:
        obj['answer-q'] = display_poly(answer_q, m)
    if answer_r:
        obj['answer-r'] = display_poly(answer_r, m)
    if answer_a:
        obj['answer-a'] = display_poly(answer_a, m)
    if answer_b:
        obj['answer-b'] = display_poly(answer_b, m)
    if answer_d:
        obj['answer-d'] = display_poly(answer_d, m)

    return obj


def print_output(objects):
    """
    Print the initial values + answer to an output file.
    """
    output_file = open(OUTPUTFILE, 'w')

    for obj in objects:
        output_file.write("[mod] {}\n".format(obj['mod']))
        
        # If mod_poly then also output the polynomial behind it
        if obj['operation'] == "mod-poly":            
            output_file.write("[{}]\t{}\n".format(obj['operation'], obj['operation_values_original']))
            output_file.write("[{}]\n".format(obj['additional_data']))
        else:
            output_file.write("[{}]\n".format(obj['operation']))

        # Print all values that are present    
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
        if 'answer-q' in obj:
            output_file.write('[answer-q] {}\n'.format(obj['answer-q']))
        if 'answer-r' in obj:
            output_file.write('[answer-r] {}\n'.format(obj['answer-r']))
        if 'answer-a' in obj:
            output_file.write('[answer-a] {}\n'.format(obj['answer-a']))
        if 'answer-b' in obj:
            output_file.write('[answer-b] {}\n'.format(obj['answer-b']))
        if 'answer-d' in obj:
            output_file.write('[answer-d] {}\n'.format(obj['answer-d']))

        output_file.write('\n')

    # Let the user know it has been generated
    print('Output has been saved to ' + OUTPUTFILE + '.')
    output_file.close()


def display_poly(f_remote, m):
    """
    Convert an Array f_remote to a Polynomial string.
    """
    # If it is a string return the given value
    if isinstance(f_remote, str):
        return f_remote

    # Get the values we need from the object
    f = f_remote.copy()

    # Reduce the polynomial
    f = reduce_poly(f, m)

    return poly_string(f)


def add_poly(a_remote, b_remote, m):
    """
    Add two polynomials together.
    """
    # Copy the two arrays
    a = a_remote.copy()
    b = b_remote.copy()

    # Make the length the same
    sanitize_arrays(a, b)

    result = []
    # Add numbers with same index and modulo m them. Add to result
    for x, y in zip(a, b):
        result.append((x + y) % m)

    return clear_leading_zeroes(result)


def subtract_poly(a_remote, b_remote, m):
    """
    Subtract two polynomials together.
    """
    # Copy the two arrays
    a = a_remote.copy()
    b = b_remote.copy()

    # Make the length the same
    sanitize_arrays(a, b)

    result = []
    # Subtract numbers with same index and modulo m them. Add to result
    for x, y in zip(a, b):
        result.append((x - y) % m)

    return clear_leading_zeroes(result)


def mult(a, b, m):
    result = [0] * (len(a) + len(b) - 1)

    for i in range(0, len(a)):
        for j in range(0, len(b)):
            result[i + j] = result[i + j] + (a[i] * b[j])
            while result[i + j] < 0:
                result[i + j] = result[i + j] + m
            result[i + j] = result[i + j] % m

    return clear_leading_zeroes(result)


def long_div_poly(a_remote, b_remote, m):
    a = a_remote.copy()
    b = b_remote.copy()

    a = reduce_poly(a, m)
    b = reduce_poly(b, m)

    if b_remote == [0]:
        return 'ERROR', 'ERROR'

    q = [0]
    r = a
    while len(r) >= len(b) and r != [0]:
        try:
            div = mod_div(r[0], b[0], m)
        except:
            return 'ERROR', 'ERROR'
        x = [div] + [0] * (len(r) - len(b))
        q = add_poly(q, x, m)
        w = mult(x, b, m)
        r = subtract_poly(r, w, m)
        r = clear_leading_zeroes(r)

    # Reducing result as sanity-check
    q = reduce_poly(q, m)
    r = reduce_poly(r, m)

    return q, r


# Modular division of integers a and b mod m
def mod_div(a, b, m):
    a = a % m
    b = b % m
    i = 0

    while a % b != 0:
        a += m
        i += 1
        if i > b:
            raise Exception

    return int((a / b) % m)


def euclid_extended_poly(a_remote, b_remote, m):
    a = reduce_poly(a_remote, m)
    b = reduce_poly(b_remote, m)

    x = [1]
    v = [1]
    y = [0]
    u = [0]
    while b != [0]:
        q, r = long_div_poly(a, b, m)
        if q and r == 'ERROR':
            return 'ERROR', 'ERROR', 'ERROR'
        a = b
        b = r
        x_ = x
        y_ = y
        x = u
        y = v
        u = subtract_poly(x_, mult(q, u, m), m)
        v = subtract_poly(y_, mult(q, v, m), m)
    x_out, _ = long_div_poly(x, [a[0]], m)
    y_out, _ = long_div_poly(y, [a[0]], m)

    if x_out == 'ERROR' or y_out == 'ERROR':
        return 'ERROR', 'ERROR', 'ERROR'

    gcd = add_poly(mult(a_remote, x_out, m), mult(b_remote, y_out, m), m)
    return x_out, y_out, gcd


def equals_poly_mod(f_remote, g_remote, h_remote, m):
    a = f_remote.copy()
    b = g_remote.copy()
    c = h_remote.copy()

    _, answer_a = long_div_poly(a, c, m)
    _, answer_b = long_div_poly(b, c, m)

    if answer_a == 'ERROR' or answer_b == 'ERROR':
        return 'FALSE'

    answer_a = answer_a[0] % m
    answer_b = answer_b[0] % m

    if answer_a == answer_b:
        return 'TRUE'
    else:
        return 'FALSE'


def is_irreducible(a_remote, m):
    t = 1
    n = len(a_remote) - 1

    if n <= 1:
        return 'DEGREE OF F IS TOO SMALL'

    b = [0] * ((m ** t) + 1)
    b[0] = 1
    b[-2] = -1
    _, _, euclid = euclid_extended_poly(a_remote, b, m)

    if euclid == 'ERROR':
        return 'ERROR'

    while euclid == [1]:
        t = t + 1
        b = [0] * ((m ** t) + 1)
        b[0] = 1
        b[-2] = -1
        _, _, euclid = euclid_extended_poly(a_remote, b, m)
        if euclid == 'ERROR':
            return 'ERROR'

    if t == n:
        return 'TRUE'
    else:
        return 'FALSE'


def find_irred(d, m):
    l = d + 1
    result = []
    for _ in range(l):
        result.append(random.randrange(0, m))
    result[0] = random.randrange(1, m)

    while is_irreducible(result, m) == 'FALSE':
        result = []
        for _ in range(l):
            result.append(random.randrange(0, m))
        result[0] = random.randrange(1, m)

    return clear_leading_zeroes(result)

### FIELD SECTION
def display_field(a_remote, m, poly_mod):
    """
    Display the field a_remote given two modulos
    """
    _, r = long_div_poly(a_remote, poly_mod, m)
    return r

def display_table(a, m):
    """
    Get a 3D array of polynomials, convert them to a string
    """
    # Initialize string
    result = ''
    result += '{'

    # Add all polynomials to the string, given they are already a string
    for i in a:
        for j in i[:-1]:
            result += display_poly(j, m)
            result += ', '

        # Add the last one here to prevent unneeded comma
        result += display_poly(i[-1], m)
        result += '; '

    # Remove final semicolon and close the brace
    result = result[:-2]
    result += '}'

    return result

def inverse_field(a_remote, m, poly_mod):
    """
    Calculates the inverse of a field, ERROR if it does not exist
    """
    x, _, gcd = euclid_extended_poly(a_remote, poly_mod, m)
    if gcd == [1]:
        return x
    return 'ERROR'


def add_table_field(m, poly_mod):
    x = find_all_elements_field(m, poly_mod)
    f = [[[] for a in range(len(x))] for b in range(len(x))]
    for i in range(len(x)):
        for j in range(len(x)):
            f[i][j] = add_field(poly_mod, m, x[i], x[j])
    return f


def multiply_table_field(m, poly_mod):
    x = find_all_elements_field(m, poly_mod)
    f = [[[] for a in range(len(x))] for b in range(len(x))]
    for i in range(len(x)):
        for j in range(len(x)):
            f[i][j] = multiply_field(poly_mod, m, x[i], x[j])
    return f


def equals_field(a_remote, b_remote, m, poly_mod):
    """
    Check if two fields are equal given polynomial modulo
    """
    return equals_poly_mod(a_remote, b_remote, poly_mod, m)


def add_field(poly_mod, m, a, b):
    a_and_b = add_poly(a, b, m)
    _, answer = long_div_poly(a_and_b, poly_mod, m)
    if answer == 'ERROR':
        return a_and_b
    else:
        return answer


def subtract_field(poly_mod, m, a, b):
    a_and_b = subtract_poly(a, b, m)
    _, answer = long_div_poly(a_and_b, poly_mod, m)
    if answer == 'ERROR':
        return a_and_b
    else:
        return answer


def multiply_field(poly_mod, m, a, b):
    a_and_b = mult(a, b, m)
    _, answer = long_div_poly(a_and_b, poly_mod, m)
    if answer == 'ERROR':
        return a_and_b
    else:
        return answer


def is_primitive(a, m, mod_poly):
    mod_poly_clean = clear_leading_zeroes(mod_poly)
    _, x = long_div_poly(a, mod_poly, m)
    if x == 'ERROR':
        return 'ERROR'
    x = clear_leading_zeroes(x)
    if x == [0]:
        return 'FALSE'

    q = m ** (len(mod_poly_clean) - 1)
    factors = find_prime_factors(q - 1)
    i = 1
    for factor in reversed(factors):
        while i * 2 <= (q - 1) / factor:
            x = multiply_field(mod_poly, m, x, x)
            i = i * 2
        while i < (q - 1) / factor:
            x = multiply_field(mod_poly, m, x, a)
            i += 1
        if x == [1]:
            return 'FALSE'

    return 'TRUE'


def find_primitive(m, mod_poly):
    elements = find_all_elements_field(m, mod_poly)

    for element in elements:
        if is_primitive(element, m, mod_poly) == 'TRUE':
            return element

    return 'ERROR'


if __name__ == "__main__":
    main()
