import string
from collections import deque
import numpy as np

options = """Options:
s - use only the suggestions retrieved through BFS
n - use only the N-gram Language Model for spell checking
b - use the N-gram on suggestions
"""

# Define the N-Gram Class
class NGramLanguageModel:
    def __init__(self, n=3):
        self.n = n
        self.ngrams = {}
        self.total_count = 0

    def train(self, corpus):
        # Create n-grams from the corpus
        for i in range(len(corpus) - self.n + 1):
            ngram = tuple(corpus[i:i+self.n])
            self.ngrams[ngram] = self.ngrams.get(ngram, 0) + 1
            self.total_count += 1

    def probability(self, ngram):
        return self.ngrams.get(ngram, 0) / self.total_count

    def suggestions_with_language_model(self, suggestions, context):
        # Calculate probabilities for each suggestion
        suggestion_probs = [(word, self.probability(context + (word,))) for word in suggestions]
        # Sort suggestions by probability (highest to lowest)
        sorted_suggestions = sorted(suggestion_probs, key=lambda x: x[1], reverse=True)
        return sorted_suggestions

# Define Trie data structure
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
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def suggestions(self, word, max_distance=2):
        suggestions = set()
        queue = deque([(self.root, word, "", max_distance)])

        while queue:
            node, remaining, candidate, distance = queue.popleft()

            if not remaining and node.is_end_of_word:
                suggestions.add(candidate)

            if distance == 0:
                continue

            # Check if there are remaining characters
            if remaining:
                # Handle single-letter substitution
                for char, child_node in node.children.items():
                    if char == remaining[0]:
                        queue.append((child_node, remaining[1:], candidate + char, distance))
                    else:
                        queue.append((child_node, remaining[1:], candidate + char, distance - 1))
            else:
                # Check for suggestions when remaining string is empty
                for char, child_node in node.children.items():
                    if node.children[char].is_end_of_word:
                        suggestions.add(candidate + char)

            # Check for double-letter substitution
            for char, child_node in node.children.items():
                if len(remaining) > 1 and char == remaining[1]:
                    queue.append((child_node, remaining[1:], candidate + char, distance - 1))
                    queue.append((child_node, remaining[2:], candidate + char, distance - 1))

        return suggestions

# Function to correct misspelled words
def correct_spelling_suggestions(word, suggestions):
    print(f"Original: {word}")
    print("Suggestions:")

    i = 1
    for sug in suggestions:
        print(f"{i}- {sug}")
        i = i + 1
    choice = input("Enter your choice (or press Enter to keep the original): ")
    if choice.strip():
        return choice.strip()
    else:
        return word

# Function to correct spelling using Trie, N-gram model, or both
def correct_spelling(word, trie, ngram_model, mode):
    # Step 1: Search Trie
    if trie.search(word):
        return word
    
    # Step 2: Calculate suggestions based on Trie
    suggestions = trie.suggestions(word, max_distance=2)

    # Step 3: Apply custom rules (not implemented here)

    # Step 4: Apply N-gram language model for refinement
    if mode == "n":
        return suggestions
    elif mode == "l":
        refined_suggestions = ngram_model.suggestions_with_language_model(suggestions, context=(word,))
        return refined_suggestions
    elif mode == "b":
        # Combine suggestions from Trie with language model for ranking
        refined_suggestions = ngram_model.suggestions_with_language_model(suggestions, context=(word,))
        return refined_suggestions
    else:
        return suggestions

# Main function
def main():

    # Load training data
    with open("corpus.txt", "r", encoding="utf-8") as file:
        corpus = file.read().split()
    
    # Build Trie from file
    trie = Trie()
    with open("largedict.txt", "r") as file:
        for line in file:
            word = line.strip().lower()
            trie.insert(word)

    # Train N-gram language model
    ngram_model = NGramLanguageModel(n=3)
    ngram_model.train(corpus)

    mode = "b"

    while True:
        word = input("Enter a word (press Enter to exit, 'o' for more options, or select one of the modes): ").strip().lower()
        if not word:
            break
        if word == "o": # View options
            print(options)
            print(f"Your current mode is {'suggestions' if mode == 's' else 'N-gram model' if mode == 'n' else 'N-gram on suggestions' if mode == 'b' else 'N-gram Language Model on suggestions' if mode == 'l' else ''}.")
            continue
        if word in ["s", "n", "b"]: # Change modes
            mode = word
            print(f"You've switched to {'suggestions' if mode == 's' else 'N-gram model' if mode == 'n' else 'N-gram on suggestions' if mode == 'b' else ''}.")
            continue

        # Input word is correct
        if trie.search(word):
            print("Word is spelled correctly.")
            continue

        # Suggestions through BFS
        if mode == "s":
            suggestions = trie.suggestions(word, max_distance=2)
            if suggestions:
                corrected_word = correct_spelling_suggestions(word, suggestions)
                print(f"Corrected word: {corrected_word}")
            else:
                print("No suggestions available.")

        # N-gram only
        elif mode == "n":
            refined_suggestions = ngram_model.suggestions_with_language_model([word], context=())
            if refined_suggestions:
                corrected_word = refined_suggestions[0][0]
                print(f"Corrected word using N-gram model: {corrected_word}")
            else:
                print("No suggestions available.")

        # Suggestions refined with N-gram
        elif mode == "b":
            suggestions = trie.suggestions(word, max_distance=2)
            if suggestions:
                refined_suggestions = ngram_model.suggestions_with_language_model(suggestions, context=(word,))
                if refined_suggestions:
                    corrected_word = refined_suggestions[0][0]
                    print(f"Corrected word using both methods: {corrected_word}")
                else:
                    print("No suggestions available.")
            else:
                print("No suggestions available.")

if __name__ == "__main__":
    main()
