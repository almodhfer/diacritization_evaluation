import random
from typing import  List
import unittest
import os

from util import (
    calculate_rate,
    combine_txt_and_haraqat,
    count_diacritics,
    extract_haraqat,
    get_case_ending_indices_from_un_diacritized_txt,
    get_different_haraqah,
    get_word_without_case_ending,
)
from wer import calculate_wer


class WERTest(unittest.TestCase):
    """Test Word Error Rate with and without Case Ending

    This is done by  changing  diacritics of random words and checking wether the
    WER function outputs align with the changes that we made.

    """

    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(
            os.path.join(dir_path, "test_sentences.txt"), encoding="utf8"
        ) as file:
            self.content = file.read()

    def test_wer(self):
        words = self.content.split()
        n_changes = random.randint(1000, 3000)
        words, _ = self.change_n_random_words(n_changes, words)
        predicted_content = " ".join(words)
        result = calculate_wer(self.content, predicted_content, include_non_arabic=True)
        result_should_be = calculate_rate(len(words) - n_changes, n_changes)
        self.assertEqual(result_should_be, result)

    def test_wer_not_case_ending_last_char_should_not_be_calculated(self):
        n_changes = random.randint(500, 2000)
        words = self.content.split()
        words, _ = self.change_n_random_words_last_char(n_changes, words)
        predicted_content = " ".join(words)
        result = calculate_wer(
            self.content, predicted_content, case_ending=False, include_non_arabic=True
        )
        result_should_be = 0.0
        self.assertEqual(result_should_be, result)

    def test_wer_only_core_word_change(self):
        n_changes = random.randint(500, 2000)
        words = self.content.split()
        words, _ = self.change_n_random_core_word(n_changes, words)
        predicted_content = " ".join(words)
        result = calculate_wer(
            self.content, predicted_content, case_ending=True, include_non_arabic=True
        )
        result_should_be = calculate_rate(
            len(words) - n_changes,
            n_changes,
        )
        self.assertEqual(result_should_be, result)

        result = calculate_wer(
            self.content, predicted_content, case_ending=False, include_non_arabic=True
        )
        result_should_be = calculate_rate(len(words) - n_changes, n_changes)
        self.assertEqual(result_should_be, result)

    def test_both_wer_case_and_not_case_ending(self):
        last_chart_changes = random.randint(500, 2000)
        core_word_changes = random.randint(500, 2000)
        total_change = last_chart_changes + core_word_changes
        words = self.content.split()
        words, changed_idxs = self.change_n_random_words_last_char(
            last_chart_changes, words
        )

        words, changed_idxs2 = self.change_n_random_core_word(
            core_word_changes, words, except_idxs=changed_idxs, shuffle=False
        )

        assert len(changed_idxs) + len(changed_idxs2) == total_change

        predicted_content = " ".join(words)
        wer_case_ending = calculate_wer(
            self.content, predicted_content, case_ending=True, include_non_arabic=True
        )
        wer_case_ending_should_be = calculate_rate(
            len(words) - total_change, total_change
        )
        self.assertEqual(wer_case_ending_should_be, wer_case_ending)

        wer_not_case_ending = calculate_wer(
            self.content, predicted_content, case_ending=False, include_non_arabic=True
        )
        wer_not_case_ending_should_be = calculate_rate(
            len(words) - core_word_changes, core_word_changes
        )
        self.assertEqual(wer_not_case_ending_should_be, wer_not_case_ending)

    def change_n_random_words(
        self,
        n: int,
        words: List[str],
        except_idxs: List[int] = None,
        shuffle: bool = True,
    ):
        word_indices = list(range(len(words)))
        if shuffle:
            random.shuffle(word_indices)
        changed_idxs = []

        idx = 0
        count = 0
        while count < n and idx < len(word_indices):
            index = word_indices[idx]
            idx += 1

            if except_idxs and index in except_idxs:
                continue

            _, word_chars, word_diacritics = extract_haraqat(words[index])

            rand: int = random.randint(0, len(word_diacritics) - 1)
            word_diacritics[rand] = get_different_haraqah(word_diacritics[rand])
            words[index] = combine_txt_and_haraqat(word_chars, word_diacritics)

            changed_idxs.append(index)

            count += 1

        assert count == n

        return words, changed_idxs

    def change_n_random_core_word(
        self,
        n: int,
        words: List[str],
        except_idxs: List[int] = None,
        shuffle: bool = True,
    ):
        word_indices = list(range(len(words)))

        if shuffle:
            random.shuffle(word_indices)

        changed_idxs = []
        idx = 0
        count = 0

        while count < n and idx < len(word_indices):
            index = word_indices[idx]
            word = words[index]
            idx += 1

            if except_idxs and index in except_idxs:
                continue

            if count_diacritics(words[index], skip_count_equal=2) < 2:
                continue

            _, word_chars, word_diacritics = extract_haraqat(words[index])

            indices = get_case_ending_indices_from_un_diacritized_txt(word_chars)

            if len(indices) == 1:
                choices = [
                    val for val in range(len(word_diacritics)) if val != indices[-1]
                ]
                rand = random.choice(choices)
            else:
                rand = random.randint(0, len(word_diacritics) - 2)

            rand = 0

            word_diacritics[rand] = get_different_haraqah(word_diacritics[rand])
            words[index] = combine_txt_and_haraqat(word_chars, word_diacritics)

            assert get_word_without_case_ending(
                words[index]
            ) != get_word_without_case_ending(word)

            changed_idxs.append(index)

            count += 1

        assert count == n

        return words, changed_idxs

    def change_n_random_words_last_char(
        self,
        n: int,
        words: List[str],
        except_idxs: List[int] = None,
        shuffle: bool = True,
    ):

        word_indices = list(range(len(words)))

        if shuffle:
            random.shuffle(word_indices)

        changed_idxs = []

        idx = 0
        count = 0
        while count < n and idx < len(word_indices):
            index = word_indices[idx]
            idx += 1
            if except_idxs and index in except_idxs:
                continue

            word = words[index]
            _, word_chars, word_diacritics = extract_haraqat(words[index])

            if count_diacritics(words[index], skip_count_equal=2) < 2:
                continue

            indices = get_case_ending_indices_from_un_diacritized_txt(word_chars)

            if len(indices) != 1:
                continue

            last_idx = indices[-1]

            word_diacritics[last_idx] = get_different_haraqah(word_diacritics[last_idx])
            words[index] = combine_txt_and_haraqat(word_chars, word_diacritics)

            changed_idxs.append(index)

            count += 1

        assert count == n

        return words, changed_idxs
