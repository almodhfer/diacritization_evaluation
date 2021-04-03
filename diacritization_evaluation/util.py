"""
Util functions that are helpful for calculating DER and WER
"""
import random
from .constants import (
    ALL_POSSIBLE_HARAQAT,
    BASIC_HARAQAT,
    ARAB_CHARS_NO_SPACE,
    VALID_ARABIC,
)


def get_different_haraqah(haraqah):
    """
    Given a haraqah, this function return a random haraqah from all possible haraqat
    but different than this one
    """
    if haraqah not in ALL_POSSIBLE_HARAQAT.keys():
        raise AttributeError("haraqah is not in correct{}".format(haraqah))
    haraqat = list(ALL_POSSIBLE_HARAQAT.keys())
    random.shuffle(haraqat)
    for _haraqah in haraqat:
        if _haraqah != haraqah:
            return _haraqah

    return None


def calculate_rate(equal: int, not_equal: int) -> float:
    """
    Given an Equal and  not equal values, this function calculate the error rate
    Args:
    equal: the number of matching values when comparing two files, this can be in
    a word level or diacritic level
    not_equal: the number of un_matching
    Returns:
    The error rate
    """
    return round(not_equal / max(1, (equal + not_equal)) * 100, 2)


def combine_txt_and_haraqat(txt_list, haraqat_list):
    """
    Rejoins text with its corresponding haraqat
    Args:
    txt_list: The text that does not contain any haraqat
    haraqat_list: The haraqat that are corresponding to the text list
    """

    assert len(txt_list) == len(haraqat_list)
    out = []
    for i, char in enumerate(txt_list):
        out.append(char)
        out.append(haraqat_list[i])
    return "".join(out)


def get_case_ending_indices_from_un_diacritized_txt(text):
    text = text + [" "]
    indices = []
    for i in range(len(text)):
        if text[i] not in  ARAB_CHARS_NO_SPACE and text[i - 1] in ARAB_CHARS_NO_SPACE:
            indices.append(i - 1)
    return indices


def get_case_ending_indices(content):
    _, text, _ = extract_haraqat(content)
    return get_case_ending_indices_from_un_diacritized_txt(text)


def extract_stack(stack, correct_reversed: bool = True):
    """
    Given stack, we extract its content to string, and check whether this string is
    available at all_possible_haraqat list: if not we raise an error. When correct_reversed
    is set, we also check the reversed order of the string, if it was not already correct.
    """
    char_haraqat = []
    while len(stack) != 0:
        char_haraqat.append(stack.pop())
    full_haraqah = "".join(char_haraqat)
    reversed_full_haraqah = "".join(reversed(char_haraqat))
    if full_haraqah in ALL_POSSIBLE_HARAQAT:
        out = full_haraqah
    elif reversed_full_haraqah in ALL_POSSIBLE_HARAQAT and correct_reversed:
        out = reversed_full_haraqah
    else:
        raise ValueError(
            f"""The chart has the following haraqat which are not found in
        all possible haraqat: {'|'.join([ALL_POSSIBLE_HARAQAT[diacritic]
                                         for diacritic in full_haraqah ])}"""
        )
    return out


def extract_haraqat(text: str, correct_reversed: bool = True):
    """
    Args:
    text (str): text to be diacritized
    Returns:
    text: the text as came
    text_list: all text that are not haraqat
    haraqat_list: all haraqat_list

    """
    if len(text.strip()) == 0:
        return text, [" "] * len(text), [""] * len(text)
    stack = []
    haraqat_list = []
    txt_list = []
    for char in text:
        # if chart is a diacritic, then extract the stack and empty it
        if char not in BASIC_HARAQAT.keys():
            stack_content = extract_stack(stack, correct_reversed=correct_reversed)
            haraqat_list.append(stack_content)
            txt_list.append(char)
            stack = []
        else:
            stack.append(char)
    if len(haraqat_list) > 0:
        del haraqat_list[0]
    haraqat_list.append(extract_stack(stack))

    return text, txt_list, haraqat_list


def get_word_without_case_ending(word: str):
    _, text, haraqat = extract_haraqat(word)
    indices = get_case_ending_indices_from_un_diacritized_txt(text)

    if len(indices) == 0:
        return -1

    idx = indices[-1]
    text = text[:idx] + text[idx + 1 :]
    haraqat = haraqat[:idx] + haraqat[idx + 1 :]
    output = combine_txt_and_haraqat(text, haraqat)
    return output


def remove_diacritics(text: str):
    for diacritic in BASIC_HARAQAT.keys():
        text = text.replace(diacritic, "")

    return text


def has_arabic_letters(text: str):
    for char in VALID_ARABIC:
        if char in text:
            return True

    return False


def count_diacritics(text: str, skip_count_equal: int = None):
    _, text, extracted_haraqat = extract_haraqat(text)

    count = 0
    for extracted_haraqah in extracted_haraqat:
        if extracted_haraqah != "" and extracted_haraqah in ALL_POSSIBLE_HARAQAT.keys():
            count += 1
            if skip_count_equal and count >= skip_count_equal:
                return count
    return count


if __name__ == "__main__":
    counted = count_diacritics("لِيُهْرِيقَ")
    counted2 = count_diacritics("،", skip_count_equal=2)
    counted3 = count_diacritics(".(7/40)", skip_count_equal=2)
    counted4 = count_diacritics("213123", skip_count_equal=2)
    print(counted, counted2, counted3, counted4)
