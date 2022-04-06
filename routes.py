from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from graph import Node


class RouteOutput:
    def __init__(self, route: 'Route', origin: str, destination: str, bag_count: int):
        self.route = route
        self.origin = origin
        self.destination = destination
        self.bag_count = bag_count

    @staticmethod
    def _get_route_travel_time(route: 'Route') -> str:
        """ This function calculates total travel time for route """

        start_time = route.nodes[0].departure
        end_time = route.nodes[-1].arrival
        travel_time = str(end_time - start_time)
    
        return travel_time

    @staticmethod
    def _get_route_total_price(route: 'Route', bag_count: int) -> float:
        """ This function calculates total price for route.
        The price depends on number of requested bags."""

        if bag_count == 0:
            total_price = sum(float(node.base_price) for node in route.nodes)
            return total_price

        if bag_count != 0:
            total_price = sum(float(node.base_price + node.bag_price*bag_count) for node in route.nodes)
            return total_price

    def as_dict(self):
        return {
            "flights": [node.as_dict() for node in self.route.nodes],
            "origin": self.origin,
            "destination": self.destination,
            "bags_allowed": min([int(node.bags_allowed) for node in self.route.nodes]),
            "bags_count": self.bag_count,
            "total_price": self._get_route_total_price(self.route, self.bag_count),
            "travel_time": self._get_route_travel_time(self.route)
        }


class Route:
    def __init__(self, nodes: list[Node]) -> None:
        self._nodes = nodes
        self._visited_airports = list()
        self._get_visited_airports()
    
    def is_valid_node(self, node):
        if node.destination not in self._visited_airports:
            return True
        else:
            return False

    def _get_visited_airports(self):
        for node in self._nodes:
            self._visited_airports.append(node.origin)
            self._visited_airports.append(node.destination)

    @property
    def last_airport(self):
        return self._nodes[-1].destination

    @property
    def last_node(self):
        return self._nodes[-1]

    @property
    def first_node(self):
        return self._nodes[0]

    @property
    def nodes(self):
        return self._nodes
