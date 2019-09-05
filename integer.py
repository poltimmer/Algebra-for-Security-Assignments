import re


def parse():
    input_file = open("input.txt", "r")

    result = []

    for line in input_file:
        obj = {}

        if line.startswith("#"):
            print("skip")
            continue
        elif line.startswith("[radix]"):
            radix = int(line.split()[1])
            operation_original = input_file.readline()
            x_original = input_file.readline()
            y_original = input_file.readline()

            operation = re.findall(r'\[([^\[\]]*)\]', operation_original)[0]
            x = x_original.split()[1]
            y = y_original.split()[1]

            answer = input_file.readline().split()[1]

            int_to_array(x, radix)
            int_to_array(y, radix)

            obj['operation_original'] = operation_original
            obj['x_original'] = x_original
            obj['y_original'] = y_original

            obj['radix'] = radix
            obj['operation'] = operation
            obj['x'] = x
            obj['y'] = y

            result.append(obj)
        else:
            print("nothing here")

        print(obj)


# print(int('149bf28597ae40bbfdd09', 16))


def print_output(sol):
    print('[radix]  {}'.format(sol['radix']))
    print(sol['operation_original'])
    print(sol['x_original'])
    print(sol['y_original'])


def int_to_array(s, radix):
    result = []
    for digit in s:
        result.append(int(digit, radix))
    result.reverse()
    print(result)


parse()

# print_output({'radix': 2})
