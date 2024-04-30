import nltk
import string
from collections import deque
from nltk.corpus import wordnet

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        # Check if the word exists in WordNet
        return bool(wordnet.synsets(word))

    def suggestions(self, word, max_distance=1):
        suggestions = set()
        queue = deque([(self.root, word, "", max_distance)])

        while queue:
            node, remaining, candidate, distance = queue.popleft()

            if not remaining and node.is_end_of_word:
                suggestions.add(candidate)

            if not remaining:  # Handle empty remaining string
                continue

            if distance == 0:
                continue

            for char, child_node in node.children.items():
                if char == remaining[0]:
                    queue.append((child_node, remaining[1:], candidate + char, distance))
                else:
                    queue.append((child_node, remaining[1:], candidate + char, distance - 1))
                    queue.append((child_node, remaining, candidate + char, distance - 1))

        return suggestions

def build_trie_from_word_list(word_list):
    trie = Trie()
    for word in word_list:
        trie.insert(word.lower())
    return trie

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def main():
    # Initialize NLTK and download WordNet
    nltk.download('wordnet')

    # Build Trie from NLTK words corpus (optional)
    # nltk.download('words')
    # word_list = set(nltk.corpus.words.words())
    # trie = build_trie_from_word_list(word_list)

    trie = Trie()

    while True:
        text = input("Enter text (press Enter to exit): ")
        if not text:
            break

        # Remove punctuation from the text
        text = text.translate(str.maketrans('', '', string.punctuation))

        words = text.split()
        suggestions = {}
        for word in words:
            # Ignore numbers
            if word.isdigit():
                continue

            # Ignore uppercase words and correctly spelled words
            if wordnet.synsets(word.lower()):
                continue

            # Generate suggestions using Levenshtein distance
            sug = {w for w in wordnet.words() if levenshtein_distance(word, w) <= 1}
            if sug:  # Check if suggestions exist
                suggestions[word] = sug

        if not suggestions:
            print("No misspelled words found.")
        else:
            print("Misspelled words found with suggestions:")
            for word, sug in suggestions.items():
                print(f"- {word}: Suggestions - {', '.join(sug)}")

    print("Spell checking session ended.")

if __name__ == "__main__":
    main()
