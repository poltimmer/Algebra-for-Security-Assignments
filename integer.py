from math import ceil, floor
from time import sleep

from utils import (array_to_number, invert, is_equal, is_greater_than,
                   is_negative, number_to_array)

INPUTFILE = "example.txt"
OUTPUTFILE = "output.txt"

OPERATION_COUNT = 0


def main():
    global OPERATION_COUNT
    objects = parse_input()
    for obj in objects:
        OPERATION_COUNT = 0
        attach_answer(obj)
        print_output(obj)


def parse_input():
    result = []

    try:
        input_file = open(INPUTFILE, "r")
    except:
        print(
            "Input file {} not found in current directory. Make sure the file is in the same directory!"
            .format(INPUTFILE))
        return

    for line in input_file:
        obj = {}
        # we only accept blocks of info starting with [radix], this also ignores comments
        if line.startswith("[radix]"):
            # define local variables
            x_original = None
            y_original = None
            m_original = None

            # parse radix and operation, which are always present
            obj['radix'] = int(line.split()[1])
            obj['operation'] = input_file.readline()[1:-2]

            # Parse rest
            for current_line in input_file:
                if current_line == '\n':
                    break

                key = current_line.split()[0][1:-1]

                if key == 'x':
                    x_original = current_line[:-1]
                elif key == 'y':
                    y_original = current_line[:-1]
                elif key == 'm':
                    m_original = current_line[:-1]
                elif key == 'answer':  # TODO: remove
                    obj['answer_original'] = current_line[:-1]

            if x_original:
                x = number_to_array(x_original.split()[1], obj['radix'])
                obj['x_original'] = x_original
                obj['x'] = x

            if y_original:
                y = number_to_array(y_original.split()[1], obj['radix'])
                obj['y_original'] = y_original
                obj['y'] = y

            if m_original:
                m = number_to_array(m_original.split()[1], obj['radix'])
                obj['m_original'] = m_original
                obj['m'] = m

            result.append(obj)
        else:  # if the block doesn't start with [radix], we keep going until we find a line that does.
            continue

    return result


def attach_answer(obj):
    op = obj.get('operation')
    x = obj.get('x')
    y = obj.get('y')
    m = obj.get('m')

    radix = obj['radix']
    if 'm' in obj:
        # Modular arithmetic
        if op == 'add':
            obj['answer'] = mod_add(x, y, radix, m)
        elif op == 'subtract':
            obj['answer'] = mod_sub(x, y, radix, m)
        elif op == 'multiply':
            obj['answer'] = mod_mult(x, y, radix, m)
        elif op == 'reduce':
            obj['answer'] = reduce(x, m, radix)
        elif op == 'inverse':
            obj['answer'] = inverse(x, m, radix)
    else:
        # Regular arithmetic
        if op == 'karatsuba':
            obj['answer'] = karatsuba(x, y, radix)
        elif op == 'add':
            obj['answer'] = add(x, y, radix)
        elif op == 'subtract':
            obj['answer'] = subtract(x, y, radix)
        elif op == 'multiply':
            obj['answer'] = mult(x, y, radix)
        elif op == 'euclid':
            obj['answ-d'], obj['answ-a'], obj['answ-b'] = euclid_gcd(
                x, y, radix)
        elif op == 'divide':
            obj['answer'] = divide(x, y, radix)
        else:
            obj['answer'] = [1]

    return obj


def print_output(obj):
    print('[radix]  {}'.format(obj['radix']))
    print('[{}]'.format(obj['operation']))
    if 'x_original' in obj:
        print(obj['x_original'])
    if 'y_original' in obj:
        print(obj['y_original'])
    if 'm_original' in obj:
        print(obj['m_original'])

    if obj['operation'] != 'euclid':
        if 'answer' in obj:
            print('[answer] {}'.format(array_to_number(obj['answer'])))
    else:
        if 'answ-d' in obj:
            print('[answ-d] {}'.format(array_to_number(obj['answ-d'])))
        if 'answ-a' in obj:
            print('[answ-a] {}'.format(array_to_number(obj['answ-a'])))
        if 'answ-b' in obj:
            print('[answ-b] {}'.format(array_to_number(obj['answ-b'])))
    if 'answer_original' in obj:  # TODO: remove
        print(obj['answer_original'] + ' original')
    # print operations done
    print('[operations] {}'.format(OPERATION_COUNT))
    # break line
    print()


def add(x_remote, y_remote, radix):
    # Copy local lists so we don't modify input parameters
    x = x_remote.copy()
    y = y_remote.copy()

    invert_outcome = False
    # If both x and y are negative, then invert, calculate and invert
    if is_negative(x) and is_negative(y):
        x = invert(x)
        y = invert(y)
        invert_outcome = True

    if is_negative(x) and not is_negative(y):
        x = invert(x)
        return invert(subtract(x, y, radix))

    if not is_negative(x) and is_negative(y):
        y = invert(y)
        return invert(subtract(y, x, radix))

    # Sanitise input
    while len(x) > len(y):
        y.append(0)

    while len(y) > len(x):
        x.append(0)

    # Definitions
    c = 0
    z = []  # The return list

    for i in range(0, len(x)):
        z.append(x[i] + y[i] + c)  # Add to end of list (z[i])
        if z[i] >= radix:
            z[i] = z[i] - radix
            c = 1
        else:
            c = 0
        increment_operation()

    if c == 1:  # Add final carry
        z.append(1)
        increment_operation()

    if invert_outcome:
        z = invert(z)

    return z


