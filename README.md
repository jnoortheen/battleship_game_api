# Battleship
A two player guessing game implemented using Google App Engine's Endpoints API.


## Game Description
Here is the description of classic battleship game. 
Refer: [wikia]: http://battleship.wikia.com/wiki/Battleship_(game)

###Contents:
Two game boards, each one with two grids, five ships, and a number of hit and miss markers. 

###Goal:
To sink all of your opponent's ships by correctly guessing their locations before your opponent sinks all of yours. 

###Setup:
Players receive a board with two grids, one of each type of ship, and a sufficient number of hit and miss markers. 
Before play begins, each player must secretly arrange their ships on the lower grid. 

###Rules:
1. Ships must be placed horizontally or vertically (never diagonally) across grid spaces, and can't hang over the outer grid boundary. 
1. Ships may not be placed next to each other, nor are ships allowed to share a space with another ship. 
1. Players must arrange ships and record the shots made by their opponent on the lower grid, while recording their own shots on the upper grid. 
1. Players must take turns, with each player's turn consisting of announcing a target square in the opponent's grid which is to be shot at. 
1. If a ship occupies the square, the owner of the ship must announce a "hit." Likewise, if no ship occupies the square, the player must inform of a "miss." 
1. When all of the squares of a ship have been hit, the ship is sunk. 
1. Players must announce to their opponent each time one of their ships is sunk. (Example: "You sunk my Battleship!") 
1. The winner is the first player to sink their opponent's ships before all of their own are sunk.

###Fleet:
For the number of ships and their size format look at ![battleship grid and fleet](https://github.com/jnoortheen/battleship_game_api/blob/master/img/battleship.svg)

If you feel difficult to understand how the game works try this 
[Sample Game online](http://www.knowledgeadventure.com/games/battleship/)


##Endpoints:
short description about each of the endpoints 

###create_user:
creates a new user record and insert to the database if the given user name doesn't exist already.
* path: *user*
* http_method: **POST**
* params: user_name(unique), email(optional)
* returns: user creation status

###new_game:
create a new game with a player and an opponent. Two grids of size 10x10 needs to be created for each of the user. Position and alignment(horizontal or vertical) is specified for each of the ships in the fleet with respect to the grid diagram shown in the above image. As there are 7 ships totally for each of the player, each one player need to give 7 positional arguments for positioning and aligning these ships.
* path: *game*
* http_method: **POST**
* params: left, right (arguments to create grid)
* returns: game details 

###get_game:
get a game details by its unique url_key
* path: *game/{url_key}*
* http_method: **GET**
* params: url_key of the game that is returned while creating game
* returns: game details

###get_game_history:
get the game history by its url key
* path: *game/{url_key}/history*
* http_method: **GET**
* params: url_key of the game that is returned while creating game
* returns: history of shots at both sides

###cancel_game:
mark a game as cancelled as that can't be played no longer
* path: *game/{url_key}*
* http_method: **DELETE**
* params: url_key of the game that is returned while creating game
* returns: confirmation message

###play_a_shot:
make a shooting at opponents fleet; shots must be fired alternatively one after another player. Otherwise program will raise an conflict error.
* path: *game/{url_key}*
* http_method: **PUT**
* params: url_key, player_side, ypoint, xpoint
* returns: the result of the shoot. It would be one of 'HIT', 'MISS', 'SUNK', 'SUNK_ALL' in case of sunk all ships the current player making the guess/shot will become the winner of the game.

###get_user_games:
return the list of details of games that are used by the given player name
* path: *user*
* http_method: **GET**
* params: user_name
* returns: a list of game forms

###get_user_rankings:
return the user matches and wins stats
* path: *user/all/rank*
* http_method: **GET**
* returns: a list of user match stats

##Typical Usage:
1. Refer each of the python files suppied with the repo for the module level documentation.
1. If your app is running on local machine, then you can explore the API by http://localhost:<port>/_ah/api/explorer and click 'load unsafe script' on the search field if you are using Chrome.  
1. create two users using `create_user` API.
1. create a new Game with these user records.
1. in turn each of the user has to make a guess(position as A1, B5...) and in response they will get a notification of  `'HIT' / 'MISS' / 'SUNK' / 'SUNK ALL'`

###GAE Endpoint
https://battleship-147317.appspot.com
