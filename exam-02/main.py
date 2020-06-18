from trie import Trie
import string
from typing import List, Tuple
from autocorrect import NorvigAutoCorrecter


def clean_text(text: str, strip_punctuation=True) -> str:
    """Clean text"""

    text = text.lower().strip()

    if strip_punctuation:
        text = text.translate(str.maketrans('', '', string.punctuation))

    return text


def make_trie(cleaned_text: str) -> Trie:
    """Make trie from cleaned text"""

    words = cleaned_text.split()

    # Trie object
    t = Trie()

    # Construct trie
    for word in words:
        t.insert(word)

    return t


def autocomplete(tree: Trie, prefix: str, n: int = 5) -> List[Tuple[str, int]]:
    """Autocomplete wrapper"""

    possible_words = tree.get_children_leaves(prefix)
    words = sorted(possible_words, key=lambda t: -t[1])[:n]
    return [w[0] for w in words]


def autocorrect(tree: Trie, prefix: str, n: int = 5):
    """Autocorrect wrapper"""

    possible_words = correcter.edits1(prefix)
    words_intersection = [(prefix, tree.search(prefix).word_count) for prefix in possible_words]
    words = list(filter(lambda data: data[1] > 0, words_intersection))

    return sorted(words, key=lambda t: -t[1])[:n]


if __name__ == '__main__':
    with open('sample_text.txt') as f:
        text = f.read()

    cleaned_text = clean_text(text, strip_punctuation=True)

    trie = make_trie(cleaned_text)

    # Search for words and print their word count
    print('Word count:')
    for word in ['the', 'their', 'these', 'tha']:
        print(f'{word} -> {trie.search(word).word_count}')

    # Autocomplete
    autocomplete_words = autocomplete(trie, 'th', n=5)
    print('\nAutocomplete:')
    print(autocomplete_words)

    # Autocorrect
    correcter = NorvigAutoCorrecter(cleaned_text)

    autocorrect_words = autocorrect(trie, 'th', n=5)
    print('\nAutocorrect:')
    print(autocorrect_words)
