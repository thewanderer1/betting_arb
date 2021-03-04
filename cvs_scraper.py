from bs4 import BeautifulSoup
import random
import time
import json
from urllib import request
import twitter
import tweepy
import datetime

auth = tweepy.OAuthHandler('YtALy1rMz8KaqP2XrqT9SSpe2',
                      'r4KzqjXO5XTX5O71AU5N6JtLuKQY2PGKPBNCGmJeHdos6TWcOc')
auth.set_access_token('1358136718663245824-gGWy53o2cSWhpbkPtJ7UXQMyA0n7QN',
                      'QV7r5a7fQAMabCRyIJGKsnP8xKd6H6KcRSz3ty8l3pBaR')
api = twitter.Api(consumer_key='YtALy1rMz8KaqP2XrqT9SSpe2',
                      consumer_secret='r4KzqjXO5XTX5O71AU5N6JtLuKQY2PGKPBNCGmJeHdos6TWcOc',
                      access_token_key='1358136718663245824-gGWy53o2cSWhpbkPtJ7UXQMyA0n7QN',
                      access_token_secret='QV7r5a7fQAMabCRyIJGKsnP8xKd6H6KcRSz3ty8l3pBaR')
replyapi =  tweepy.API(auth)
states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming", "American Samoa", "District of Columbia", "Federated States of Micronesia", "Guam", "Marshall Islands", "Northern Mariana Islands", "Palau", "Puerto Rico", "Virgin Islands" ]
abbreviations = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "AS", "DC", "FM", "GU", "MH", "MP", "PW", "PR", "VI"]
while True:

	for state in abbreviations:
		ran = random.uniform(20,60)
		html=request.urlopen('https://www.cvs.com/immunizations/covid-19-vaccine/immunizations/covid-19-vaccine.vaccine-status.json?vaccineinfo').read()
		soup = BeautifulSoup(html,"lxml")
		json_content = soup.get_text()
		json_dict = json.loads(json_content)
		a = json_dict['responsePayloadData']
		b = a['data']
		cities  = ""
		if(state in b):
			for city in b[state]: 
				if city['status'] !='Fully Booked':
					cities+=  city['city'] + ", "
		if(cities !=""):
			cities = cities[:len(cities) - 2]
			#print(states[abbreviations.index(state)] + ": " + cities)
			dt_string = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
			s = dt_string + ": Vaccine Appointment Availability found at CVS in " + states[abbreviations.index(state)].upper() + ". Check Replies for details."
			print(s)
			api.PostUpdate(s )
			time.sleep(3)
			r = replyapi.search(q = "from:arb_bet "+s)
			h = [0]
			for x in h:
				try:
					if(len(cities) > 200):

						comma = cities.rfind(", ", 0, 200)
						cities1 = cities[0:comma]
						comma2 = cities.rfind(", ", comma, comma + 200)
						cities2 = cities[comma+2:comma2]
						comma3 = cities.rfind(", ", comma2, comma2 + 200)
						cities3 = cities[comma2+2:comma3]
						print("In the citie(s) of " + cities1.upper().title()) 
						print()
						x = replyapi.update_status("In the cities of " + cities1.upper().title(), x.id)
						print("and " + cities2.upper().title())
						print()
						x = replyapi.update_status("and " + cities2.upper().title(), x.id)
						if(comma3 > comma2 + 2):
							print("and " + cities3.upper().title())
							print()
							x = replyapi.update_status("and " + cities3.upper().title(), x.id)

					else:
						print("In the cities of " + cities.upper().title()) 
						x = replyapi.update_status("In the cities of " + cities.upper().title(), x.id)

				finally: 
					time.sleep(ran +30)

		ran = random.uniform(10,20)
		time.sleep(ran)

	time.sleep(300)
			




