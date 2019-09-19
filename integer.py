from math import ceil, floor
from time import sleep

from utils import (array_to_number, invert, is_equal, is_greater_than,
                   is_negative, number_to_array)

INPUTFILE = "test1.txt"
OUTPUTFILE = "output.txt"

x_neg = False
y_neg = False


def parse_input():
    global x_neg
    global y_neg

    try:
        input_file = open(INPUTFILE, "r")
    except:
        print(
            "Input file {} not found in current dirctory. Make sure the file is in the same directory!"
            .format(INPUTFILE))
        return

    for line in input_file:
        obj = {}
        # we only accept blocks of info starting with [radix], this also ignores comments
        if line.startswith("[radix]"):
            x_neg = False
            y_neg = False
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
                if '-' in x_original:
                    x_neg = True

            if y_original:
                y = number_to_array(y_original.split()[1], obj['radix'])
                obj['y_original'] = y_original
                obj['y'] = y
                if '-' in y_original:
                    y_neg = True

            if m_original:
                m = number_to_array(m_original.split()[1], obj['radix'])
                obj['m_original'] = m_original
                obj['m'] = m

            obj = choose_operation(obj)
            print('SOLUTION!!!!!!!!!!!!!!!!')
        # if the block doesn't start with [radix], we keep going until we find a line that does.
        else:
            continue

        print_output(obj)


def choose_operation(obj):
    op = obj.get('operation')
    x = obj.get('x')
    y = obj.get('y')
    m = obj.get('m')

    radix = obj['radix']
    if op == 'karatsuba':
        obj['answer'] = karatsuba(x, y, radix)
    elif op == 'add':
        obj['answer'] = add(x, y, radix)
    elif op == 'subtract':
        obj['answer'] = subtract(x, y, radix)
    elif op == 'multiply':
        obj['answer'] = mult(x, y, radix)
    elif op == 'reduce':
        obj['answer'] = reduce(x, m, radix)
    elif op == 'euclid':
        obj['answ-d'], obj['answ-a'], obj['answ-b'] = euclid_gcd(x, y, radix)
    else:
        obj['answer'] = [1]

    return obj


def print_output(sol):
    print('[radix]  {}'.format(sol['radix']))
    print('[{}]'.format(sol['operation']))
    if 'x_original' in sol:
        print(sol['x_original'])
    if 'y_original' in sol:
        print(sol['y_original'])
    if 'm_original' in sol:
        print(sol['m_original'])

    if sol['operation'] != 'euclid':
        if 'answer' in sol:
            print('[answer] {}'.format(array_to_number(sol['answer'])))
    else:
        if 'answ-d' in sol:
            print('[answ-d] {}'.format(array_to_number(sol['answ-d'])))
        if 'answ-a' in sol:
            print('[answ-a] {}'.format(array_to_number(sol['answ-a'])))
        if 'answ-b' in sol:
            print('[answ-b] {}'.format(array_to_number(sol['answ-b'])))
    if 'answer_original' in sol:  # TODO: remove
        print(sol['answer_original'] + ' original')
    # break line
    print()


def add(x, y, radix):
    invert_outcome = False
    # If both x and y are negative, then invert, calculate and invert
    if is_negative(x) and is_negative(y):
        x = invert(x)
        y = invert(y)
        invert_outcome = True

    if is_negative(x) and not is_negative(y):
        x = invert(x)
        z = subtract(x, y, radix)
        return invert(z)

    if not is_negative(x) and is_negative(y):
        y = invert(y)
        z = subtract(y, x, radix)
        return invert(z)

    # Sanitise input
    while len(x) > len(y):
        y.append(0)

    while len(y) > len(x):
        x.append(0)

    # Definitions
    c = 0
    z = []  # The return list

    for i in range(0, len(x)):
        z.append(
            x[i] + y[i] + c
        )  # Add to end of list (z[i]) TODO: deal with different length lists
        if z[i] >= radix:
            z[i] = z[i] - radix
            c = 1
        else:
            c = 0

    if c == 1:  # Add final carry
        z.append(1)

    if invert_outcome:
        z = invert(z)


    return z


def subtract(x, y, radix):
    # Sanitise input
    invert_solution = False

    if is_negative(x) and not is_negative(y):
        x = invert(x)
        z = add(x, y, radix)
        return invert(z)

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

    while z[-1] == 0 and len(z) > 1:  # Remove leading zeroes
        z.pop()

    if invert_solution:
        return invert(z)
    else:
        return z


