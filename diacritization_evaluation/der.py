"""
Calculating the DER
"""

from .util import (
    extract_haraqat,
    get_case_ending_indices_from_un_diacritized_txt,
    calculate_rate,
)


def calculate_der(
    original_content: str, predicted_content: str, case_ending: bool = True
) -> float:
    """Given the original text and the predicted text,
    this function calculate the DER
    between these two files.
    Args
        original_content (str): the original text that contains the correct
        diacritization.
        predicted_content (str): the predicted text
        case_ending (str): whether to include the last character of each word darning
        the calculation
    Returns:
        DER: the  diacritic error rate (DER)
    """
    _, original_text, original_haraqat = extract_haraqat(original_content)
    _, predicted_text, predicted_haraqat = extract_haraqat(predicted_content)

    SKIP_CASE_ENDING_VALUE = -1
    if not case_ending:
        indices = get_case_ending_indices_from_un_diacritized_txt(original_text)
        for i in indices:
            original_haraqat[i] = SKIP_CASE_ENDING_VALUE

    equal = 0
    not_equal = 0
    for i, (original_char, predicted_chart) in enumerate(
        zip(original_haraqat, predicted_haraqat)
    ):
        if not case_ending:
            if original_char == SKIP_CASE_ENDING_VALUE:
                continue
        if original_char == predicted_chart:
            equal += 1
        else:
            not_equal += 1

    return calculate_rate(equal, not_equal)


def calculate_der_from_path(
    original_path: str, predicted_path: str, case_ending: bool = True
) -> float:
    """Given the original_ path and the predicted_path, this function read the content
    of both files and call calculate_der function.
    Args:
        original_path (str): the path to the original file
        predicted_path (str): the path to the generated file
        case_ending (bool): whether to calculate the last character of each word or not
    Return:
     DER: the diacritic error rate between the two files
    """
    with open(original_path, encoding="utf8") as file:
        original_content = file.read()

    with open(predicted_path, encoding="utf8") as file:
        predicted_content = file.read()

    return calculate_der(original_content, predicted_content, case_ending)
