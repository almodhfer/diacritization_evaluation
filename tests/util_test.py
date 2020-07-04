import unittest

from util import *
from constants import all_possible_haraqat

class UtilTest(unittest.TestCase):

    def setUp(self):
        self.content = None
        with open('test_sentences.txt', encoding='utf8') as file:
            self.content = file.read()

    def test_haraqat_extraction(self):
        _, t, h = extract_haraqat(self.content)
        out = combine_txt_and_haraqat(t, h)

        should_be_equal = True
        for c1, c2 in zip(out, self.content):
            if c1 != c2:
                should_be_equal = False
                break

        self.assertTrue(should_be_equal)

    def test_case_ending_indices(self):
        txt = "الْمَسْأَلَةُ السَّابِعَةُ : فَضْلُ الْفَاتِحَةِ : لَيْسَ فِي أُمِّ الْقُرْآنِ حَدِيثٌ يَدُلُّ عَلَى " \
              "فَضْلِهَا إلَّا حَدِيثَانِ : أَحَدُهُمَا : حَدِيثُ : { قَسَمْتُ الصَّلَاةَ بَيْنِي وَبَيْنَ عَبْدِي " \
              "نِصْفَيْنِ . "
        _, t, h = extract_haraqat(txt)
        indices = get_case_ending_indices_from_un_daicritized_txt(t)
        # correct
        out = "ةةلةسيمنثلىااناثتةينين"
        self.assertTrue(len(indices), len(out))

        should_be = True
        i = 0
        for index in indices:
            if out[i] != t[index]:
                should_be = False
                print(out[i], t[index])
                break

            i += 1
        self.assertTrue(should_be)

    def test_get_different_haraqah(self):
        should_be_true = True

        for h in all_possible_haraqat.keys():
            different_h = get_different_haraqah(h)
            if h == different_h:
                should_be_true = False
                break
        self.assertTrue(should_be_true)