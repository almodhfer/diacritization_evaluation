import unittest

from util import *
from wer import calculate_wer


class WERTest(unittest.TestCase):

    def setUp(self):
        self.content = None
        self.case_ending_change = 2000
        self.not_case_ending_change = 5000
        self.number_of_changes = self.case_ending_change + self.not_case_ending_change
        self.content = ''
        with open('test_sentences.txt', encoding='utf8') as file:
            self.content = file.read()

    def test_wer_both(self):
        words = self.content.split()
        assert len(words) > 0
        word_indices = list(range(len(words)))
        random.shuffle(word_indices)
        not_case_ending_change = self.not_case_ending_change

        i = 0
        while True:
            index = word_indices[i]
            _, w, h = extract_haraqat(words[index])
            if len(h) > 2 and not_case_ending_change > 0:
                rand = random.randint(0, len(h) - 2)
                h[rand] = get_different_haraqah(h[rand])
                words[index] = combine_txt_and_haraqat(w, h)
                not_case_ending_change -= 1
                i += 1
                continue
            h[-1] = get_different_haraqah(h[-1])
            words[index] = combine_txt_and_haraqat(w, h)
            i += 1
            if i == self.number_of_changes:
                break

        predicted_content = ' '.join(words)
        result = calculate_wer(self.content, predicted_content)
        result_should_be = calculate_rate(
            len(word_indices) - self.number_of_changes, self.number_of_changes)
        self.assertEqual(result_should_be, result)
        result = calculate_wer(
            self.content, predicted_content, case_ending=False)
        result_should_be = calculate_rate(len(self.content.split()) - self.not_case_ending_change,
                                          self.not_case_ending_change)
        self.assertEqual(result_should_be, result)
