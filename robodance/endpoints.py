from pyramid.httpexceptions import HTTPBadRequest
from pyramid.request import Request
from pyramid.view import view_config
from .model import danceoffs, Danceoff, robots, Robot, Root
from datetime import datetime

team_size = 5


@view_config(context=Root, name='robots', renderer='json')
def robots(context: Root, request: Request):
    if 'id' in request.params:
        try:
            return context[robots].get(int(request.params['id'])).json()
        except ValueError:
            return HTTPBadRequest('Id is not an integer.')
        except KeyError:
            return HTTPBadRequest('Id not found.')
    return [r.json() for r in context[robots].values()]


@view_config(context=Root, name='danceoffs', renderer='json')
def danceoffs(context: Root, request: Request):
    if 'date' in request.params and 'id' in request.params:
        try:
            date = datetime.fromisoformat(request.params['date'])
        except ValueError:
            return HTTPBadRequest('Datetime is malformed. Please provide ISO format.')
        
        try:
            return context[danceoffs].get(Danceoff.to_key(date, int(request.params['id']))).json()
        except ValueError:
            return HTTPBadRequest('Id is not an integer.')
        except KeyError:
            return HTTPBadRequest('There is no danceoff with these parameters.')
    
    board = sorted(context[danceoffs].values(), key=getattr('time'))
    return [d.json() for d in board]

@view_config(context=Root, name='danceoff', request_method='POST', renderer='json')
def danceoff_post(context: Root, request: Request):
    if not ('team1' in request.params and 'team2' in request.params):
        return HTTPBadRequest('Two teams need to be assembled. (5 robot ids separated by comma)')
    
    robot_count = len(context[robots])
    team1 = [i for i in list(map(request.params['team1'].split(','), int)) if i < robot_count]
    team2 = [i for i in list(map(request.params['team2'].split(','), int)) if i < robot_count]

    if len(team1) != len(team2) != team_size:
        return HTTPBadRequest(f'Both teams need to contain {team_size} robots.')
    
    return context.danceoff(team1, team2)
