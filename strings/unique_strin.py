def get_unique_string(word):
    result = word[0]
    for i in range(1, len(word)):
        if result[-1] != word[i]:
            result += word[i]
    return result.strip()

print(get_unique_string('AAABBBBCCCABCCD'))