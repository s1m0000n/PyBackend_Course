#! /home/s1m00n/PyBackend_Course/'5_Server-Client_App'/venv/bin/python
"""Simple server for morph&semantic analysis of pair of words"""

from configparser import ConfigParser
import sys
import logging as log
import socket
from time import perf_counter
import json
from navec import Navec
from natasha import Doc, MorphVocab, Segmenter, NewsMorphTagger, NewsEmbedding
from scipy.spatial.distance import cosine
import daemon


class TextProcessing:
    """
    Class for semantic similarity and morphological analysis
    """

    def __init__(self):
        self.navec = Navec.load('navec_hudlit_v1_12B_500K_300d_100q.tar')
        self.segmenter = Segmenter()
        self.embeddings = NewsEmbedding()
        self.morph_tagger = NewsMorphTagger(self.embeddings)
        self.morph_vocab = MorphVocab()

    def semantic_sim(self, word1, word2):
        """
        Computation of cosine semantic similarity of word GloVe vectors
        :param word1: First word
        :param word2: Second word
        :return: Coefficient or err str
        """
        try:
            return cosine(self.navec[word1.lower()], self.navec[word2.lower()])
        except KeyError:
            return "Don't have vector for one/two of the words"

    def process(self, word1, word2):
        """
        Morph&Semantic analysis
        :param word1: First word
        :param word2: Second word
        :return: Morph&Semantic analysis dict
        """
        doc1, doc2 = tuple(map(lambda w: Doc(w.strip()), (word1, word2)))
        for doc in (doc1, doc2):
            doc.segment(self.segmenter)
            doc.tag_morph(self.morph_tagger)
            for token in doc.tokens:
                token.lemmatize(self.morph_vocab)
        res = {f'Word {i}': {
            'Original': doc.tokens[0].text,
            'Lemma': doc.tokens[0].lemma,
            'Part of speech': doc.tokens[0].pos,
            'Features': doc.tokens[0].feats
        } for i, doc in enumerate((doc1, doc2))}
        res['Semantic Similarity'] = self.semantic_sim(doc1.tokens[0].lemma, doc2.tokens[0].lemma)
        return res


def build_xml(data_dict):
    """
    Dict -> xml
    """
    res = ''
    for key, value in data_dict.items():
        res += (lambda tag_name, inner: f'<{tag_name}>{inner}</{tag_name}>\n') \
            (key, str(value) if not isinstance(value, dict) else build_xml(value))
    return res


def main(config):
    """Processing requests"""
    analysis = TextProcessing()
    try:
        port = int(config['main']['port'])
    except KeyError:
        port = 5000
        log.warning(f'Port number is not specified, using {port}')
    except:
        log.critical(f"Couldn't bind socket at localhost:{config['main']['port']}")
        raise ConnectionError
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('', port))
        sock.listen()
        log.info(f"Now listening on localhost:{config['main']['port']}")
        num_connections = 0
        try:
            max_connections = int(config['main']['max_connections'])
        except KeyError:
            max_connections = 1000
        while num_connections <= max_connections:
            num_connections += 1
            conn, addr = sock.accept()
            with conn:
                log.info(f'Connected {addr}')
                request_counter = 0
                connection_tic = perf_counter()
                while True:
                    if not (data := conn.recv(1024)):
                        break
                    request_counter += 1
                    data = data.decode(sys.stdout.encoding)
                    log.info(f'Request #{request_counter}: {data}')
                    request_tic = perf_counter()
                    args = dict([tuple(arg.split('=')) for arg in data.split('&')])
                    try:
                        result_format = args['format']
                    except KeyError:
                        log.warning(f'Expected to get format request arg,'
                                    f' but not in request {data}; using JSON')
                        result_format = 'json'
                    processed = analysis.process(args['w1'], args['w2'])
                    response = json.dumps(processed, ensure_ascii=False) \
                        if result_format == 'json' else build_xml(processed)
                    conn.send(response.encode(sys.stdout.encoding))
                    request_toc = perf_counter()
                    log.info(f'Responded in {request_toc - request_tic:0.2f} sec')
                    connection_toc = perf_counter()
                    log.info(f'Total connection time: {connection_toc - connection_tic:0.2f} sec')
                    log.info(f'Total requests: {request_counter}')
            log.info(f'Connection with {addr} closed')


def keyboard_interrupt_manager():
    """Graceful shutdown"""
    if (answer := input('\nShut the server down? [y/n]: ').lower()) == 'y':
        log.info('Server shutdown')
        exit()
    elif answer == 'n':
        log.warning('Cancelled shutting down')
        run_server()
    else:
        print('Please, try again')
        keyboard_interrupt_manager()


def launcher():
    """Configuring log, starting server"""
    config = ConfigParser()
    try:
        config.read(sys.argv[1])
    except IndexError:
        print('Expected config.conf as a 1st arg\nNow quitting')
        raise KeyError
    try:
        log.basicConfig(filename=config['main']['log_path'], filemode='a',
                        format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                        level=log.DEBUG)
    except KeyError:
        print(f"Failed to open logging file\n"
              f"Logging to stdout\n"
              f"Look at config file at {sys.argv[1]}")
        log.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                        level=log.DEBUG, stream=sys.stdout)
    try:
        mode = config['main']['mode']
    except KeyError:
        log.warning(f'No mode declaration in {sys.argv[1]}, using default - regular')
        mode = 'regular'

    if mode == 'daemon':
        log.info('Server started in daemon mode')
        with daemon.DaemonContext():
            main(config)
    elif mode == 'regular':
        log.info('Server started in regular mode')
        main(config)
    else:
        log.critical(f"Unexpected mode value in config {sys.argv[1]}, "
                     f"mode = {config['main']['mode']}")
        raise ValueError


def run_server():
    try:
        launcher()
    except KeyboardInterrupt:
        keyboard_interrupt_manager()
    except:
        log.critical('Critical error')
        exit()
    else:
        log.info('Server shutdown')

if __name__ == '__main__':
    run_server()
