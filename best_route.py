#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from math import pi,sin,cos,acos,floor
import csv
import pandas as pd


# In[ ]:


class AirportAtlas:
    
    ''' This class is used for looking up airport details '''
    
    countries = {} #dictionary of countries (by name) and their currencies
    currencyDict = {} #currency dict - index 0 of tuple is euros in currency, index 1 is to euro
    airports = {} #dictionary of airports and their latitude/longitude
    
    def __init__ (self, countrycodes, currency, airports):
        self.load_codes(countrycodes)
        self.load_currency(currency)
        self.load_airports(airports)
    
    @classmethod 
    def load_codes(cls, file):
        '''loads currency codes by name from file'''
        with open(file, 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                cls.countries[row[0]] = row[14]
        csvFile.close()
        
    def show_currency_code(self, name):
        '''This method returns the currency code from the country name'''
        return self.countries[name]
    
    def show_country(self, code):
        '''This method returns the country name/s from the currency code'''
        return {k for k, v in self.countries.items() if v == code}
    
    @classmethod #updates currency rates
    def load_currency(cls, file):
        '''loads currencies from file'''
        with open(file, 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                cls.currencyDict[row[1]] = (row[2],row[3])
        csvFile.close()
        
    def get_toEuro_rate(self, code):
        '''This method returns the toEuro rate from the currency code'''
        return self.currencyDict[code][0]
    
    def get_fromEuro_rate(self, code):
        '''This method returns the fromEuro rate from the currency code'''
        return self.currencyDict[code][1]
    
    @classmethod
    def load_airports(cls, file):
        '''loads airports info from file'''
        with open(file, 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                cls.airports[row[4]] = (row[2], row[3], row[6], row[7])
        csvFile.close()
    
    
    def get_ap_name(self, code):
        '''This method returns the airport name from the airport code'''
        return self.airports[code][0]
    
    def get_ap_country(self, code):
        '''This method returns the airport country from the airport code'''
        return self.airports[code][1] 
    
    def get_ap_lat(self, code):
        '''This method returns the airport latitude from the airport code'''
        return self.airports[code][2]
    
    def get_ap_lng(self, code):
        '''This method returns the airport longitude from the airport code'''
        return self.airports[code][3]
    
    def get_ap_currency(self,code):
        '''This method returns the airport currency code from the airport code'''
        self.country_name = self.get_ap_country(code)
        return self.show_currency_code(self.country_name)
    
    def get_ap_toEuro_rate(self,code):
        '''This method returns the airport toEuro rate from the airport code'''
        self.currency_code = self.get_ap_currency(code)
        return self.get_toEuro_rate(self.currency_code)
    
    def get_ap_fromEuro_rate(self,code):
        '''This method returns the airport fromEuro rate from the airport code'''
        self.currency_code = self.get_ap_currency(code)
        return self.get_fromEuro_rate(self.currency_code)
    


# In[ ]:


class AircraftAtlas():
    
    ''' This class is used for looking up aircrafts details '''
    aircrafts = {}
    
    def __init__ (self, aircrafts):
        self.load_aircrafts(aircrafts)
        
    @classmethod 
    def load_aircrafts(cls, file):
        '''loads currency codes by name from file'''
        with open(file, 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                cls.aircrafts[row[0]] = (row[3],row[1],row[4], row[2])
        csvFile.close()
        
    def get_ac_type(self, code):
        '''This method returns the aircraft type from the aircraft code'''
        return self.aircrafts[code][1]
    
    def get_ac_manufacturer(self, code):
        '''This method returns the aircraft manufacturer from the aircraft code'''
        return self.aircrafts[code][0] 
    
    def get_ac_range(self, code):
        '''This method returns the aircraft range in km from the aircraft code'''
        if (self.aircrafts[code][3] == "imperial"):
            return int(float(self.aircrafts[code][2]) * 1.609)
        else:
            return int(self.aircrafts[code][2])
    


# In[ ]:


class Airport(AirportAtlas):
    
    def __init__(self, code):
        self.code = code
        self.name = self.get_ap_name(code) #airport name
        self.lat = self.get_ap_lat(code) #latitude
        self.lng = self.get_ap_lng(code) #longitude
        self.country = self.get_ap_country(code) #country of airport
        self.currency = self.get_ap_currency(code) #retrieves appropriate currency code from airport.countries dict
        self.toEuro_rate = self.get_ap_toEuro_rate(code)
        
        
    def __repr__(self):
        print('code:', self.code)
        print('name:', self.name)
        print('Country:', self.country)
        print('latitude:', self.lat)
        print('longitude:', self.lng)
        print('currency:', self.currency)
        print('toEuro rate:', self.toEuro_rate)
        return "\n"


# In[ ]:


class FlightPlan(AirportAtlas, AircraftAtlas):
    
    def __init__(self, route, airplane):
        self.route = route
        self.airplane = airplane
        
    def valid_route(self, route):
        '''check if the route is valid'''
        for elem in route:
            if elem not in self.airports:
                return ('Error! airport not valid')
        return True
        
    def valid_aircraft(self, aircraft):
        '''check if the airport is valid'''
        if aircraft not in self.aircrafts:
            return ('Error! aircraft not valid')
        return True
    
    def calculate_distance(self, airport1, airport2):
        ''' This method calculates the distance between 2 airports'''
        
        #create 2 instances of the class airport
        airport1 = Airport(airport1)
        airport2 = Airport(airport2)
        
        #extract lat and lng
        self.latitude1 = float(airport1.lat)
        self.longitude1 = float(airport1.lng)
        self.latitude2 = float(airport2.lat)
        self.longitude2 = float(airport2.lng)
        
        if self.latitude1 == self.latitude2 and self.longitude1 == self.longitude2:
            return 0
        else:
            radius_earth = 6371  # km
            theta1 = self.longitude1 * (2 * pi) / 360
            theta2 = self.longitude2 * (2 * pi) / 360
            phi1 = (90 - self.latitude1) * (2 * pi) / 360
            phi2 = (90 - self.latitude2) * (2 * pi) / 360
            distance = acos( sin(phi1) * sin(phi2) * cos(abs(theta1 - theta2)) +  cos(phi1)                             * cos(phi2) ) * radius_earth
            return floor(distance)
    
    def calculate_cost(self, airport1, airport2):
        ''' This method calculates the cost of a trip from an airport to another'''
        
        self.airport1 = Airport(airport1)
        self.distance = self.calculate_distance(airport1,airport2)
        
        return round(self.distance*(float(self.airport1.toEuro_rate)),2)
    
    def home_made_permutation(self,route, s, all_routes):
        ''' This method contains our permutation algorithm, returns a list containing 
        all the possible trips combination '''
        
        self.route = route
        self.all_routes = all_routes
        
        if len(self.route)<=1:
            self.route = route
            return self.route

        if s==(len(self.route)-1): #base case
            return  self.all_routes.append(list(self.route))
        else:
            for i in range(s,len(self.route)):
                self.route[s],self.route[i] = self.route[i],self.route[s]
                self.home_made_permutation(self.route, s+1,  self.all_routes)
                self.route[s],self.route[i] = self.route[i],self.route[s]
            return self.all_routes
        
    def fixed_dep_arr_permutation(self, route):
        ''' This method returns a list containing all possible routes assuming that departure and arrival
        airports are the same and fixed'''
        
        self.route = route
        self.fixed_route = []
        self.middle_stops = self.home_made_permutation(self.route[1:],0,[])
        self.route = route
        
        for elem in self.middle_stops:
            # insert departure airport at the beginning
            elem.insert(0,self.route[0])
            # insert at the end the final destination airport as the home airport
            elem.insert(len(elem),self.route[0])
            # insert all intermediate stops
            self.fixed_route.append(list(elem))
            
        return self.fixed_route
    
    def find_route_cost(self,route):
        ''' This method returns the cost of a specific route '''
        self.route = route
        self.cost = 0
        
        for i in range (len(self.route)-1):
            self.trip_cost = self.calculate_cost(self.route[i], self.route[i+1])
            self.cost += self.trip_cost
            
        return round(self.cost, 2)
        
    def find_cheapest_route(self, routes):
        ''' This method returns the cheapest route among all the possible routes'''
        
        self.all_routes = self.fixed_dep_arr_permutation(route) 
        #assume that the first route is the cheapest
        self.cheapest_route = [self.find_route_cost(self.all_routes[0]), self.all_routes[0]]
        
        for elem in self.all_routes:
            route_cost = self.find_route_cost(elem)
            if route_cost < self.cheapest_route[0]:
                self.cheapest_route = [route_cost, elem]
        
        return self.cheapest_route
    
    def can_fly_route(self, route, airplane):
        ''' This method returns True if an airplane can travel a specific route otherwise False'''
        
        self.airplane = Aircraft(airplane)
        self.route = route
        
        #assume that the airplane can fly
        self.can_travel = True
        
        for i in range (len(self.route)-1):
            self.can_travel = self.airplane.can_fly(self.route[i], self.route[i+1])
            if self.can_travel == False:
                break
    
        return self.can_travel
    
    def find_cheapest_route_w_airplane(self, route, airplane):
        ''' This method returns the cheapest route an airplane can perform, 
        if the airplane cannot fly any of the routes, displays appropriate error message '''
        
        if self.valid_route(route) is not True or self.valid_aircraft(airplane) is not True:
            print ('Error in the input values! Not valid route or aircraft')
        else:
            self.airplane = Aircraft(airplane)
            self.all_routes = self.fixed_dep_arr_permutation(route) 

            i = 0
            while (i < len(self.all_routes)-1):
                #if plane can fly the route
                if (self.airplane.can_fly_route(self.all_routes[i], self.airplane.code) is True):
                    #assume that the first route is the cheapest
                    self.cheapest_route_w_plane = [self.find_route_cost(self.all_routes[i]), self.all_routes[i]]
                    break
                else:
                    #if the airplane cannot fly any of the routes print an error
                    self.cheapest_route_w_plane = "The aircraft cannot perform this route"
                i += 1

            #if the plane can fly at least one of the routes, find the cheapest
            if (self.cheapest_route_w_plane != "The aircraft cannot perform this route"):
                for elem in self.all_routes:
                    route_cost = self.find_route_cost(elem)
                    if route_cost < self.cheapest_route_w_plane[0] and self.airplane.can_fly_route(elem, self.airplane.code) is True:
                        self.cheapest_route_w_plane = [route_cost, elem]

            return self.cheapest_route_w_plane
        


# In[6]:


class Aircraft(FlightPlan):
    
    def __init__(self, code):
        self.code = code
        self.type = self.get_ac_type(code) 
        self.manufacturer = self.get_ac_manufacturer(code) 
        self.range = self.get_ac_range(code) 
        
    def can_fly(self, airport1, airport2):
        ''' This method determines if an aircraft can complete the trip between airports'''

        self.distance = self.calculate_distance(airport1,airport2)
        
        if self.range < self.distance:
#             print("Error! This aircraft range is not sufficient to complete the trip")
            return False
        else:
#             print("Ok! this aircraft can complete the trip")
            return True
        
    def __repr__(self):
        print('code:', self.code)
        print('type:', self.type)
        print('manufacturer:', self.manufacturer)
        print('range:', self.range)
        return "\n"


# In[7]:

#load csv files
atlas = AirportAtlas("countrycurrency.csv", "currencyrates.csv", "airport.csv")
aircrafts = AircraftAtlas("aircraft.csv")


# In[8]:


def load_test_cases(file):
        '''loads test cases from file'''
        test_cases = []
        with open(file, 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                new_test_case = [row[:-1], row[-1]]
                test_cases.append(new_test_case)
        csvFile.close()
        return test_cases


# In[9]:


test_cases = load_test_cases("test.csv")


# In[10]:


best_routes = {}
for elem in test_cases:
#     best_routes.append(plan.find_cheapest_route_w_airplane(elem[0], elem[1]))
    plan = FlightPlan(elem[0], elem[1])
    route = plan.find_cheapest_route_w_airplane(elem[0], elem[1])
    try:
        cost = float(route[0])
        best = route[1]
    except:
        cost = 0
        best = [route]
    best_routes[cost] = best

df_best_routes = pd.DataFrame.from_dict(best_routes,orient='index')
df_best_routes.to_csv('best_routes.csv', header=None)


# In[ ]:




