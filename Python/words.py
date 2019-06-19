from urllib.request import urlopen


def fetch_words():
    with urlopen('http://sixty-north.com/c/t.txt') as story:
        story_words = []
        for line in story:
            line_words = line.decode('utf-8').split()
            for word in line_words:
                story_words.append(word)

    print(story_words)


print(__name__)
# When called as script ($ python words.py), execute fetch_words function of words module
if __name__ == '__main__':
    fetch_words()
