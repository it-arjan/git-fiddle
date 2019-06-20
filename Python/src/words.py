from urllib.request import urlopen
import sys


def fetch_words(url):
    with urlopen(url) as story:
        story_words = []
        for line in story:
            line_words = line.decode('utf-8').split()
            for word in line_words:
                story_words.append(word)
    return story_words


def print_items(items):
    for item in items:
        print(item)


def main(url):
    words = fetch_words(url)
    print_items(words)


print(__name__)
# When called as script ($ python words.py), execute fetch_words function of words module
if __name__ == '__main__':
    url = sys.argv[1]
    main(url)
