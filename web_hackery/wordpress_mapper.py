import contextlib
import os
import queue
import requests
import sys
import threading
import time

# Download wordpress from https://wordpress.org/download/

FILTERED = [".jpg", ".gif", ".png", ".css"]
TARGET = "http://boodelyboo.com/wordpress"
THREADS = 10

answers = queue.Queue()
web_paths = queue.Queue()

def gather_paths():
    for root, _, files in os.walk("."):
        for file in files:
            if os.path.splitext(file)[1] in FILTERED:
                continue
            path = os.path.join(root, file)
            if path.startswith("."):
                path = path[1:]
            print(path)
            web_paths.put(path)

def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = f"{TARGET}{path}"
        time.sleep(2)
        response = requests.get(url)
        if response.status_code == 200:
            answers.put(url)
            sys.stdout.write("+")
        else:
            sys.stdout.write("x")
        sys.stdout.flush()
    
def run():
    threads: list = list()
    for i in range(THREADS):
        print(f"Spawning thread {i}")
        thread = threading.Thread(target=test_remote)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

@contextlib.contextmanager
def chdir(path):
    this_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(this_dir)

def main():
    with chdir("/home/parrot/Downloads/wordpress"):
        gather_paths()
    input("Press return to continue.")

    run()
    with open("myanswers.txt", "w") as file:
        while not answers.empty():
            file.write(f"{answers.get()}\n")
    print("Done")

if __name__ == "__main__":
    main()