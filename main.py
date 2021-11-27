from fanduelBot import FanduelBot
from barstoolUpcomingBot import BarstoolUpcomingBot
from barstoolLiveBot import BarstoolLiveBot
from fanduelLiveBot import FanduelLiveBot
from DraftkingsBot import DraftkingsBot
from FoxbetBot import FoxbetBot
from GoldenNuggetBot import GoldenNuggetBot
from WilliamHillBot import WilliamHillBot
from ArbitrageBot import ArbitrageBot



def main():

    # create the different bots for the different sportsbooks and sports
    NBAbots = []
    NBAbots.append(FoxbetBot("Foxbet NBA", 'https://mi.foxbet.com/#/basketball/competitions/8936422'))
    NBAbots.append(BarstoolUpcomingBot("Barstool Upcoming NBA", 'https://www.barstoolsportsbook.com/sports/basketball/nba'))
    NBAbots.append(BarstoolLiveBot("Barstool Live NBA", 'https://www.barstoolsportsbook.com/sports/basketball/nba?list=live'))
    NBAbots.append(GoldenNuggetBot("GoldenNugget NBA", 'https://mi-casino.goldennuggetcasino.com/sports/sport/5/basketball/matches?preselectedFilters=543'))
    NBAbots.append(DraftkingsBot("DraftKings NBA", 'https://sportsbook.draftkings.com/leagues/basketball/88670846'))
    NBAbots.append(WilliamHillBot("William Hill NBA", 'https://www.williamhill.com/us/mi/bet/basketball'))

    NFLbots = []
    NFLbots.append(FoxbetBot("Foxbet NFL", 'https://mi.foxbet.com/#/american_football/competitions/8707516'))
    NFLbots.append(BarstoolUpcomingBot("Barstool Upcoming NFL", 'https://www.barstoolsportsbook.com/sports/american_football/nfl'))
    NFLbots.append( BarstoolLiveBot("Barstool Live NFL", 'https://www.barstoolsportsbook.com/sports/american_football/nfl?list=live'))
    NFLbots.append(GoldenNuggetBot("GoldenNugget NFL",'https://mi-casino.goldennuggetcasino.com/sports/sport/3/football/matches?preselectedFilters=13'))
    NFLbots.append(DraftkingsBot("DraftKings NFL", 'https://sportsbook.draftkings.com/leagues/football/88670561'))
    NFLbots.append(WilliamHillBot("William Hill NFL", 'https://www.williamhill.com/us/mi/bet/basketball'))

    # run the arbitrage bot
    a = ArbitrageBot(NBAbots + NFLbots)
    a.run()

    """fbb = FoxbetBot('https://mi.foxbet.com/#/american_football/competitions/8211237')
    fbb.navigate()
    fbb.getData()
    print(fbb.teams)
    print(fbb.odds)"""



if __name__ == '__main__':
    main()
