# Returns boolean whether x is greater than y, where x and y are numbers in list representation, with the digit of
# lowest significance being first in the list.
def is_greater_than(x, y):
    while len(x) > len(y):
        y.append(0)
    while len(y) > len(x):
        x.append(0)

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
    invert_outcome = False
    result = []
    for digit in n:
        if digit == '-':  # TODO: implement negative numbers
            invert_outcome = True
            continue
        result.append(int(digit, radix))
    result.reverse()

    if invert_outcome:
        return invert(result)

    return result


# does the opposite of number_to_array
# doesn't need radix, as input array is an array of integers that can be larger than 9
def array_to_number(a):
    result = ''
    a.reverse()
    if a[0] < 0:
        result += '-'

    for digit in a:
        result += dec_to_string(digit)
    return result


# takes a single digit, represented as an int (could be higher than 10) and returns it as a string character,
# allowing up to base 16.
def dec_to_string(n):
    n = abs(n)
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
    else:
        return 'E'


def is_negative(x):
    return is_greater_than([0], x)
