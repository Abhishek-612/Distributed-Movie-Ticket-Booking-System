from xmlrpc.server import SimpleXMLRPCServer,SimpleXMLRPCRequestHandler
import xmlrpc.client
import sys,os
import queue, requests
import threading
from time import sleep
import pika


# set as False to hide logs
DEBUG = True

''' constants '''
DEBUG_FLAG = '[DEBUG]'                          # flag used in logs
BROADCAST = 'broadcast'                         # id of exchange common to all nodes (used as broadcast)
MSG_REQUEST = 'REQUEST'                         # Lamport request message prefix
MSG_RELEASE = 'RELEASE'                         # Lamport release message prefix
MSG_PERMISSION = 'PERMISSION'                   # Lamport granted permission message prefix
MSG_NETWORK_SIZE_REQUEST = 'NETWORK_SIZE'       # network size request message prefix
MSG_NETWORK_SIZE_ACK = 'NETWORK_SIZE_ACK'       # network size response message prefix
STATUS = ''

''' global variables '''
requests = queue.PriorityQueue()                # thread-safe requests queue, automatically ordered by timestamps
clock = 0                                       # logical clock used by Lamport Algorithm
network_size = 1                                # number of nodes in the system
received_permissions = 0                        # global counter: number of received permissions for the actual request
node_id = ''

global port
port = None

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/delhi','/mumbai','/bangalore')

class Request:
    def __init__(self, timestamp, queue_name, access_duration=None, city=None):
        self.timestamp = timestamp
        self.owner_id = queue_name
        self.access_duration = access_duration
        self.city = city

    def __repr__(self):
        return "(timestamp: %s, queue: %s, access_duration: %s)" % (self.timestamp, self.owner_id, self.access_duration)

    # used by PriorityQueue for comparing elements
    def __lt__(self, other):
        return self.timestamp < other["timestamp"]

def bookTicket(n,city):
    seconds = 2
    if(seats[n-1]==0):
        seats[n-1] = 1
        for i in range(1, seconds + 1):
            sleep(1)
            print('work done: ' + str(int(100*(i/seconds))) + '%')
        return f"Congratulations! You have booked seat number {n} at {cinemaName}, {city} by Server port {port}"
    else:
        return "Sorry the seat you selected has already been booked, select another seat."

def showAvailableSeats():
    return seats

# increment global variable clock
def increment_clock():
    global clock
    clock += 1
    if DEBUG:
        print(DEBUG_FLAG, "[CLOCK] incremented clock to", clock)


# return True if, and only if, all the necessary permissions for the last request have been received
def node_has_permissions():
    return received_permissions == (network_size-1)


# put a request in node's request queue
def requests_put(request):
    requests.put_nowait(request)
    if DEBUG:
        print(DEBUG_FLAG, '[PUT]', request)
        print(requests.queue)


# get the first request from node's request queue
def requests_get():
    req = requests.get()  # equivalent to get(False)
    if DEBUG:
        print(DEBUG_FLAG, '[GET]', req)
        print(requests.queue)
    return req

def enter_critical_section(request):
    global received_permissions
    global seats
    received_permissions = 0
    request = requests_get()
    print(request)
    temp = bookTicket(request["access_duration"])
    # warn other nodes that the use of CS is over
    # send_msg(MSG_RELEASE, node_id, True)
    # process_next_request()
    return temp

def serverDetails(city):
    return f"\n**********************************************************\n\nWelcome to INOX Cinema, {city}. Served by port {port}\n\n**********************************************************"


if __name__ == '__main__':
    cinemaName = "INOX Cinema"
    seats = [0 for i in range(20)]

    if sys.argv.__len__()>1:
        port = int(sys.argv[1])

    server = SimpleXMLRPCServer(("localhost", port),requestHandler=RequestHandler,allow_none=True)
    print("Welcome to "+cinemaName+f" {port} - {os.getpid()}")

    server.register_instance(node_id, "node_id")
    server.register_instance(clock, "clock")
    server.register_instance(MSG_REQUEST, "MSG_REQUEST")
    server.register_function(enter_critical_section, "enter_critical_section")
    server.register_function(increment_clock, "increment_clock")
    server.register_function(requests_put, "requests_put")
    server.register_function(bookTicket, "bookTicket")
    server.register_function(serverDetails, "serverDetails")
    server.register_function(showAvailableSeats, "showAvailableSeats")
    server.serve_forever()

