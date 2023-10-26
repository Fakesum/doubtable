from difflib import SequenceMatcher

print(SequenceMatcher(None, "What is A feline tiger", "What is a cat").ratio())