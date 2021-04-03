"""
Calculating WER
"""

from .constants import ALL_POSSIBLE_HARAQAT
from .util import calculate_rate, get_word_without_case_ending, has_arabic_letters


def calculate_wer(
    original_content, predicted_content, case_ending=True, include_non_arabic=False
):
    """
    Calculate Word Error Rate (WER) from two text content
    Args
        original_content (str): the original text that contains the correct
        diacritization.
        predicted_content (str): the predicted text
        case_ending (str): whether to include the last character of each word darning
        the calculation
        include_non_arabic (bool): any space separated word other than Arabic,
        such as punctuations
    Returns:
        WER : The  word error rate (WER)

    """

    original = original_content.split()
    prediction = predicted_content.split()

    # If the whole word is a diacritic, then skip it since it my cause error in the WER caclulation
    #by shifting all remaining words.
    prediction = [
        word for word in prediction if word not in ALL_POSSIBLE_HARAQAT.keys()
    ]
    original = [word for word in original if word not in ALL_POSSIBLE_HARAQAT.keys()]

    assert len(prediction) == len(original)

    equal = 0
    not_equal = 0

    for _, (original_word, predicted_word) in enumerate(zip(original, prediction)):
        if not include_non_arabic:

            if not has_arabic_letters(original_word) and not has_arabic_letters(
                predicted_word
            ):
                continue

        if not case_ending:
            # When not using case_ending, exclude the last char of each word from
            # calculation
            original_word = get_word_without_case_ending(original_word)
            predicted_word = get_word_without_case_ending(predicted_word)

        if original_word == predicted_word:
            equal += 1
        else:
            not_equal += 1

    return calculate_rate(equal, not_equal)


def calculate_wer_from_path(
    original_path: str,
    predicted_path: str,
    case_ending: bool = True,
    include_non_arabic: bool = False,
) -> float:
    """
    Given the input path and the out_path, this function read the content
    of both files and call calculate_der function.
    Args:
        original_path: the path to the original file
        predicted_path: the path to the predicted file
        case_ending: whether to calculate the last character of each word or not
    Return:
     DER: the diacritic error rate between the two files
    """
    with open(original_path, encoding="utf8") as file:
        original_content = file.read()

    with open(predicted_path, encoding="utf8") as file:
        predicted_content = file.read()

    return calculate_wer(
        original_content,
        predicted_content,
        case_ending=case_ending,
        include_non_arabic=include_non_arabic,
    )
