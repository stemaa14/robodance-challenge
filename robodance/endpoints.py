from pyramid.httpexceptions import HTTPBadRequest
from pyramid.request import Request
from pyramid.view import view_config
from .model import danceoffs, Danceoff, robots, Robot, Root
from datetime import datetime

team_size = 5


@view_config(context=Root, name='robots', renderer='json')
def robots_get(context: Root, request: Request):
    if 'id' in request.params:
        try:
            pid = int(request.params['id'])
        except ValueError:
            return HTTPBadRequest('Id is not an integer.')
            
        robot = context[robots].get(pid)
        if robot is None:
            return HTTPBadRequest('Id not found.')
        return robot.json()
    return [r.json() for r in context[robots].values()]


@view_config(context=Root, name='danceoffs', renderer='json')
def danceoffs_get(context: Root, request: Request):
    if 'date' in request.params and 'id' in request.params:
        try:
            date = datetime.fromisoformat(request.params['date'])
        except ValueError:
            return HTTPBadRequest('Datetime is malformed. Please provide ISO format.')
        
        try:
            pid = int(request.params['id'])
        except ValueError:
            return HTTPBadRequest('Id is not an integer.')
        
        danceoff = context[danceoffs].get(Danceoff.to_key(date, pid))
        if danceoff is None:
            return HTTPBadRequest('There is no danceoff with these parameters.')
        return danceoff.json()
    
    board = sorted(context[danceoffs].values())
    return [d.json() for d in board]


@view_config(context=Root, name='danceoffs', request_method='POST', renderer='json')
def danceoffs_post(context: Root, request: Request):
    if not ('team1' in request.params and 'team2' in request.params):
        return HTTPBadRequest('Two teams need to be assembled. (5 robot ids separated by comma)')
    
    robot_count = len(context[robots])
    team1 = [i for i in list(map(int, request.params['team1'].split(','))) if i < robot_count]
    team2 = [i for i in list(map(int, request.params['team2'].split(','))) if i < robot_count]

    if len(team1) != len(team2) != team_size:
        return HTTPBadRequest(f'Both teams need to contain {team_size} robots.')
    
    result = context.danceoff(team1, team2)
    return result
