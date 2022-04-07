from __future__ import annotations
from datetime import datetime
from typing import List
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from graph import Node


class RouteOutput:
    def __init__(self, route: 'Route', bag_count: int) -> None:
        self._route = route
        self._origin = route.origin
        self._destination = route.destination
        self._bag_count = bag_count

    @staticmethod
    def _get_route_total_price(route: 'Route', bag_count: int) -> float:
        
        if bag_count == 0:
            total_price = sum(float(node.base_price) for node in route.nodes)
            return total_price

        if bag_count != 0:
            total_price = sum(float(node.base_price + node.bag_price*bag_count) for node in route.nodes)
            return total_price

    def as_dict(self):
        return {
            "flights": [node.as_dict() for node in self._route.nodes],
            "origin": self._origin,
            "destination": self._destination,
            "bags_allowed": min([int(node.bags_allowed) for node in self._route.nodes]),
            "bags_count": self._bag_count,
            "total_price": self._get_route_total_price(self._route, self._bag_count),
            "travel_time": str(self._route._travel_time)
        }


class Route:
    def __init__(self, nodes: List[Node]) -> None:
        self._nodes = nodes
        self._visited_airports = list()
        self._travel_time = None
        self._get_route_travel_time()
        self._get_visited_airports()
    
    def is_valid_node(self, node: Node) -> bool:
        if node.destination not in self._visited_airports:
            return True
        else:
            return False

    def _get_visited_airports(self):
        for node in self._nodes:
            self._visited_airports.append(node.origin)
            self._visited_airports.append(node.destination)

    def _get_route_travel_time(self) -> datetime:

        start_time = self._nodes[0].departure
        end_time = self._nodes[-1].arrival
        self._travel_time = end_time - start_time
  
    @property
    def destination(self):
        return self._nodes[-1].destination

    @property
    def origin(self):
        return self._nodes[0].origin

    @property
    def last_node(self):
        return self.nodes[-1]

    @property
    def nodes(self):
        return self._nodes
    
    @property
    def travel_time(self):
        return self._travel_time
