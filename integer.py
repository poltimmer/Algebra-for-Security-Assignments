from math import ceil
from math import floor


def parse_input():
    input_file = open("input.txt", "r")

    result = []

    for line in input_file:
        obj = {}
        # we only accept blocks of info starting with [radix], this also ignores comments
        if line.startswith("[radix]"):
            # define local variables
            x_original = None
            y_original = None
            m_original = None

            # parse radix and operation, which are always present
            radix = int(line.split()[1])
            operation = input_file.readline()[1:-2]

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

            # insert values into return object
            obj['radix'] = radix
            obj['operation'] = operation

            if x_original:
                x = number_to_array(x_original.split()[1], radix)
                obj['x_original'] = x_original
                obj['x'] = x
            if y_original:
                y = number_to_array(y_original.split()[1], radix)
                obj['y_original'] = y_original
                obj['y'] = y
            if m_original:
                m = number_to_array(m_original.split()[1], radix)
                obj['m_original'] = m_original
                obj['m'] = m

            result.append(obj)
            print(obj)
            solution = karatsuba(obj['x'], obj['y'], obj['radix'])
            print('SOLUTION!!!!!!!!!!!!!!!!')
            print(solution)
        # if the block doesn't start with [radix], we keep going until we find a line that does.
        else:
            continue

        print_output(obj)


def print_output(sol):
    print('[radix]  {}'.format(sol['radix']))
    print('[{}]'.format(sol['operation']))
    if 'x_original' in sol:
        print(sol['x_original'])
    if 'y_original' in sol:
        print(sol['y_original'])
    if 'm_original' in sol:
        print(sol['m_original'])
    if 'answer' in sol:
        print('[answer] {}'.format(array_to_number(sol['answer'])))
    # break line
    print()


def add(x, y, radix):
    # Sanitise input
    while len(x) > len(y):
        y.append(0)

    while len(y) > len(x):
        x.append(0)

    # Definitions
    m = len(x)
    n = len(y)
    c = 0
    z = []  # The return list

    for i in range(0, max(m, n)):
        z.append(x[i] + y[i] + c)  # Add to end of list (z[i]) TODO: deal with different length lists
        if z[i] >= radix:
            z[i] = z[i] - radix
            c = 1
        else:
            c = 0

    if c == 1:  # Add final carry
        z.append(1)

    return z


def subtract(x, y, radix):
    # Sanitise input
    invert_solution = False
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
    m = len(x)
    n = len(y)
    c = 0
    z = []  # The return list

    for i in range(0, m):
        z.append(x[i] - y[i] - c)  # Add to end of list (z[i]) TODO: deal with different length lists
        if z[i] < 0:
            z[i] = z[i] + radix
            c = 1
        else:
            c = 0

    while z[-1] == 0:  # Remove leading zeroes
        z.pop()

    if invert_solution:
        return invert(z)
    else:
        return z


def mult(x, y, radix):
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

    return z[:k + 1]


# recursively returns the product of x and y, where x and y are arrays of numbers, to represent a number of base radix
def karatsuba(x, y, radix):
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
    split = radix ** n

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
    b = subtract(subtract(karatsuba(x_hi_lo_sum, y_hi_lo_sum, radix), c, radix), a, radix)

    # again, we are dealing with lists, so we don't need to multiply by any radix
    return a + b + c


def mod_add(x, y, m):

    reduce(x, m, radix) #reduce x to modulo m
    reduce(y, m, radix) #reduce y to modulo m


    z = x + y

    if z < m:
        z = z
    else:
        z = z - m

    return (z "mod" m)


def mod_sub(x, y, m):

    reduce(x, m, radix)
    reduce(y, m, radix)

    z = x - y

    if z => 0:
        z = z
    else:
        z = z + m

    return (z "mod" m)


def mod_mult(x, y, m):

    reduce(x, m, radix)
    reduce(y, m, radix)

    z = x*y

    while z => m:
         z = z - m

    return (z "mod" n)


#
# def euclid_gcd(x, y, radix):
#     while is_greater_than(y, [0]):
#         r = x
#         while is_greater_than(r, y):
#             r = subtract(r, y, radix)
#     return True


# Returns boolean whether x is greater than y, where x and y are numbers in list representation, with the digit of
# lowest significance being first in the list.
def is_greater_than(x, y):
    for a, b in zip(reversed(x), reversed(y)):
        if a > b:
            return True
        elif a < b:
            return False
    return False


def is_equal(x, y):
    for a, b in zip(x, y):
        if a != b:
            return False
    return True


def invert(x):
    result = []
    for number in x:
        result.append(-number)
    return result


# converts a string number of base [radix] to an array of integers, still of base [radix]
def number_to_array(n, radix):
    result = []
    for digit in n:
        result.append(int(digit, radix))
    result.reverse()
    return result


# does the opposite of number_to_array
# doesn't need radix, as input array is an array of integers that can be larger than 9
def array_to_number(a):
    result = ''
    a.reverse()
    for digit in a:
        result += dec_to_string(digit)
    return result


# takes a single digit, represented as an int (could be higher than 10) and returns it as a string character,
# allowing up to base 16.
def dec_to_string(n):
    if n < 10:
        return str(n)
    elif n == 10:
        return "a"
    elif n == 11:
        return "b"
    elif n == 12:
        return "c"
    elif n == 13:
        return "d"
    elif n == 14:
        return "e"
    elif n == 15:
        return "f"


parse_input()
