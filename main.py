import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = "<Whatever you want to name the folder>"
HOMEPAGE = "<The name of the homepage>"
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
# You can use any number of threads that your operating system can handle, More Threads = More Speed
NUMBER_OF_THREADS = 4
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


# Create worker thread (will die when main exists
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        thread = threading.Thread(target=work)
        thread.daemon = True
        thread.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + " links in the queue")
        create_jobs()


create_workers()
crawl()