# edit test
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_terminal = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_terminal = True

def build_trie_from_file(filename, limit=None):
    trie = Trie()
    current = 0
    with open(filename, 'r') as file:
        for line in file:
            word = line.strip().lower()
            if word:
                trie.insert(word)
            current += 1
            if limit and current == limit:
                break
    return trie

class DAWGNode:
    def __init__(self):
        self.children = {}
        self.is_terminal = False

class DAWG:
    def __init__(self):
        self.root = DAWGNode()
        self.nodes = {}

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = DAWGNode()
            node = node.children[char]
        node.is_terminal = True

    def minimize(self):
        self.minimize_node(self.root)

    def minimize_node(self, node):
        for char, child in node.children.items():
            self.minimize_node(child)
        for char, child in node.children.items():
            child_key = self.get_node_key(child)
            if child_key in self.nodes:
                node.children[char] = self.nodes[child_key]
            else:
                self.nodes[child_key] = child

    def get_node_key(self, node):
        key = (node.is_terminal,)
        key += tuple(sorted((char, self.get_node_key(child)) for char, child in node.children.items()))
        return key

def trie_to_dawg(trie):
    dawg = DAWG()
    def convert(trie_node, dawg_node):
        dawg_node.is_terminal = trie_node.is_terminal
        for char, trie_child in trie_node.children.items():
            dawg_child = DAWGNode()
            dawg_node.children[char] = dawg_child
            convert(trie_child, dawg_child)
    convert(trie.root, dawg.root)
    dawg.minimize()
    return dawg

def build_dawg_from_file(filename, limit=None):
    trie = build_trie_from_file(filename, limit)
    dawg = trie_to_dawg(trie)
    return dawg


def is_word_in_dawg(word, dawg):
    node = dawg.root
    for char in word:
        if char not in node.children:
            return False
        node = node.children[char]
    return node.is_terminal