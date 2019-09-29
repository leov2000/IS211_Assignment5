from request import Request
from server import Server
from queue import Queue
import urllib.request as urllib
import logging
import argparse
import csv
import pprint

def get_data(url):
    csvData = urllib.urlopen(url).read()
    csvPayLoad = csv.reader(csvData.decode('utf-8').splitlines())
    csvResults = [row for row in csvPayLoad]

    return csvResults

def count_down(server):
    while(server.busy()):
        server.tick()

    return True

def cast_to_int(req_list):
    return [[req_num, req_file, int(sec)] for [req_num, req_file, sec] in req_list ]

def create_request_queue(req_list):
    request_queue = Queue()
    casted_list = cast_to_int(req_list)

    for request in casted_list:
        request_obj = Request(request)
        request_queue.enqueue(request_obj)

    return request_queue


def simulateOneServer(request_list):
    request_queue = create_request_queue(request_list)
    request_length = request_queue.size()
    request_server = Server()

    processed_list = []

    while not request_queue.is_empty():

        if not request_server.boot_strapped:
            first_req = request_queue.dequeue()
            request_server.first_request(first_req)
            count_down(request_server)
            processed_list.append(first_req.get_request())
        else:
            next_req = request_queue.dequeue()
            request_server.first_request(next_req)
            count_down(request_server)
            processed_list.append(next_req.get_request())



def main():
    """
    The primary function of this application.

    Parameters:
        None

    Logs:
        An error if the string url is entered incorrectly.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('servers')
    args = parser.parse_args()

    logging.basicConfig(filename='errors.log',
                        level=logging.ERROR, format='%(message)s')
    logging.getLogger('assignment5')

    if args.url:
        try:
            result = get_data(args.url)
            server_num = args.servers
            simulateOneServer(result)
        except (ValueError, urllib.HTTPError):
            print(
                f'Something went wrong, you entered in <{args.url}>, please check your url param for errors')

            logging.error(f'Error processing <{args.url}>')
            return SystemExit


if __name__  == '__main__':
    main()