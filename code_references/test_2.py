def get_line(lineno):
    re.search('', document.lines[lineno])

    split_input = document.lines[lineno].split(' ')
    aux_split_input = []
    for index, item in enumerate(split_input):
        for item_function in function_name:
            if split_input[index].startswith(item_function):
                aux_split_input.append((colors[10 % len(colors)], item_function))
            else:
                aux_split_input.append((colors[30 % len(colors)], item))

        if len(split_input) > 1:
            for keyword in arg_keywords:
                if split_input[index].startswith('--'):
                    if item == keyword:
                        aux_split_input.append((colors[100 % len(colors)], keyword))
                else:
                    aux_split_input.append((colors[30 % len(colors)], item))
    return aux_split_input

class RainbowLexer(Lexer):
    def lex_document(self, document):
        colors = list(sorted(NAMED_COLORS, key=NAMED_COLORS.get))

        def get_line(lineno):
            split_input_data = document.lines[lineno].split(' ')
            aux_split_input = []
            for item in split_input_data:
                try:
                    try:
                        get_function = re.search(
                            'isOwner|getThreshold|addOwner|swapOwner|removeOwner|changeThreshold|sendEther|sendToken|VERSION|NAME',
                            item).group(0)
                        # print(get_function)
                        aux_split_input.append((colors[10 % len(colors)], get_function))
                    except AttributeError:
                        try:
                            get_address = re.search(normal_address, item).group(0)
                            # print('address_data:', get_address)
                            aux_split_input.append((colors[10 % len(colors)], get_address))
                        except AttributeError:
                            try:
                                get_uint = re.search(uint_data, item).group(0)
                                # print('uint_data:', get_uint)
                                aux_split_input.append((colors[10 % len(colors)], get_uint))
                            except AttributeError:
                                try:
                                    get_execute = re.search(execute, item).group(0)
                                    # print('execute_data:', get_execute)
                                    aux_split_input.append((colors[10 % len(colors)], get_execute))
                                except AttributeError:
                                    try:
                                        get_queue = re.search(execute, item).group(0)
                                        # print('queue_data', get_queue)
                                        aux_split_input.append((colors[10 % len(colors)], get_queue))
                                    except AttributeError:
                                        # print(item)
                                        aux_split_input.append((colors[10 % len(colors)], item))
                except AttributeError:
                    continue

            return aux_split_input

        return get_line
