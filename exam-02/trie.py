from typing import List, Tuple


class TrieNode:
    """Trie node class"""

    def __init__(self):
        self.children = {}

        # isEndOfWord is True if node represent the end of the word
        self.word_count = 0


class Trie:
    """Trie data structure class"""

    def __init__(self):
        self.root = self.get_node()

    @staticmethod
    def get_node():
        """Returns new trie node"""
        return TrieNode()

    def insert(self, prefix: str):
        """Inserts value into trie (add word_count)"""
        leaf = self.root
        for level in range(len(prefix)):
            letter = prefix[level]

            # if current character is not present
            if letter not in leaf.children:
                leaf.children[letter] = self.get_node()
            leaf = leaf.children[letter]

            # mark last node as leaf
        leaf.word_count += 1

    def search(self, prefix: str) -> TrieNode:
        """Search value in the trie. Return leaf"""
        leaf = self.root
        for level in range(len(prefix)):
            letter = prefix[level]

            if letter not in leaf.children:
                return self.get_node()
            leaf = leaf.children[letter]

        if leaf is not None:
            return leaf
        return self.get_node()

    def _get_children_leaves_recursively(self, prefix: str, leaf: TrieNode) -> List[Tuple[str, int]]:
        leaves = []
        if leaf.children:
            for next_letter in leaf.children:
                child_leaves = self._get_children_leaves_recursively(prefix + next_letter, leaf.children[next_letter])
                leaves.extend(child_leaves)
        else:
            leaves.append((prefix, leaf.word_count))
        return leaves

    def get_children_leaves(self, prefix: str):
        initial_leaf = self.search(prefix)
        if not initial_leaf.children:
            return []
        return self._get_children_leaves_recursively(prefix, initial_leaf)
