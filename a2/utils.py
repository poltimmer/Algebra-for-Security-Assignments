from primes import primes
import itertools as it


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


def clear_leading_zeroes(x_remote):
    x = x_remote.copy()

    while x[0] == 0 and len(x) > 1:
        x = x[1:]

    return x


# Converts a polynomial to a string representing that polynomial. Assumes positive coefficients.
def poly_string(x):
    result = ''

    for power, coefficient in enumerate(reversed(x)):
        term = ''
        if coefficient > 1:
            term += str(coefficient)
        elif coefficient == 1:
            if power > 0:
                pass
            else:
                term += str(coefficient)
        else:
            continue

        if power > 1:
            term += 'X^' + str(power)
        elif power == 1:
            term += 'X'

        result = term + '+' + result

    # If nothing gets added to result then we should just return 0
    if result == '':
        return '0'
    else:
        return result[:-1]  # Removes '+' at the end


def reduce_poly(x_remote, m):
    x = x_remote.copy()

    for i in range(len(x)):
        x[i] = x[i] % m

    return x


def find_prime_factors(x):
    result = []
    for prime in primes:
        if prime > x:
            return result
        while x % prime == 0:
            x = x / prime
            if len(result) == 0 or result[-1] != prime:
                result.append(prime)

    return result


def find_all_elements_field(m, poly_mod):
    d = len(poly_mod) - 1

    a = list(range(m))
    f = list((map(list, it.product(a, repeat=d))))

    return f



