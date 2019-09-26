def set_to_array(original_set):
    result = []
    split_set = original_set.split(',')
    for group in split_set:
        if '{' or '}' in group:
            group = group.strip('{}')

        if group is not '':
            result.append(int(group))

    return result
