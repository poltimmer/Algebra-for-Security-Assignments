from a2.utils import test

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
            obj['mod'] = int(line.split()[1])
            obj['operation'] = input_file.readline()[1:-2]

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
