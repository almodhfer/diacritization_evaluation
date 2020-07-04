from util import *


def calculate_der(original_content:str, prediction_content:str, case_ending:bool = True)-> float:
    _, original_text, original_haraqat = extract_haraqat(original_content)
    _, original_text, prediction_haraqat = extract_haraqat(prediction_content)

    if not case_ending:
        indices = get_case_ending_indices_from_un_daicritized_txt(original_text)
        for i in indices:
            original_haraqat[i] = 0

    equal = 0
    not_equal = 0
    for i, (c1, c2) in enumerate(zip(original_haraqat, prediction_haraqat)):
        if not case_ending:
            if c1 == 0:
                continue
        if c1 == c2:
            equal += 1
        else:
            not_equal += 1
    return calculate_rate(equal, not_equal)


def calculate_der_from_path(inp_path:str, out_path:str, case_ending:bool = True) -> float:
    with open(inp_path, encoding='utf8') as file:
        inp_content = file.read()
    with open(out_path, encoding='utf8') as file:
        out_content = file.read()

    return calculate_der(inp_content, out_content, case_ending)
