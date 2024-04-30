# FinalCSC310
The final project for CSC310

Contents of the Repository:

FinalProjSpellChecker.py - The final version of the Spell Checker file, which is the primary submission for the Final Project (Homework 7)
corpus.txt - The text file that contains the training data for the N-gram Language Model
largedict.txt - The text file that contains the dictionary, which fills the Trie
SpellChecker.py - First version of the Spell Checker file, which was what was submitted for Homework 5 
UpdatedSC.py - Second iteration of the Spell Checker file, which is a secondary submission for the Final Project (Homework 7)

For the Final Project related files:

FinalProjSpellChecker.py:
- This version has 3 different modes for spell checking, which are selected through entering a single character correlating to the mode you want.
  Options:
    s - use only the suggestions retrieved through BFS
    n - use only the N-gram Language Model for spell checking
    b - use the N-gram on suggestions
  With these options implemented, I felt it was best to only have the project allow one word submitted at a time to be spell checked, as it would allow for me to easily see if each mode was working like I expected. Along with this, having the ability to have the spell-checked words be sent to a file wouldn't have too much use, especially since my main focus was on the spell checking modes themselves rather than the ability to save the words.

UpdatedSC.py:
- This version was my first go at the final project. My original goals for this version was to improve the error detection and implement the ability to have it correct a string with multiple words, one word at a time. I then added the ability to modify your overall string. Upon exiting of the program, you are then asked to save the text to a file, which you can do so by giving typing [filename].[ext] and pressing Enter.
