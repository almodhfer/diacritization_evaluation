import random

from constants import *
from constants import punctuations


def get_different_haraqah(haraqah):
    if haraqah not in all_possible_haraqat.keys():
        raise AttributeError('haraqah is wrong {}'.format(haraqah))
    haraqat = list(all_possible_haraqat.keys())
    random.shuffle(haraqat)
    for h in haraqat:
        if h != haraqah:
            return h

    return None


def calculate_rate(equal:int, not_equal:int)-> float:
    return round(not_equal / max(1, (equal + not_equal)) * 100, 2)


def combine_txt_and_haraqat(txt_list, haraqat_list):
    assert len(txt_list) == len(haraqat_list)
    out = []
    for i, c in enumerate(txt_list):
        out.append(c)
        out.append(haraqat_list[i])
    return ''.join(out)


def get_case_ending_indices_from_un_daicritized_txt(text_only):
    text = text_only + [' ']
    indices = []
    end_words = punctuations + [' ']
    for i in range(len(text)):
        if text[i] in end_words and text[i - 1] in arab_chars_no_space:
            indices.append(i - 1)
    return indices


def get_case_ending_indices(content):
    _, text, _ = extract_haraqat(content)
    return get_case_ending_indices_from_un_daicritized_txt(text)


def extract_stack(stack):
    char_haraqat = []
    while len(stack) != 0:
        char_haraqat.append(stack.pop())
    full_haraqah = ''.join(char_haraqat)
    reversed_full_haraqah = ''.join(reversed(char_haraqat))
    if full_haraqah in all_possible_haraqat:
        out = full_haraqah
    elif reversed_full_haraqah in all_possible_haraqat:
        out = reversed_full_haraqah
    else:
        for c in full_haraqah:
            print(all_possible_haraqat[c])
        print('------------')
        raise ValueError
    return out


def extract_haraqat(sentence):
    if len(sentence.strip()) == 0:
        return sentence, [' '] * len(sentence), [''] * len(sentence)
    stack = []
    haraqat_list = []
    txt_list = []
    for i, char in enumerate(sentence):
        # if encounter Arabic character, then append char
        if char not in basic_haraqat.keys():
            haraqat_list.append(extract_stack(stack))
            txt_list.append(char)
            stack = []
        else:
            stack.append(char)
    if len(haraqat_list) > 0:
        del haraqat_list[0]
    haraqat_list.append(extract_stack(stack))

    return sentence, txt_list, haraqat_list
