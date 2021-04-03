"""
Util Test Module
"""
import unittest
import os

from diacritization_evaluation.util import (
    extract_haraqat,
    get_case_ending_indices_from_un_diacritized_txt,
    combine_txt_and_haraqat,
    get_different_haraqah,
    get_word_without_case_ending
)
from constants import ALL_POSSIBLE_HARAQAT


class UtilTest(unittest.TestCase):
    """Testing several functions used for during DER and WER evaluations"""

    def setUp(self):

        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(
            os.path.join(dir_path, "test_sentences.txt"), encoding="utf8"
        ) as file:
            self.content = file.read()

    def test_haraqat_extraction(self):
        _, text, haraqat = extract_haraqat(self.content)
        combined_text = combine_txt_and_haraqat(text, haraqat)

        should_be_equal = True
        for char1, char2 in zip(combined_text, self.content):
            if char1 != char2:
                should_be_equal = False
                break

        self.assertTrue(should_be_equal)

    def test_case_ending_indices(self):
        txt = (
            "الْمَسْأَلَةُ السَّابِعَةُ : فَضْلُ الْفَاتِحَةِ : لَيْسَ فِي أُمِّ الْقُرْآنِ حَدِيثٌ يَدُلُّ عَلَى "
            "فَضْلِهَا إلَّا حَدِيثَانِ : أَحَدُهُمَا : حَدِيثُ : { قَسَمْتُ الصَّلَاةَ بَيْنِي وَبَيْنَ عَبْدِي "
            "نِصْفَيْنِ . "
        )
        _, text, haraqah = extract_haraqat(txt)
        indices = get_case_ending_indices_from_un_diacritized_txt(text)
        # correct
        expected_out = "ةةلةسيمنثلىااناثتةينين"
        self.assertTrue(len(indices), len(expected_out))

        should_be = True
        i = 0
        for index in indices:
            if expected_out[i] != text[index]:
                should_be = False
                break

            i += 1
        self.assertTrue(should_be)

    def test_get_different_haraqah(self):
        should_be_true = True

        for haraqah in ALL_POSSIBLE_HARAQAT.keys():
            different_h = get_different_haraqah(haraqah)
            if haraqah == different_h:
                should_be_true = False
                break
        self.assertTrue(should_be_true)
    
    def test_word_without_case_ending(self):
        word1 = 'الْأَصَحِّ'
        word1_expected = 'الْأَصَ'

        word2 = 'الْأَصَحِّ:'
        word2_expected = 'الْأَصَ:'

        word3 = 'الْأَصَحِّ '
        word3_expected = 'الْأَصَ '


        output_word1 = get_word_without_case_ending(word1)
        output_word2 = get_word_without_case_ending(word2)
        output_word3 = get_word_without_case_ending(word3)

        assert output_word1 == word1_expected
        assert output_word2 == word2_expected
        assert output_word3 == word3_expected
      
