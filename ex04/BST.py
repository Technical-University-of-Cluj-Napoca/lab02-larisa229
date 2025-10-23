import urllib.request


class Node:
    def __init__(self, word):
        self.word = word
        self.left = None
        self.right = None


class BST:
    def __init__(self, source, file=False, url=False):

        if file and url:
            raise ValueError("Cannot set both file and url to True.")

        if file:
            with open(source, "r", encoding="utf-8") as f:
                words = [line.strip() for line in f if line.strip()]
        elif url:
            response = urllib.request.urlopen(source)
            words = [line.decode("utf-8").strip() for line in response if line.strip()]
        else:
            raise ValueError("Must specify either file=True or url=True")

        words.sort()

        self.root = self._build_bst(words)

    def _build_bst(self, words):
        if not words:
            return None
        mid = len(words) // 2
        node = Node(words[mid])
        node.left = self._build_bst(words[:mid])
        node.right = self._build_bst(words[mid + 1:])
        return node

    def autocomplete(self, prefix):
        results = []
        self._collect(self.root, prefix, results)
        return results

    def _collect(self, node, prefix, results):
        if node is None:
            return

        if node.word >= prefix:
            self._collect(node.left, prefix, results)

        if node.word.startswith(prefix):
            results.append(node.word)

        if node.word <= prefix + chr(255):
            self._collect(node.right, prefix, results)
