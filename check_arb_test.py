import getDataFromFanduel


def main():
	getDataFromFanduel.fanduel_teams = ['brooklyn nets', 'washington wizards']
	getDataFromFanduel.barstool_teams = ['brooklyn nets','washington wizards']

	getDataFromFanduel.barstool_odds = [35,-35]
	getDataFromFanduel.fanduel_odds = [30,-40]

	print('nothing should print below')
	getDataFromFanduel.checkForArbitrage()

	print('arbitrage should be found below')
	getDataFromFanduel.barstool_odds = [35,-35]
	getDataFromFanduel.fanduel_odds = [30,-30]
	getDataFromFanduel.checkForArbitrage()

	print('arbitrage should be found below')
	getDataFromFanduel.barstool_odds = [35,-35]
	getDataFromFanduel.fanduel_odds = [50,-40]
	getDataFromFanduel.checkForArbitrage()

	print('two arbitrages should be found below')
	getDataFromFanduel.barstool_odds = [45,-35]
	getDataFromFanduel.fanduel_odds = [50,-40]
	getDataFromFanduel.checkForArbitrage()


if __name__ == '__main__':
	main()