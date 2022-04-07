from argparse import ArgumentParser
import csv
from graph import Graph

if __name__ == "__main__":
    parser = ArgumentParser(usage='solution.py [-h] data origin destination [--bags] [--return_flight] [--stay] ['
                                  '--max_layover]')
    parser.add_argument("data", type=str, help="CSV file with input data.")
    parser.add_argument("origin", type=str, help="Origin airport.")
    parser.add_argument("destination", type=str, help="Destination airport.")
    parser.add_argument("--bags", default=0, type=int, help="Number of requested bags. (Optional)")
    parser.add_argument("--return_flight", action="store_true", help="Return flight (Optional)")
    parser.add_argument("--stay", default=0, type=int, help="Minimum number of days to stay in destination (Optional)")
    parser.add_argument("--max_layover", default=6, type=int, help="Maximum layover time between flights (Optional)")
    args = parser.parse_args()

    if not (args.data or args.origin or args.destination):
        parser.print_help(file=None)
        exit()

    with open(args.data, 'r') as file:
        graph = Graph(csv.DictReader(file), args.max_layover)
        graph.find_routes(args.origin, args.destination, args.return_flight, args.stay, args.bags)
