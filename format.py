async def convert_string(string):
    converted_string = ''
    for char in string:
        if char == " ":
            converted_string += ' '
        elif char == ":":
            converted_string += '꞉'
        else:
            converted_string += char
    return converted_string


def convert_int(int):
    chars = list(str(int))[::-1]
    numlist = []
    string = ""
    for i in range(len(chars)):
        if i % 3 == 0:
            numlist.append('.')
        numlist.append(chars[i])
    numlist.pop(0)
    numlist = numlist[::-1]
    for char in numlist:
        string+=char
    return string
