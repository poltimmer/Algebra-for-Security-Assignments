from math import ceil


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


def addition(x, y, radix)
    m = len(x)
    n = len(y)
    c = 0

    for i in range(0, max(m, n) - 1):
        x[i]+y[i]+c = z[i]
        if z[i] >= radix:
            z[i] = z[i] - radix
            c = 1
        else
            c = 0
    if c = 1:
        k = max(m, n) + 1
        z[k] = 1
    else k = max(m, n)
    
return reversed(z[k])

def substraction(x, y, radix)
    c = 0

    for i in range(0, len(x) - 1):
        x[i]-y[i]-c = z[i]
        if z[i] < 0:
            z[i] = z[i] + radix
            c = 1
        else
            c = 0
    k = m
    while k => 2 & z[k] = 0:
        k = k-1
        
return reversed(z[k])


# recursively returns the product of x and y, where x and y are arrays of numbers, to represent a number of base radix
def karatsuba(x, y, radix):
    # base
    if x < radix and y < radix:
        # TODO: modify multiplication for list of numbers
        return x * y

    # SPLIT
    n = ceil(max(x.length(), y.length()) / 2)
    split = radix ** n

    # splitting numbers is easy because we are dealing with lists of numbers
    x_hi = x[n:]
    x_lo = x[:n]
    y_hi = y[n:]
    y_lo = x[:n]

    a = karatsuba(x_hi, y_hi, radix)
    c = karatsuba(x_lo, y_lo, radix)
    b = karatsuba(x_hi + x_lo, y_hi + y_lo, radix) - c - a  # TODO: modify addition and subtraction for list of numbers

    # again, we are dealing with lists, so we don't need to multiply by any radix
    return a + b + c
