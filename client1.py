import xmlrpc.client
import sys

global path
path = None

print("\n**********************************************************\n\nWelcome to INOX Cinema\n\n**********************************************************")

locs = {1: 'Mumbai', 2: 'Delhi', 3: 'Bangalore'}
if sys.argv.__len__()>1:
    path = sys.argv[1]
else:
    path = locs[int(input('\nChoose Location -\n1: Mumbai\n2: Delhi\n3: Bangalore\n\n->  '))]

proxy = xmlrpc.client.ServerProxy(f"http://localhost/{path.lower()}")
print(proxy.serverDetails(path))


class Request:
    def __init__(self, timestamp, queue_name, access_duration=None):
        self.timestamp = timestamp
        self.owner_id = queue_name
        self.access_duration = access_duration

    def __repr__(self):
        return "(timestamp: %s, queue: %s, access_duration: %s)" % (self.timestamp, self.owner_id, self.access_duration)

    # used by PriorityQueue for comparing elements
    def __lt__(self, other):
        return self.timestamp < other.timestamp

def create_request(n,city):
    # increment timestamp before creating a request
    proxy.increment_clock()
    # push request to own queue
    request = Request(proxy.clock, proxy.node_id, (n, city))
    proxy.requests_put(request)
    print(proxy.enter_critical_section(request))


while True:
    seats = proxy.showAvailableSeats()
    print("\nAvailable seats\n" + str(seats))

    choice = int(input("\nPress -\n1. To select and book seat \n2. Change Location\n3. Exit\n\n->  "))
    if(choice==1):
        n = int(input("Which seat from 1-20 would you want to buy: "))
        create_request(n,path)
        # msg = proxy.bookTicket(n,path)
        # print(msg)
    elif(choice==2):
        path = locs[int(input('\nChoose Location -\n1: Mumbai\n2: Delhi\n3: Bangalore\n\n->  '))]
        proxy = xmlrpc.client.ServerProxy(f"http://localhost/{path}")
        print(proxy.serverDetails(path))
    elif(choice==3):
        print('\nThank you!')
        break

