from getDataFromFanduel import ArbitrageBot
from fanduelBot import FanduelBot
from barstoolLiveBot import BarstoolLiveBot
from barstoolUpcomingBot import BarstoolUpcomingBot

def main():
	fanduelnba = FanduelBot("https://sportsbook.fanduel.com/sports/navigation/830.1/10107.3")
	barstoolUpcomingnba = BarstoolUpcomingBot("https://www.barstoolsportsbook.com/sports/basketball/nba")
	a = ArbitrageBot(fanduelnba,barstoolUpcomingnba)
	a.scraper1.teams = ['brooklyn nets', 'washington wizards']
	a.scraper2.teams = ['brooklyn nets','washington wizards']

	a.scraper1.odds = [35,-35]
	a.scraper2.odds = [30,-40]

	print('nothing should print below')
	a.checkForArbitrage()

	print('arbitrage should be found below')
	a.scraper1.odds = [35,-35]
	a.scraper2.odds = [30,-30]
	a.checkForArbitrage()

	print('arbitrage should be found below')
	a.scraper1.odds = [35,-35]
	a.scraper2.odds = [50,-40]
	a.checkForArbitrage()

	print('two arbitrages should be found below')
	a.scraper1.odds = [45,-35]
	a.scraper2.odds = [50,-40]
	a.checkForArbitrage()


if __name__ == '__main__':
	main()