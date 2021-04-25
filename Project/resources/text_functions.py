def delete_first_nums(str):
    nums = ""
    for s in str:
        if s.isdigit():
            nums += s
        else:
            break
    return str[str.find(nums) + len(nums):]


def get_first_nums(str):
    s = ''
    for symbol in str:
        if symbol.isdigit():
            s = s + symbol
        else:
            return s
