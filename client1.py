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

proxy = xmlrpc.client.ServerProxy(f"http://localhost/{path}")
print(proxy.serverDetails(path))

while True:
    seats = proxy.showAvailableSeats()
    print("\nAvailable seats\n" + str(seats))

    choice = int(input("\nPress -\n1. To select and book seat \n2. Change Location\n3. Exit\n\n->  "))
    if(choice==1):
        n = int(input("Which seat from 1-20 would you want to buy: "))
        msg = proxy.bookTicket(n,path)
        print(msg)
    elif(choice==2):
        path = locs[int(input('\nChoose Location -\n1: Mumbai\n2: Delhi\n3: Bangalore\n\n->  '))]
        proxy = xmlrpc.client.ServerProxy(f"http://localhost/{path}")
        print(proxy.serverDetails(path))
    elif(choice==3):
        print('\nThank you!')
        break

