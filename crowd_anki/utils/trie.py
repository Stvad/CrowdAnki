from pygtrie import Trie


def keys_without_children(trie: Trie):
    result = []

    def childless_collector(key_transformer, path, children, _=None):
        if not list(children):
            result.append(key_transformer(path))

    trie.traverse(childless_collector)
    return result
