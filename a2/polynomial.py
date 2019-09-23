from a1.utils import number_to_array
from utils import set_to_array

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
        print(obj)
        obj = generate_answer(obj)

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
                elif '[' not in key:
                    if key != '':
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
    return []


def print_output(objects):
    pass


if __name__ == "__main__":
    main()
