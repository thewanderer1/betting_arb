# betting_arb

I envision the code to be organized as follows: 

Each scraping tool is a class and runs as its own thread for each site. The class members are the games and odds.

There is a master thread that polls the different objects for continuously updated odds. Once an opportunity is discovered, its stops, confirms that the polled odds are correct with what is on the site and immediately files both bets on the respective sites. Then it resumes polling the objects.

The plan for now should be as follows:

1. Research local sportsbooks in michigan that have online interfaces
  -FanDuel is a good start, though not local
  -Betrivers
  -William Hill
  -FoxBet
  -PointsBet
  -BetMGM
  -Yet others that are still to come online
  
2. Write python code to scrape the sites. We can begin withe the big sportsbooks (FanDuel, DraftKings, etc.). I suggest we use selenium to ensure that all the javascript on the site executes and to look as less suspicious as possible to the books. It will also make filling out the textboxes easier.

3. Write a class that will do the scraping and update its members as the odds change. Pandas could be a good option to store the data.

4. Test this to ensure that the members are showing the correct odds and the program is working as intended.

4. Write the driver that polls these objects, confirms and submits the bets.

Profit!!

Key ways to not get banned:

don't bet on clear mistakes (check to make sure the odds aren't too far off)

bet rounded to nearest 10 (or rounder if possible)

add delay (ms?) so the site doesn't detect youre automated