# Returns x - y
def subtract(x_remote, y_remote, radix):
    # Copy local lists so we don't modify input parameters
    x = x_remote.copy()
    y = y_remote.copy()

    # Sanitise input
    invert_solution = False

    # If we try to subtract a positive number from a negative number, it is the same as
    # adding the positive of those two numbers and returning the negative result.
    if is_negative(x) and not is_negative(y):
        x = invert(x)
        z = add(x, y, radix)
        return invert(z)

    # If we try to subtract a negative number from a positive number, it is the same as
    # adding the positive of those two numbers and returning the positive result.
    if not is_negative(x) and is_negative(y):
        y = invert(y)
        z = add(x, y, radix)
        return z

    # The algorithm requires x to be greater than y. If this is not the case, we swap x and y and invert the outcome,
    # resulting in a correct solution
    if is_greater_than(y, x):
        invert_solution = True
        temp = x
        x = y
        y = temp

    while len(x) > len(y):
        y.append(0)

    while len(y) > len(x):
        x.append(0)

    # Definitions
    c = 0
    z = []  # The return list

    for i in range(0, len(x)):
        z.append(
            x[i] - y[i] - c
        )  # Add to end of list (z[i]) TODO: deal with different length lists
        if z[i] < 0:
            z[i] = z[i] + radix
            c = 1
        else:
            c = 0
        increment_operation()

    while z[-1] == 0 and len(z) > 1:  # Remove leading zeroes
        z.pop()

    if invert_solution:
        return invert(z)
    else:
        return z


def mult(x_remote, y_remote, radix):
    # Copy local lists so we don't modify input parameters
    x = x_remote.copy()
    y = y_remote.copy()
    # Convert input to be positive, to fit the algorithm
    invert_outcome = False
    if is_negative(x) and is_negative(y):
        x = invert(x)
        y = invert(y)
        invert_outcome = False
    elif is_negative(x):
        x = invert(x)
        invert_outcome = True
    elif is_negative(y):
        y = invert(y)
        invert_outcome = True

    m = len(x)
    n = len(y)
    c = 0
    k = 0
    z = [0] * (m + n)

    for i in range(0, m):
        c = 0
        for j in range(0, n):
            t = z[i + j] + x[i] * y[j] + c
            c = floor(t / radix)
            z[i + j] = t - c * radix
            increment_operation(5)
        z[i + n] = c

    if z[m + n - 1] == 0:
        k = m + n - 2
    else:
        k = m + n - 1

    z = z[:k + 1]
    if invert_outcome:
        z = invert(z)
    return z


# recursively returns the product of x and y, where x and y are arrays of numbers, to represent a number of base radix
def karatsuba(x_remote, y_remote, radix):
    # Copy local lists so we don't modify input parameters
    x = x_remote.copy()
    y = y_remote.copy()

    while x[-1] == 0 and len(x) > 1:  # Remove leading zeroes
        x.pop()
    while y[-1] == 0 and len(y) > 1:
        y.pop()

    invert_outcome = False
    if is_negative(x) and is_negative(y):
        x = invert(x)
        y = invert(y)
        invert_outcome = False
    elif is_negative(x):
        x = invert(x)
        invert_outcome = True
    elif is_negative(y):
        y = invert(y)
        invert_outcome = True

    # Base case to break recursion
    if len(x) == 1 and len(y) == 1:
        if invert_outcome:
            return invert(mult(x, y, radix))
        return mult(x, y, radix)

    # Equalize number length
    while len(x) > len(y):
        y.append(0)

    while len(y) > len(x):
        x.append(0)

    if len(x) % 2 == 1:
        x.append(0)
        y.append(0)

    # SPLIT
    n = ceil(max(len(x), len(y)) / 2)

    # splitting numbers is easy because we are dealing with lists of numbers
    x_hi = x[n:]
    x_lo = x[:n]
    y_hi = y[n:]
    y_lo = y[:n]

    a = karatsuba(x_hi, y_hi, radix)
    c = karatsuba(x_lo, y_lo, radix)
    x_hi_lo_sum = add(x_hi, x_lo, radix)
    y_hi_lo_sum = add(y_hi, y_lo, radix)
    # b = ((x_hi + x_lo) * (y_hi + y_lo)) - c - a
    b = subtract(
        subtract(karatsuba(x_hi_lo_sum, y_hi_lo_sum, radix), c, radix), a,
        radix)

    # We get the result by adding a, b, and c, shifted accordingly.
    z = add(add(([0] * 2 * n) + a, ([0] * n) + b, radix), c, radix)

    # Transform output
    while z[-1] == 0 and len(z) > 1:  # Remove leading zeroes
        z.pop()
    # Invert if necessary
    if invert_outcome:
        return invert(z)
    else:
        return z


