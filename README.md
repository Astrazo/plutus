# Plutus

An experiment in building a sports paper trader that can make predictions, place simulated bets, and track how they turn out.

## What it does and why

Plutus simulates betting on sports games, tracking available cash, money in play, and profit. It saves games and bets between runs so the simulation can continue where it left off. The idea is to work out the betting lifecycle first, then connect real game data and predictive models to explore strategies without risking money.

## Tech

Built with Python, a command-line interface, and JSON files for saved state, with basic tests written using pytest. Pandas, python-dotenv, and nba-api are listed as dependencies but are not connected to the simulator yet. No web frontend or machine learning pipeline.

## Current status

Basic bet placement, settlement, and saving state are implemented using fictional games, random outcomes, home-team selections, and a fixed default payout multiplier of 1.90. Real game data, sportsbook odds, and predictive models are not implemented yet.
