from xmlrpc.server import SimpleXMLRPCServer,SimpleXMLRPCRequestHandler
import xmlrpc.client
import sys,os

global port
port = None

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/delhi','/mumbai','/bangalore')

def bookTicket(n,city):
    if(seats[n-1]==0):
        seats[n-1] = 1
        return f"Congratulations! You have booked seat number {n} at {cinemaName}, {city} by Server port {port}"
    else:
        return "Sorry the seat you selected has already been booked, select another seat."

def showAvailableSeats():
    return seats

def serverDetails(city):
    return f"\n**********************************************************\n\nWelcome to INOX Cinema, {city}. Served by port {port}\n\n**********************************************************"

if __name__=='__main__':
    cinemaName = "INOX Cinema"
    seats = [0 for i in range(20)]

    if sys.argv.__len__()>1:
        port = int(sys.argv[1])

    server = SimpleXMLRPCServer(("localhost", port),requestHandler=RequestHandler)
    print("Welcome to "+cinemaName+f" {port} - {os.getpid()}")
    server.register_function(bookTicket, "bookTicket")
    server.register_function(serverDetails, "serverDetails")
    server.register_function(showAvailableSeats, "showAvailableSeats")
    server.serve_forever()