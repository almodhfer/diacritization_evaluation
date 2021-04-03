""" DER Test Module """

import os
import unittest
import random

from diacritization_evaluation.der import calculate_der

from util import (
    calculate_rate,
    extract_haraqat,
    get_case_ending_indices_from_un_diacritized_txt,
    get_different_haraqah,
    combine_txt_and_haraqat,
)


class DERTest(unittest.TestCase):
    """ Test Diacritic Error Rate with and without Case Ending

        This is done by  changing  random diacritics and checking wether the
        DER function outputs align with the changes that we made.

    """

    def setUp(self):
        self.case_ending_change = 2000
        self.not_case_ending_change = 5000
        self.number_of_changes = self.case_ending_change + self.not_case_ending_change
        self.number_of_changes = self.case_ending_change + self.not_case_ending_change
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(
            os.path.join(dir_path, "test_sentences.txt"), encoding="utf8"
        ) as file:
            self.content = file.read()

    def test_der_case_and_not_case_ending(self):
        _, text, haraqat = extract_haraqat(self.content)
        assert self.number_of_changes <= len(haraqat)
        haraqat_indices = list(range(len(haraqat)))
        case_ending_indices = get_case_ending_indices_from_un_diacritized_txt(text)

        case_ending_map = {}
        for i in case_ending_indices:
            case_ending_map[i] = 0

        not_case_ending_indices = [
            index for index in haraqat_indices if case_ending_map.get(index) is None
        ]

        random.shuffle(case_ending_indices)
        for i in range(self.case_ending_change):
            wrong_haraqah = get_different_haraqah(haraqat[case_ending_indices[i]])
            haraqat[case_ending_indices[i]] = wrong_haraqah

        random.shuffle(not_case_ending_indices)
        for i in range(self.not_case_ending_change):
            wrong_haraqah = get_different_haraqah(haraqat[not_case_ending_indices[i]])
            haraqat[not_case_ending_indices[i]] = wrong_haraqah

        predicted_content = combine_txt_and_haraqat(text, haraqat)

        result = calculate_der(self.content, predicted_content)
        result_should_be = calculate_rate(
            len(haraqat) - self.number_of_changes, self.number_of_changes
        )
        self.assertEqual(result_should_be, result)

        result = calculate_der(self.content, predicted_content, case_ending=False)
        result_should_be = calculate_rate(
            len(haraqat) - len(case_ending_indices), self.not_case_ending_change
        )
        self.assertEqual(result_should_be, result)
