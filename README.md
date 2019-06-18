## Group project of the module Data Structures & Algorithms

**Problem Statement:**
Imagine you work for a small software company that has won the tender to deliver a fuel management software solution to a large Airline company. The airline is entering the European air freight cargo business and wants a software tool to manage their fuel purchasing strategy.
Each week, an aircraft will fly trips to a number of other cities. The airplane will start and end in the same home airport each week. The company has a number of different types of aircraft that have different fuel capacities and the cost of fuel varies from airport to airport. 

### Given a list of airports (including to the home airport) that a given plane needs to visit in a week, the most economic route must be found to visit all the airport and return to the home base. Note that fuel has a different place depending on the departure location.


#### Input:
- *Flight Plan*, a sequence of airports where the first airport is the home airport and where the aircraft must return after visinting all the other airport. 

Example: SNN	ORK	MAN	CDG	SIN

- *Aircraft*, the airplane that will need to perform the route

Example:  Boing 777

Example input:
```DUB CPH LHR MOW HEL	777```


#### Output:

The cheapest route leaving from the home airport, visiting all the other airports and return home, and the cost of the trip.
If the airplane can not perform the route, an error message will be displated.

Example: DUB → LHR → CPH → HEL → MOW → DUB (Euro 2,883.51)

Example output:

```DUB LHR CPH HEL MOW DUB 2,883.51```


#### Files included:
- `airport.csv`   containing details about the airports
- `aircraft.csv`  containing details about the aircrafts
- `countrycurrency.csv`  containing details about countries and related currencies
- `currencyrates.csv`	 containing details about currency exchange rate
- `test.csv`  containing test input data
- `best_route_notebook.ipynb`	 jupiter notebook with step by step solution
- `best_route.py`	final solution program
- `HashTablesImplementation.ipynb` personal notebook containing Hash Tables Implementation
