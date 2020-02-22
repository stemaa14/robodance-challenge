
Robodance API
==

Requirements
--
- Python 3.6 or higher
- Pip

Getting Started
--

- cd [directory containing this file]
- python -m pip install virtualenv
- python -m virtualenv venv
- venv/bin/pip install -e . (*replace bin with Scripts if you are on Windows*)
- venv/bin/pserve development.ini

Note: Default port for development is :6543 if you use the production.ini file the port will be :8080

Documentation
--

`GET /robots[?id=0]`
 - Retrieves all existing robots
 - `id` attribute lets you retrieve a specific single robot

`GET /danceoffs[?date=24.12.2019T13:59:59&id=4]`
- Retrieves all danceoff battles ordered by date and time
- `date` and `id` attributes lets you retrieve a specific single battle

`POST /danceoffs?team1=0,1,2,3,4&team2=5,6,7,8,9`
- Creates a danceoff between the two given teams `team1` and `team2`
- Returns each `date` and `id` of the 5 created battles

Note: Requests with bad or malformed query attributes will return 400 Bad Request


`robot`
|attribute |type   |comment
|--        |--     |--
|id        |int    |
|name      |string |
|experience|int    |0-9
|powermove |string |
|outOfOrder|boolean|
|avatar    |string |URL to picture


`danceoff`
|attribute   |type     |comment
|--          |--       |--
|date        |string   |ISO format
|id          |int      |Number of battle (0-4)
|participants|list[int]|The ids of the two matched robots
|winner      |robot    |
