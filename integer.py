import re


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
                x = x_original.split()[1]
                x_array = int_to_array(x, radix)
                obj['x_original'] = x_original
                obj['x'] = x_array
            if y_original:
                y = y_original.split()[1]
                y_array = int_to_array(y, radix)
                obj['y_original'] = y_original
                obj['y'] = y_array
            if m_original:
                m = m_original.split()[1]
                m_array = int_to_array(m, radix)
                obj['m_original'] = m_original
                obj['m'] = m_array

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

    print()


def int_to_array(s, radix):
    result = []
    for digit in s:
        result.append(int(digit, radix))
    result.reverse()
    return result


parse_input()

# print_output({'radix': 2})