def mod_add(x_remote, y_remote, radix, m):
    # Copy local lists so we don't modify input parameters
    x = x_remote.copy()
    y = y_remote.copy()
    # The algorithm assumes input in reduced form
    reduce(x, m, radix)
    reduce(y, m, radix)

    z = add(x, y, radix)

    if not is_greater_than(m, z):
        z = subtract(z, m, radix)

    return z


def mod_sub(x_remote, y_remote, radix, m):
    # Copy local lists so we don't modify input parameters
    x = x_remote.copy()
    y = y_remote.copy()
    # The algorithm assumes input in reduced form
    reduce(x, m, radix)
    reduce(y, m, radix)

    z = subtract(x, y, radix)

    if is_negative(z):
        z = add(z, m, radix)

    return z


def mod_mult(x_remote, y_remote, radix, m):
    # Copy local lists so we don't modify input parameters
    x = x_remote.copy()
    y = y_remote.copy()
    # The algorithm assumes input in reduced form
    reduce(x, m, radix)
    reduce(y, m, radix)

    z = karatsuba(x, y, radix)

    z = reduce(z, m, radix)

    return z


# Efficient modular reduction with radix, follows algorithm 2.5
def reduce(x_remote, m, radix):
    # Copy local list so we don't modify input parameters
    x = x_remote.copy()

    invert_outcome = False
    # x' = |x|
    if is_negative(x):
        x = invert(x)
        invert_outcome = True

    k = len(x)
    n = len(m)
    for i in reversed(range(0, k - n + 1)):
        while not is_greater_than(([0] * i) + m, x):
            x = subtract(x, ([0] * i) + m, radix)

    if invert_outcome:
        return subtract(m, x, radix)
    else:
        return x


# Division method that returns floor(x/y) using long division
def divide(x_remote, y_remote, radix):
    # Copy local lists so we don't modify input parameters
    x = x_remote.copy()
    y = y_remote.copy()

    if is_negative(x):
        x = invert(x)
        invert_outcome = True
    if is_negative(y):
        y = invert(y)
        invert_outcome = True

    k = len(x)
    n = len(y)
    if n > k:
        return [0]

    z = [0] * (k - n + 1)
    for i in reversed(range(0, k - n + 1)):
        while not is_greater_than(([0] * i) + y, x):
            x = subtract(x, ([0] * i) + y, radix)
            z = add(z, ([0] * i) + [1], radix)

    while z[-1] == 0 and len(z) > 1:  # Remove leading zeroes
        z.pop()

    return z


# Modular inversion, follows algorithm 2.11
def inverse(a_remote, m_remote, radix):
    # Copy local lists so we don't modify input parameters
    a = a_remote.copy()
    m = m_remote.copy()

    x_1 = [1]
    x_2 = [0]

    while is_greater_than(m, [0]):
        q = divide(a, m, radix)
        r = subtract(a, karatsuba(q, m, radix), radix)
        a = m
        m = r
        x_3 = subtract(x_1, karatsuba(q, x_2, radix), radix)
        x_1 = x_2
        x_2 = x_3

    if is_equal(a, [1]):
        return reduce(x_1, m_remote, radix)
    else:
        print("inverso no existo")
        return [0]


def euclid_gcd(a, b, radix):
    x = [[0], [1], [0], [0]]
    y = [[0], [0], [1], [0]]

    # if is_greater_than(y, x):
    #     temp = x
    #     x = y
    #     y = temp

    ap = a
    bp = b

    if is_negative(a):
        ap = invert(a)

    if is_negative(b):
        bp = invert(b)

    while is_greater_than(bp, [0]):
        q = divide(ap, bp, radix)
        r = subtract(ap, karatsuba(q, bp, radix), radix)

        ap = bp
        bp = r

        t1 = karatsuba(q, x[2], radix)
        t2 = karatsuba(q, y[2], radix)
        x[3] = subtract(x[1], t1, radix)
        y[3] = subtract(y[1], t2, radix)
        x[1] = x[2]
        y[1] = y[2]
        x[2] = x[3]
        y[2] = y[3]

    d = ap

    while d[-1] == 0 and len(d) > 1:  # Remove leading zeroes
        d.pop()

    if is_greater_than(
            a, [0]):  # TODO: Must be changed to x >= 0 once negatives work
        x = x[1]
    else:
        x = invert(x[1])

    if is_greater_than(
            b, [0]):  # TODO: Must be changed to y >= 0 once negatives work
        y = y[1]
    else:
        y = invert(y[1])

    return d, x, y


def increment_operation(amount=1):
    global OPERATION_COUNT
    OPERATION_COUNT += amount


if __name__ == "__main__":
    main()
