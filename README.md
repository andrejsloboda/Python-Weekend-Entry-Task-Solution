# Python Weekend Entry Task Solution

### Table of Contents

- [Description](#description)
- [How To Use](#how-to-use)
- [Requirements](#requirements)
- [References](#references)
  
---

## Description

This project is a solution to the Python Weekend [entry task](https://github.com/kiwicom/python-weekend-entry-task). It reads arguments from the console, loads data from the dataset in the CSV file, and constructs graph data structure from the data. Then it implements a breadth-first search algorithm to find every possible combination of flights from origin to destination airport based on user preferences. Subsequently, prints found routes in JSON format to the console.

### Dataset
The dataset consists of semi-randomly generated data about flights with the following columns:

- `flight_no`: Flight number.
- `origin`, `destination`: Airport codes.
- `departure`, `arrival`: Dates and times of the departures/arrivals.
- `base_price`, `bag_price`: Prices of the ticket and one piece of baggage.
- `bags_allowed`: Number of allowed pieces of baggage for the flight.

### Output
The output will be a json-compatible structured list of trips sorted by price. The trip has the following schema:
| Field          | Description                                                   |
|----------------|---------------------------------------------------------------|
| `flights`      | A list of flights in the trip according to the input dataset. |
| `origin`       | Origin airport of the trip.                                   |
| `destination`  | The final destination of the trip.                            |
| `bags_allowed` | The number of allowed bags for the trip.                      |
| `bags_count`   | The searched number of bags.                                  |
| `total_price`  | The total price for the trip.                                 |
| `travel_time`  | The total travel time.                                        |

### Search restrictions
- By default you're performing search on ALL available combinations, according to search parameters.
- In case of a combination of A -> B -> C, the layover time in B should **not be less than 1 hour and more than 6 hours**.
- No repeating airports in the same trip!
    - A -> B -> A -> C is not a valid combination for search A -> C.
- Output is sorted by the final price of the trip.

[Back To The Top](#python-weekend-entry-task-solution)

---

## How To Use

### Arguments

There are three mandatory arguments(data, origin, destination) required for the solution to print output and four
optional arguments to adjust output based on user preferences:

| Argument name  | type    | Description              | Notes                        |
|----------------|---------|--------------------------|------------------------------|
| `data`         | string  | Path to the CSV file     |                              |
| `origin`       | string  | Origin airport IATA code      |                              |
| `destination`  | string  | Destination airport IATA code |                              |
| `--bags`       | integer | Number of requested bags      | Optional (defaults to 0)     |
| `--return_flight`     | boolean | Return flight                 | Optional (defaults to false) |
| `--stay`       | integer | Minimum number of hours to stay  | Optional (defaults to1) |  
| `--max_layover`| integer | Maximum layover time between flights in hours   | Optional (defaults to 6)|

[Back To The Top](#python-weekend-entry-task-solution)

### Examples

#### A simple search without any optional arguments:

```bash
python -m solution example0.csv WIW RFZ
```
#### Output

```json
[
    {
        "flights": [
            {
                "flight_no": "ZH214",
                "origin": "WIW",
                "destination": "RFZ",
                "departure": "2021-09-01T23:20:00",
                "arrival": "2021-09-02T03:50:00",
                "base_price": 168.0,
                "bag_price": 12.0,
                "bags_allowed": 2
            }
        ],
        "origin": "WIW",
        "destination": "RFZ",
        "bags_allowed": 2,
        "bags_count": 0,
        "total_price": 168.0,
        "travel_time": "4:30:00"
    },
    {
        "flights": [
            {
                "flight_no": "ZH214",
                "origin": "WIW",
                "destination": "RFZ",
                "departure": "2021-09-04T23:20:00",
                "arrival": "2021-09-05T03:50:00",
                "base_price": 168.0,
                "bag_price": 12.0,
                "bags_allowed": 2
            }
        ],
        "origin": "WIW",
        "destination": "RFZ",
        "bags_allowed": 2,
        "bags_count": 0,
        "total_price": 168.0,
        "travel_time": "4:30:00"
    },
    {
        "flights": [
            {
                "flight_no": "ZH214",
                "origin": "WIW",
                "destination": "RFZ",
                "departure": "2021-09-09T23:20:00",
                "arrival": "2021-09-10T03:50:00",
                "base_price": 168.0,
                "bag_price": 12.0,
                "bags_allowed": 2
            }
        ],
        "origin": "WIW",
        "destination": "RFZ",
        "bags_allowed": 2,
        "bags_count": 0,
        "total_price": 168.0,
        "travel_time": "4:30:00"
    }
]
```
[Back To The Top](#python-weekend-entry-task-solution)  
#### A search for return flight with number of requested bags:

```bash
python -m solution example0.csv WIW RFZ --bags 1 --return
```
#### Output
```json
[
    {
        "flights": [
            {
                "flight_no": "ZH214",
                "origin": "WIW",
                "destination": "RFZ",
                "departure": "2021-09-01T23:20:00",
                "arrival": "2021-09-02T03:50:00",
                "base_price": 168.0,
                "bag_price": 12.0,
                "bags_allowed": 2
            },
            {
                "flight_no": "ZH214",
                "origin": "RFZ",
                "destination": "WIW",
                "departure": "2021-09-02T05:50:00",
                "arrival": "2021-09-02T10:20:00",
                "base_price": 168.0,
                "bag_price": 12.0,
                "bags_allowed": 2
            }
        ],
        "origin": "WIW",
        "destination": "WIW",
        "bags_allowed": 2,
        "bags_count": 1,
        "total_price": 360.0,
        "travel_time": "11:00:00"
    },
    {
        "flights": [
            {
                "flight_no": "ZH214",
                "origin": "WIW",
                "destination": "RFZ",
                "departure": "2021-09-01T23:20:00",
                "arrival": "2021-09-02T03:50:00",
                "base_price": 168.0,
                "bag_price": 12.0,
                "bags_allowed": 2
            },
            {
                "flight_no": "ZH214",
                "origin": "RFZ",
                "destination": "WIW",
                "departure": "2021-09-05T05:50:00",
                "arrival": "2021-09-05T10:20:00",
                "base_price": 168.0,
                "bag_price": 12.0,
                "bags_allowed": 2
            }
        ],
        "origin": "WIW",
        "destination": "WIW",
        "bags_allowed": 2,
        "bags_count": 1,
        "total_price": 360.0,
        "travel_time": "3 days, 11:00:00"
    },
    {
        "flights": [
            {
                "flight_no": "ZH214",
                "origin": "WIW",
                "destination": "RFZ",
                "departure": "2021-09-01T23:20:00",
                "arrival": "2021-09-02T03:50:00",
                "base_price": 168.0,
                "bag_price": 12.0,
                "bags_allowed": 2
            },
            {
                "flight_no": "ZH214",
                "origin": "RFZ",
                "destination": "WIW",
                "departure": "2021-09-10T05:50:00",
                "arrival": "2021-09-10T10:20:00",
                "base_price": 168.0,
                "bag_price": 12.0,
                "bags_allowed": 2
            }
        ],
        "origin": "WIW",
        "destination": "WIW",
        "bags_allowed": 2,
        "bags_count": 1,
        "total_price": 360.0,
        "travel_time": "8 days, 11:00:00"
    },
    {
        "flights": [
            {
                "flight_no": "ZH214",
                "origin": "WIW",
                "destination": "RFZ",
                "departure": "2021-09-04T23:20:00",
                "arrival": "2021-09-05T03:50:00",
                "base_price": 168.0,
                "bag_price": 12.0,
                "bags_allowed": 2
            },
            {
                "flight_no": "ZH214",
                "origin": "RFZ",
                "destination": "WIW",
                "departure": "2021-09-05T05:50:00",
                "arrival": "2021-09-05T10:20:00",
                "base_price": 168.0,
                "bag_price": 12.0,
                "bags_allowed": 2
            }
        ],
        "origin": "WIW",
        "destination": "WIW",
        "bags_allowed": 2,
        "bags_count": 1,
        "total_price": 360.0,
        "travel_time": "11:00:00"
    },
    {
        "flights": [
            {
                "flight_no": "ZH214",
                "origin": "WIW",
                "destination": "RFZ",
                "departure": "2021-09-04T23:20:00",
                "arrival": "2021-09-05T03:50:00",
                "base_price": 168.0,
                "bag_price": 12.0,
                "bags_allowed": 2
            },
            {
                "flight_no": "ZH214",
                "origin": "RFZ",
                "destination": "WIW",
                "departure": "2021-09-10T05:50:00",
                "arrival": "2021-09-10T10:20:00",
                "base_price": 168.0,
                "bag_price": 12.0,
                "bags_allowed": 2
            }
        ],
        "origin": "WIW",
        "destination": "WIW",
        "bags_allowed": 2,
        "bags_count": 1,
        "total_price": 360.0,
        "travel_time": "5 days, 11:00:00"
    },
    {
        "flights": [
            {
                "flight_no": "ZH214",
                "origin": "WIW",
                "destination": "RFZ",
                "departure": "2021-09-09T23:20:00",
                "arrival": "2021-09-10T03:50:00",
                "base_price": 168.0,
                "bag_price": 12.0,
                "bags_allowed": 2
            },
            {
                "flight_no": "ZH214",
                "origin": "RFZ",
                "destination": "WIW",
                "departure": "2021-09-10T05:50:00",
                "arrival": "2021-09-10T10:20:00",
                "base_price": 168.0,
                "bag_price": 12.0,
                "bags_allowed": 2
            }
        ],
        "origin": "WIW",
        "destination": "WIW",
        "bags_allowed": 2,
        "bags_count": 1,
        "total_price": 360.0,
        "travel_time": "11:00:00"
    }
]
```

[Back To The Top](#python-weekend-entry-task-solution)

---
## Requirements
This solution doesn't require the installation of any packages and should run on Python version 3.7 and later. 
## References
Here you can find the resources I used to create this solution and learn Python.
### Courses  
[Advanced Algorithmics and Graph Theory with Python(edx.org)](https://www.edx.org/course/advanced-algorithmics-and-graph-theory-with-python?index=product&queryID=893e87e57219aba67fcb783155865580&position=1)  
[Intro to Data Structures and Algorithms(Udacity.com)](https://www.udacity.com/course/data-structures-and-algorithms-in-python--ud513)  
[Objektové programovanie v Pythone(skillmea.sk)](https://skillmea.sk/kurzy/objektove-programovanie-v-pythone)  
### Books  
[Learn Python Programming - Third Edition(Packt)](https://www.packtpub.com/product/learn-python-programming-third-edition/9781801815093)  
[Python Object-Oriented Programming - Fourth Edition(Packt)](https://www.packtpub.com/product/python-object-oriented-programming-fourth-edition/9781801077262) 

[Back To The Top](#python-weekend-entry-task-solution)

---
