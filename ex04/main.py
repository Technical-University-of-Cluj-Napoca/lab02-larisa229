from BST import BST
from search_engine import search_loop

if __name__ == '__main__':
    bst = BST('https://raw.githubusercontent.com/dwyl/english-words/refs/heads/master/words.txt', url=True)
    search_loop(bst)
