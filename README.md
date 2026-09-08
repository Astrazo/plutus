# Plutus

An experiment in building a sports paper trader that can make predictions,
place simulated bets, and track how they turn out.

## What it does and why

Plutus simulates betting on sports games, tracking available cash, money in play,
and profit. It saves games and bets between runs so the simulation can continue
where it left off.

The idea is to build out the betting lifecycle first, then connect real game
data, sportsbook odds, and predictive models to explore whether any of this
actually makes money without donating real money to a sportsbook in the process.

## Tech

Plutus is currently built in Python with a simple command-line interface and
JSON-based persistence.

The project uses the nba-api, which will eventually source the data for modelling and inference.

## Current status

The currnet simulation can place bets, track money currently in play, settle bets,
calculate profit, and persist its state between runs.

For now, games and outcomes are simulated and bets use a fixed payout multiplier
of 1.90. The next major stage is connecting real sports data and replacing the
simulated decisions with predictive models and real odds.

As with most projects involving the words "predictive model" and "sports betting",
the difficult part is still to come.