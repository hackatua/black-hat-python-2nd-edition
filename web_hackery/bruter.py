import queue
import requests
import threading
import sys

# Sample dict: https://raw.githubusercontent.com/nathanmyee/SVNDigger/master/SVNDigger/all.txt

AGENT = "Mozilla/5.0 (X11: Lunux x86_64: rv:19.0) Gecko/20100101 Firefox/19.0"
EXTENSIONS = [".php", ".bak", ".orig", ".inc"]
TARGET = "http://testphp.vulnweb.com"
THREADS = 5
WORDLIST = "/home/parrot/Downloads/all.txt"

def get_words(resume=None):
    def extend_words(word):
        if "." in word:
            words.put(f"/{word}")
        else:
            words.put(f"/{word}")
            for extension in EXTENSIONS:
                words.put(f"/{word}{extension}")
    
    with open(WORDLIST) as file:
        raw_words = file.read()

    found_resume = False
    words = queue.Queue()
    for word in raw_words.split():
        if resume is not None:
            if found_resume:
                extend_words(word)
            elif word == resume:
                found_resume = True
                print(f'Resuming wordlist from: {resume}')
        else:
            print(word)        
            extend_words(word)
    return words

def dir_bruter(words: queue.Queue):
    headers = {'User-Agent': AGENT}
    while not words.empty():
        url = f"{TARGET}{words.get()}"
        try:
            response = requests.get(url, headers=headers)
        except requests.exceptions.ConnectionError:
            sys.stderr.write("x")
            sys.stderr.flush()
            continue
        if response.status_code == 200:
            print(f"\nSuccess ({response.status_code}: {url})")
        elif response.status_code == 404:
            sys.stderr.write(".")
            sys.stderr.flush()
        else:
            print(f"{response.status_code} => {url}")

def main():
    words = get_words()
    print("Press return to continue.")
    sys.stdin.readline()
    for _ in range(THREADS):
        thread = threading.Thread(target=dir_bruter, args=(words,))
        thread.start()

if __name__ == "__main__":
    main()