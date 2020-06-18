import unittest
from main import *


class TestCleaner(unittest.TestCase):
    def setUp(self):
        self.text = ', '.join(['the', 'their', 'these', 'tha'])

    def test_clean_with_punc_strip(self):
        result = clean_text(self.text, strip_punctuation=True)
        expected = 'the their these tha'

        self.assertEqual(result, expected)

    def test_clean_without_punc_strip(self):
        result = clean_text(self.text, strip_punctuation=False)
        expected = 'the, their, these, tha'

        self.assertEqual(result, expected)


class TestTrie(unittest.TestCase):
    def setUp(self):
        self.words = 'the their these tha'

        self.trie = Trie()
        for word in self.words.split():
            self.trie.insert(word)

    def test_exising_word(self):
        result = self.trie.search('the').word_count
        expected = 1

        self.assertEqual(result, expected)

    def test_non_exising_word(self):
        result = self.trie.search('someunknownword').word_count
        expected = 0

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
