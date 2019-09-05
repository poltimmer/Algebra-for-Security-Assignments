def parse():
	input = open("input.txt", "r")

	result = []

	for line in input:
		obj = {}

		if line.startswith("#"):
			print("skip")
			continue
		elif line.startswith("[radix]"):
			radix = int(line.split()[1])
			operation_original = input.readline()

			x_original = input.readline()
			y_original = input.readline()

			x = x_original.split()[1]
			y = y_original.split()[1]

			answer = input.readline().split()[1]

			int_to_array(x, radix)
			int_to_array(y, radix)


			obj['radix'] = radix
			obj['operation'] = operation
			obj['x'] = x
			obj['y'] = y


			result.append(obj)
		else:
			print("nothing here")

		print(obj)

	# print(int('149bf28597ae40bbfdd09', 16))

def int_to_array(s, radix):
	result = []
	for digit in s:
		result.append(int(digit, radix))
	result.reverse()
	print(result)

parse()
