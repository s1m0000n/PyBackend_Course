from multiprocessing import Process, Queue
from configparser import ConfigParser
import socket
import requests
import sys
import json
from bs4 import BeautifulSoup
import signal
import os


def process_url(url: str, n: int, connection) -> None:
    """
    Loads contents of a certain url, selects top n words, sends
    :param url: Url to process
    :param n: Number of top words to send
    :param connection: Object with method .send()
    :return: None, it's a procedure
    """
    r = requests.get(url, allow_redirects=True)
    soup = BeautifulSoup(r.content, 'html.parser')
    text = soup.get_text()
    text = text.strip()
    top_n = text.split(' ')[:n]
    resp = {'url':url, 'top':top_n}
    connection.send(json.dumps(resp, ensure_ascii=False).encode(sys.stdout.encoding))


def queue_processing(process: callable, process_other_args: tuple,
                     urls: Queue, stop_cmd: str = '@STOP', results: Queue = None):
    tasks_done = 0
    while True:
        url = urls.get()
        if url == stop_cmd and results is not None:
            results.put(tasks_done)
            urls.put(stop_cmd)
            process_other_args[1].close()
            return
        else:
            process(url, *process_other_args)
            tasks_done += 1


def run_server():
    config_path = 'server_config.conf'
    config = ConfigParser()
    try:
        config.read(config_path)
        workers_n = int(config['settings']['workers_n'])
        top_n = int(config['app']['top_n'])
        stop_cmd = config['settings']['stop_cmd']
        port = int(config['connections']['port'])
    except KeyError:
        raise KeyError(f'Could\'t read some values of {config_path}')
    except ValueError:
        raise TypeError(f'Some of the values in {config_path} are of unexpected type')
    else:
        urls_queue = Queue()
        results_queue = Queue()
        workers = []

    total_urls_processed = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('', port))
        sock.listen()
        while True:
            connection, addr = sock.accept()
            with connection:
                for w in range(workers_n):
                    process = Process(target=queue_processing,
                                      args=(process_url, (top_n, connection), urls_queue, stop_cmd),
                                      kwargs={'results':results_queue})
                    workers.append(process)
                    process.start()

                def sigusr1_handler(signum, frame):
                    print(f'Recieved a {signum} signal, shutting down server')
                    connection.close()
                    sock.close()
                    urls_queue.put(stop_cmd)
                    for process in workers:
                        process.join()
                    total_urls = total_urls_processed + sum(iter(results_queue.get), start=0)
                    print(total_urls)
                    quit()
                    return total_urls_processed
                signal.signal(signal.SIGUSR1, sigusr1_handler)

                while True:
                    data = connection.recv(4096)
                    url = data.decode(sys.stdout.encoding)
                    url = url.replace('\r\n', '')
                    urls_queue.put(url)
                for process in workers:
                    process.join()
                total_urls_processed += sum(iter(results_queue.get), start=0)
                print(total_urls_processed)
    return True


if __name__ == '__main__':
    print(os.getpid())
    run_server()
