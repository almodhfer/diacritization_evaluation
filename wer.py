from util import *


def calculate_wer(original_content, prediction_content, case_ending=True):
    original = original_content.split()
    prediction = prediction_content.split()
    # print('before {} {}'.format(len(original), len(prediction)))
    prediction = [p for p in prediction if p not in all_possible_haraqat.keys()]
    original = [o for o in original if o not in all_possible_haraqat.keys()]
    # print('after {} {}'.format(len(original), len(prediction)))
    for p in prediction:
        if p in all_possible_haraqat.keys():
            raise AssertionError()
    equal = 0
    not_equal = 0
    for i, (w1, w2) in enumerate(zip(original, prediction)):
        if not case_ending:
            _, w1, h1 = extract_haraqat(w1)
            _, w2, h2 = extract_haraqat(w2)
            w1 = combine_txt_and_haraqat(w1[:-1], h1[:-1])
            w2 = combine_txt_and_haraqat(w2[:-1], h2[:-1])

        if w1 == w2:
            equal += 1
        else:
            not_equal += 1
    return calculate_rate(equal, not_equal)


def calculate_wer_from_path(inp_path, out_path, case_ending=True):
    with open(inp_path, encoding='utf8') as file:
        inp_content = file.read()
    with open(out_path, encoding='utf8') as file:
        out_content = file.read()

    return calculate_wer(inp_content, out_content, case_ending)
