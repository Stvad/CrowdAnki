from functional import seq
from pygtrie import Trie


def keys_without_children(trie: Trie):
    result = []

    def childless_collector(key_transformer, path, children, _=None):
        if not list(children):
            result.append(key_transformer(path))

    trie.traverse(childless_collector)
    return result


def remove_children_of(trie: Trie, keys):
    def delete_key(key):
        del trie[key]

    seq(keys) \
        .filter(lambda key: key in trie) \
        .flat_map(lambda key: trie.keys(prefix=key)) \
        .filter(lambda key: key not in keys) \
        .for_each(delete_key)
