from request import Request
from server import Server
from queue import Queue
import urllib.request as urllib
import logging
import argparse
import csv

def get_data(url):
    """
    A utility funciton used to fetch and parse csv data.

    Args:
        url(str)
    Returns:
        A list of parsed data.
    """

    csvData = urllib.urlopen(url).read()
    csvPayLoad = csv.reader(csvData.decode('utf-8').splitlines())
    csvResults = [row for row in csvPayLoad]

    return csvResults

def gatherkeys(values_list):
    """
    A utility function that gathers the relevant keys
    from the request buffer and casts those values to integers.

    Args:
        values_list(list[request-buffer])

    Returns:
        A list of casted ints. 
    """

    [time_sim, _, process_req] = values_list 

    return [int(time_sim), int(process_req)]

def create_servers(n):
    """
    A utility function used to create n amount servers.

    Args:
        n(Int)
    
    Returns:
        List of servers
    """

    return [Server(host_name=i+1) for i in range(n)]

def create_server_queue(server_list):
    """
    A utility function used to create a Queue of servers
    to round robin requests

    Args:
        server_list(dict[<Server>])
    
    Returns:
        Queue of Servers

    """

    server_queue = Queue()

    for server in server_list:
        server_queue.enqueue(server)
    
    return server_queue

def print_many_servers_result(servers_dict):
    """
    A utility print function used to aggregate n+ server nodes
    retrieve the sum, length and average and print 
    the results of each server node that processed a request.

    Args:
        servers_dict(dict[int: list[int]])

    Prints:
        A formatted message for each server which includes: server name and amount processed.
        A average seconds message which also includes the total amount of requests and total server nodes.
    """

    server_keys = list(servers_dict.keys())
    server_values = list(servers_dict.values())
    server_count = len(server_keys)
    sum_length_list = [len(servers_dict[key]) for key in server_keys]
    sum_result_list = [sum(servers_dict[key]) for key in server_keys]
    
    average = sum(sum_result_list) / sum(sum_length_list)

    for i, key in enumerate(server_keys):
        print('*' * 65)
        print('\n')
        print(f'server hostname_{key}_com: handled {len(server_values[i])} requests')
        print('\n')
        print('*' * 65)

    print('\n')
    print(f'The total average wait time is {average} seconds for a request_list of {sum(sum_length_list)} size using {server_count} servers')

def simulateManyServers(request_list, n_servers):
    """
    A primary function used to deligate creating queues for requests and servers.
    This function also processes requests so that they round robin using the server queue.

    Args:
        request_list
        n_servers(int)
    
    Prints:
        results are sent to print_many_servers_result

    """

    request_queue = Queue()
    server_list = create_servers(n_servers)
    server_queue = create_server_queue(server_list)
    processed_dict = {}
    time = 0

    for request in request_list:
        [time_simulation, sec_process] = gatherkeys(request)
        request = Request(time_simulation, sec_process)
        request_queue.enqueue(request)

    while not request_queue.is_empty():
        server_node = server_queue.dequeue()

        while server_node.busy():
            server_queue.enqueue(server_node)
            server_node.tick()
            time += 1
            server_node = server_queue.dequeue()

        if not server_node.busy():
            next_request = request_queue.dequeue()
            host_name = server_node.host_name
            server_node.start_next(next_request)

            if not host_name in processed_dict:
                processed_dict[host_name] = []

            processed_dict[host_name].append(next_request.wait_time(time))
            server_queue.enqueue(server_node)
        else:
            server_queue.enqueue(server_node)    

    print_many_servers_result(processed_dict)
    
def simulateOneServer(request_list):
    """
    A primary function used to deligate creating queues for requests.
    This function also processes requests one at a time.

    Args:
        request_list: (list[str])
    
    Prints:
        the average result and the length of the request.

    """

    request_queue = Queue()
    request_server = Server()
    processed_list = []
    time = 0

    for request in request_list:
        [time_simulation, sec_process] = gatherkeys(request)
        request = Request(time_simulation, sec_process)
        request_queue.enqueue(request)

    while not request_queue.is_empty():

        while request_server.busy():
            request_server.tick()
            time += 1

        if not request_server.busy():
            next_request = request_queue.dequeue()
            processed_list.append(next_request.wait_time(time))
            request_server.start_next(next_request)

    wait_time = sum(processed_list) / len(processed_list)

    print('*' * 70)
    print('\n')
    print(f'The Average wait time is {wait_time} for a request_list of {len(request_list)} size')
    print('\n')
    print('*' * 70)

def main():
    """
    The primary function of this application. The server param is set to default to 1 if not passed in.

    Ex:
        python3 simulation.py http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv 5
    Or:
        python3 simulation.py http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv  
            

    Args:
        url(string): url endpoint
        server(int): number of servers, defaults to 1 if not passed in.

    Logs:
        An error if the string url is entered incorrectly.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('servers', nargs='?', default=1)
    args = parser.parse_args()

    logging.basicConfig(filename='errors.log',
                        level=logging.ERROR, format='%(message)s')

    logging.getLogger('assignment5')

    if args.url:
        try:
            result = get_data(args.url)
            server_num = args.servers
            simulateOneServer(result) if server_num == 1 else simulateManyServers(result, int(server_num))

        except (ValueError, urllib.HTTPError):
            print(
                f'Something went wrong, you entered in <{args.url}>, please check your url param for errors')

            logging.error(f'Error processing <{args.url}>')
            return SystemExit


if __name__  == '__main__':
    main()