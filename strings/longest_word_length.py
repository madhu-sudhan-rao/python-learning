def longest_word_length(sentence):
    length = 0
    words = sentence.split()
    for word in words:
        if length < len(word):
            length = len(word)
        
    return length

print(longest_word_length("The quick brown fox jumps over the lazy dog"))