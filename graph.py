from typing import List
from routes import Route, RouteOutput
from collections import namedtuple
from datetime import datetime, timedelta
import re
import json

class Node:
    """ 
    This class represents node of graph that contains
    information about single flight.
    """
    def __init__(self, flight: namedtuple):
        self.flight_no = flight.flight_no
        self.origin = flight.origin
        self.destination = flight.destination
        self.departure = flight.departure
        self.arrival = flight.arrival
        self.base_price = flight.base_price
        self.bag_price = flight.bag_price
        self.bags_allowed = flight.bags_allowed
        self._edges = list()

    def add_nbr(self, nbr):
        self._edges.append(nbr)

    def __iter__(self):
        return iter(self._edges)

    def as_dict(self):
        return {
            "flight_no": self.flight_no,
            "origin": self.origin,
            "destination": self.destination,
            "departure": datetime.strftime(self.departure, '%Y-%m-%dT%H:%M:%S'),
            "arrival": datetime.strftime(self.arrival, '%Y-%m-%dT%H:%M:%S'),
            "base_price": self.base_price,
            "bag_price": self.bag_price,
            "bags_allowed": self.bags_allowed,
        }


class Graph:
    """ 
    A class representing graph data structure. Nodes are represented
    as a single flight. This class contains methods for parsing input
    data, constructing graph data structure and performing search for
    flight routes.
    """
    def __init__(self, flights, max_layover: int = 6) -> None:
        self._nodes = list()
        self._flights = list()
        self._airport_index = list()
        self._parse_input_data(flights)
        self._create_graph(max_layover)

    def _parse_input_data(self, flights):
        """ 
        This function checks if the input file has 
        correct column names and correct format of input data. 
        Afterwards it parses input data and stores it in list.
        """
        # Initialize list with correct column names and get actual column names from csv file.
        columns = ['flight_no', 'origin', 'destination', 'departure', 'arrival',
                   'base_price', 'bag_price', 'bags_allowed']
        fieldnames = flights.fieldnames

        # Initialize regex to check the flight_no, origin, and destination format.
        flight_no_re = re.compile(r"[A-Z]{2}[0-9]{3}")
        origin_re = re.compile(r"[A-Z]{3}")
        destination_re = re.compile(r"[A-Z]{3}")

        # Iterate through column names in csv files and check if they have correct names.
        for col, fn in zip(columns, fieldnames):
            if re.match(col, fn) is not None:
                continue
            else:
                raise ValueError('Column name "{}" should be "{}."'.format(fn, col))

        for f in flights:
            flight_data = namedtuple('Flight', 'flight_no origin destination departure\
                                        arrival base_price bag_price bags_allowed')

            # Check flight_no, origin and destination with regex
            if not flight_no_re.match(f['flight_no']):
                raise ValueError("Incorrect flight_no value format.")

            if not origin_re.match(f['origin']):
                raise ValueError("Incorrect origin value format.")

            if not destination_re.match(f['destination']):
                raise ValueError("Incorrect destination value format.")

            try:
                # Try to change format of data and store it.
                flight_data.flight_no = f['flight_no']
                flight_data.origin = f['origin']
                flight_data.destination = f['destination']
                flight_data.departure = datetime.strptime(f['departure'], '%Y-%m-%dT%H:%M:%S')
                flight_data.arrival = datetime.strptime(f['arrival'], '%Y-%m-%dT%H:%M:%S')
                flight_data.base_price = float(f['base_price'])
                flight_data.bag_price = float(f['bag_price'])
                flight_data.bags_allowed = int(f['bags_allowed'])

                self._flights.append(flight_data)

                if f['origin'] not in self._airport_index:
                    self._airport_index.append(f['origin'])

                if f['destination'] not in self._airport_index:
                    self._airport_index.append(f['destination'])

            except ValueError:
                raise ValueError('Please check the formats in csv file: \n \
                            departure: YYYY-mm-ddTHH:MM:SS \n \
                            arrival: YYYY-mm-ddTHH:MM:SS \n \
                            bags_allowed: int \n \
                            base_price: float \n \
                            bag_price: float')

    def _create_graph(self, max_layover):
        # Create list of nodes.
        for flight in self._flights:
            self._nodes.append(Node(flight))

        # Add neighbours to each node.
        for node_a in self._nodes:
            for node_b in self._nodes:
                self._add_edge(node_a, node_b, max_layover)

    def _add_node(self, node: Node):
        # Append node to the list of nodes 
        # if it is not already present.
        if node not in self._nodes:
            self._nodes.append(node)

    @staticmethod
    def _add_edge(node: Node, nbr: Node, max_layover: int):
        td = nbr.departure - node.arrival
        if timedelta(hours=1) <= td <= timedelta(hours=max_layover) \
                and node.destination == nbr.origin:
            node.add_nbr(nbr)

    def _bfs(self, origin: str, destination: str, bags: int, dep_date: datetime = None):
        """
        This function implements the breadth-first search algorithm as a generator function 
        and performs a search on graph data structure based on given parameters.
        """

        # Check if origin and destination airports are present in dataset before performing the search.
        if destination not in self._airport_index or origin not in self._airport_index:
            return
        if not dep_date:
            q: List[Route] = [Route([n]) for n in self._nodes if n.origin == origin and n.bags_allowed >= bags]
        else:
            # Setting up upper limit for departure date.
            #date_offset = dep_date + timedelta(hours=8)
            q: List[Route] = [Route([n]) for n in self._nodes if n.origin == origin and 
                 n.departure >= dep_date and n.bags_allowed >= bags]

        while q:
            route = q.pop(0)
            if route.destination == destination:
                yield route
            for nbr in route.last_node:
                if route.is_valid_node(nbr) and \
                        nbr.bags_allowed >= bags:
                    n_route = Route(route.nodes + [nbr])
                    q.append(n_route)

    def find_routes(self, origin: str, destination: str, return_flight: bool, stay_time: int, bags: int):

        if not return_flight:
            print_out = [RouteOutput(route, bags).as_dict() for route in self._bfs(origin, destination, bags)]
            if print_out:
                print_out = sorted(print_out, key=lambda x: x['total_price'])
                print(json.dumps(print_out, indent=4))
            else:
                print("No flights found :'(.")
        else:
            routes = list()
            for route in self._bfs(origin, destination, bags):
                if not stay_time:
                    # Passengers should have at least 1 hour before departure
                    # flight of return trip if stay_time is not specified.
                    dep_date = route.last_node.arrival + timedelta(hours=1)
                else:
                    dep_date = route.last_node.arrival + timedelta(days=stay_time)  
                for return_route in self._bfs(destination, origin, bags, dep_date):
                    routes.append(Route(route.nodes + return_route.nodes))
            if routes:
                print_out = [RouteOutput(route, bags).as_dict() for route in routes]
                print_out = sorted(print_out, key=lambda x: x['total_price'])
                print(json.dumps(print_out, indent=4))
            else:
                print("No flights found :'(.")
