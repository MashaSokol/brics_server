import difflib


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


def delete_not_alphas(str):
    new_str = ""
    for s in str:
        if not s.isalpha():
            new_str += s
    return new_str


def similarity(s1, s2):
    normalized1 = delete_not_alphas(s1.lower())
    normalized2 = delete_not_alphas(s2.lower())
    matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
    return matcher.ratio()
