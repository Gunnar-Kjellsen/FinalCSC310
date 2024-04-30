import nltk
import string
from collections import deque
from nltk.corpus import wordnet, stopwords

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
        # Check if the word exists in WordNet and is an open-class word
        return bool(wordnet.synsets(word)) and wordnet.synsets(word)[0].pos() in ['n', 'v', 'a', 'r']

    def print_trie(self, node=None, prefix=""):
        if node is None:
            node = self.root
        for char, child_node in node.children.items():
            if child_node.is_end_of_word:
                print(prefix + char)
            self.print_trie(child_node, prefix + char)

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

            # Traverse the trie for suggestions
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

def build_trie_from_text_file(file_path):
    trie = Trie()
    with open(file_path, 'r') as file:
        for line in file:
            word = line.strip() # Remove leading/trailing whitespace
            trie.insert(word.lower()) # Insert lowercase word into the trie
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

def correct_spelling(word, suggestions):
    print(f"Original: {word}")
    print("Suggestions:")
    for i, sug in enumerate(suggestions, start=1):
        print(f"{i}. {sug}")
    choice = input("Enter your choice (or press Enter to keep original): ")
    if choice.isdigit() and 1 <= int(choice) <= len(suggestions):
        return suggestions[int(choice) - 1]
    elif choice.strip():
        return choice.strip()
    else:
        # Add the corrected word to the user-modified trie regardless of whether it's in word_list
        if word.lower() != choice.lower() and choice.lower() not in word_list:
            user_modified_words_trie.insert(choice.lower())
        return word


def main():
    # Initialize NLTK and download WordNet
    nltk.download('wordnet')
    nltk.download('stopwords')

    # Build Trie from NLTK words corpus (optional)
    nltk.download('words')
    word_list = set(nltk.corpus.words.words())

    word_list.update(stopwords.words('english'))
    trie = build_trie_from_word_list(word_list)

    user_modified_words_trie = Trie()  # Trie for user-modified words

    corrected_text = ""

    while True:
        text = input('''Enter text (press Enter to exit,
'c' to check for corrections,
'v' to view the current text,
'd' to print out user-made Trie,
'm' to modify the current text): ''')
        if text == "":
            break
        elif text.lower() == "c":
            # Correct misspelled words interactively
            words = corrected_text.split()
            corrected_words = []
            for word in words:
                word_stripped = word.strip(string.punctuation)  # Strip punctuation from word
                if not wordnet.synsets(word_stripped.lower()):
                    suggestions = user_modified_words_trie.suggestions(word_stripped.lower(), max_distance=2)
                    # Check user-modified trie first
                    if not suggestions:
                        suggestions = trie.suggestions(word_stripped.lower(), max_distance=2)
                    # Skip suggesting corrections if the word is already found in the word database
                    if word_stripped.lower() not in word_list:
                        corrected_word = correct_spelling(word_stripped, suggestions)
                        corrected_words.append(corrected_word)
                        # Add the corrected word to the user-modified trie only if it's not already present
                        if corrected_word.lower() not in word_list:
                            user_modified_words_trie.insert(corrected_word.lower())
                    else:
                        corrected_words.append(word)
                else:
                    corrected_words.append(word)
            corrected_text = " ".join(corrected_words)
        elif text.lower() == "v":
            print("Current Text:")
            print(corrected_text)
        elif text.lower() == "m":
            print("Current Text:")
            print(corrected_text)
            user_input = input("Modify the current text (press Enter to keep it as is): ")
            if user_input.strip():  # If user input is not empty, update the corrected text
                corrected_text = user_input.strip()
        elif text.lower() == "d":
            user_modified_words_trie.print_trie()
        else:
            corrected_text += " " + text.rstrip()  # Add space before adding the new text

    print("Your corrected text:")
    print(corrected_text)

    # Ask if user wants to save the corrected text to a file
    save_file = input("Do you want to save this text to a file? (y/n): ")
    if save_file.lower() == "y":
        file_name = input("Enter file name (including extension): ")
        with open(file_name, "w") as file:
            file.write(corrected_text)

if __name__ == "__main__":
    main()