def mult(x, y, radix):
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
def karatsuba(x, y, radix):
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

    # base
    if is_greater_than([radix], x) and is_greater_than([radix], y):
        # TODO: modify multiplication for list of numbers
        return mult(x, y, radix)

    # Sanitise input
    while len(x) > len(y):
        y.append(0)

    while len(y) > len(x):
        x.append(0)

    if len(x) % 2 == 1:
        x.append(0)
        y.append(0)

    # SPLIT
    n = ceil(max(len(x), len(y)) / 2)
    split = radix**n

    # splitting numbers is easy because we are dealing with lists of numbers
    x_hi = x[n:]
    x_lo = x[:n]
    y_hi = y[n:]
    y_lo = x[:n]

    a = karatsuba(x_hi, y_hi, radix)
    c = karatsuba(x_lo, y_lo, radix)
    x_hi_lo_sum = add(x_hi, x_lo, radix)
    y_hi_lo_sum = add(y_hi, y_lo, radix)
    # b = ((x_hi + x_lo) * (y_hi + y_lo)) - c - a
    b = subtract(
        subtract(karatsuba(x_hi_lo_sum, y_hi_lo_sum, radix), c, radix), a,
        radix)

    z = a + b + c
    while z[-1] == 0 and len(z) > 1:  # Remove leading zeroes
        z.pop()
    # again, we are dealing with lists, so we don't need to multiply by any radix
    if invert_outcome:
        return invert(z)
    else:
        return z


def mod_add(x, y, radix, m):
    reduce(x, m, radix)  # reduce x to modulo m
    reduce(y, m, radix)  # reduce y to modulo m

    z = x + y

    if z < m:
        z = z
    else:
        z = z - m

    return z


def mod_sub(x, y, radix, m):
    reduce(x, m, radix)
    reduce(y, m, radix)

    z = x - y

    if z >= 0:
        z = z
    else:
        z = z + m

    return z


def mod_mult(x, y, radix, m):
    reduce(x, m, radix)
    reduce(y, m, radix)

    z = x * y

    while z >= m:
        z = z - m

    return z


def reduce(x, m, radix):
    if is_negative(m):
        m = invert(m)

    if is_negative(x) and not is_negative(m):
        r = [0]
        while is_greater_than(r, x):
            r = subtract(r, m, radix)
        r = subtract(x, r, radix)
    elif not is_negative(x) and not is_negative(m):
        r = x
        while is_greater_than(r, m):
            r = subtract(r, m, radix)

    if is_greater_than(r, [0]):
        while r[-1] == 0:  # Remove leading zeroes
            r.pop()

    return r


def divide(x, y, radix):
    '''
    Custom division method that counts the amount of additions before the denominator exceeds the numerator.
    Returns floor(x/y)
    '''
    counter = [0]
    ytemp = y

    while is_greater_than(x, ytemp):
        counter = add(counter, [1], radix)
        ytemp = add(ytemp, y, radix)

        if is_equal(x, ytemp):
            counter = add(counter, [1], radix)
            return counter

    return counter


def euclid_gcd(x, y, radix):
    c = [[0], [1], [0], [0]]
    d = [[0], [0], [1], [0]]
    xp = x  # TODO: Must both be the absolute value!
    yp = y

    while is_greater_than(yp, [0]):
        q = divide(xp, yp, radix)
        r = subtract(xp, mult(q, yp, radix), radix)

        xp = yp
        yp = r

        t1 = mult(q, c[2], radix)
        t2 = mult(q, d[2], radix)
        c[3] = subtract(c[1], t1, radix)
        d[3] = subtract(d[1], t2, radix)
        c[1] = c[2]
        d[1] = d[2]
        c[2] = c[3]
        d[2] = d[3]

    gcd = xp

    while gcd[-1] == 0 and len(gcd) > 1:  # Remove leading zeroes
        gcd.pop()

    if 1 >= 0:  # TODO: Must be changed to x >= 0 once negatives work
        c = c[1]
    else:
        c = -1 * c[1]

    if 1 >= 0:  # TODO: Must be changed to y >= 0 once negatives work
        d = d[1]
    else:
        d = -1 * d[1]

    return gcd, c, d


if __name__ == "__main__":
    parse_input()
