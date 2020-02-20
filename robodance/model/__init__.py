from persistent import Persistent
from persistent.mapping import PersistentMapping
from BTrees.OOBTree import OOBTree
from datetime import datetime
import random

robots = 'robot_list'
danceoffs = 'danceoff_list'
adj   = ['Funky', 'Trendy', 'Cool', 'Dank',  'Mc',   'Rad',  'Lil',  'Slim', 'Smooth', 'Young', 'Fresh', 'Crazy', 'Long', 'Big', 'Ol']
names = ['Joe',   'Eric',   'Mark', 'Kevin', 'Luke', 'Karl', 'Bart', 'Moe',  'Gary',   'Keith', 'Shady', 'Earl',  'Mike', 'Gus', 'Chad']


class Root(PersistentMapping):
    __parent__ = __name__ = None

    def __init__(self):
        super().__init__()
        self[danceoffs] = OOBTree()
        self[robots] = OOBTree()
        self.generate_robots()

    def generate_robots(self) -> None:
        if len(self[robots]) == len(adj):
            return
        
        self[robots].clear()
        random.shuffle(names)

        for i in range(len(adj)):
            name = f'{adj[i]} {names[i]}'
            url = '-'.join([s.lower() for s in name.split()])
            r = Robot(self, i, name, 'Spinning Turtle', random.randrange(10), False, f'https://robohash.org/{url}.png')
            self[robots].insert(i, r)

    def danceoff(self, team1: list, team2: list) -> list:
        result = []
        time = datetime.now().replace(microsecond=0)

        for rid1, rid2, c in zip(team1, team2, range(len(team1))):
            self[danceoffs].insert(
                Danceoff.to_key(time, c), 
                Danceoff(self, time, c, self[robots][rid1], self[robots][rid2]))

            result.append({
                'date': time.isoformat(),
                'id': c   
            })
        
        return result


class Robot(Persistent):
    def __init__(self, parent: Root, rid: int, name: str, powermove: str, experience: int, out_of_order: bool, avatar: str):
        super().__init__()
        self.__parent__ = parent
        self.__name__ = rid
        self.id = rid
        self.robot_name = name
        self.powermove = powermove
        self.experience = experience
        self.out_of_order = out_of_order
        self.avatar = avatar

    def json(self) -> str:
        return {
            'id': self.id,
            'name': self.robot_name,
            'powermove': self.powermove,
            'experience': self.experience,
            'outOfOrder': self.out_of_order,
            'avatar': self.avatar
        }


class Danceoff(Persistent):
    def __init__(self, parent: Root, time: datetime, danceid: int, robot1: Robot, robot2: Robot):
        super().__init__()
        self.__parent__ = parent
        self.__name__ = Danceoff.to_key(time, danceid)
        self.time = time
        self.id = danceid
        self.participants = [robot1, robot2]
        self.winner = self.battle()

    def battle(self) -> Robot:
        candidate, opponent = self.participants
        threshold = 0.5

        threshold -= candidate.experience - opponent.experience * 0.07

        if candidate.out_of_order ^ opponent.out_of_order:
            threshold += 0.3 if candidate.out_of_order else -0.3
        
        # TODO assess powermoves

        r = random.random()
        return candidate if r > threshold else opponent

    @staticmethod
    def to_key(date: datetime, danceid: int) -> str:
        return f"{date.strftime('%Y_%m_%d_%H_%M_%S')}-{danceid}"

    def json(self) -> dict:
        return {
            'date': self.time.isoformat(),
            'id': self.id,
            'participants': [r.id for r in self.participants],
            'winner': self.winner.json()
        }
    
    def __eq__(self, other: 'Danceoff') -> bool:
        return self.time == other.time and self.id == other.id

    def __lt__(self, other: 'Danceoff') -> bool:
        return self.time < other.time and self.id < other.id


def appmaker(zodb_root):
    if 'app_root' not in zodb_root:
        zodb_root['app_root'] = Root()
        import transaction
        transaction.commit()
    return zodb_root['app_root']
