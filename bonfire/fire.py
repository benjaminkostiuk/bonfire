from datetime import datetime
from .utils import format_process_name

# Models a lit bonfire
class Fire():
    def __init__(self, apps, id=None, timestamp=datetime.now(), nickname=None):
        self.id = id
        self.timestamp = timestamp
        self.apps = apps
        self.nickname = nickname

    # Class constructor to build a fire from a dict
    @classmethod
    def fromdict(cls, datadict):
        timestamp = datetime.strptime(datadict['timestamp'], '%m/%d/%Y %H:%M:%S')
        return cls(datadict['apps'], id=datadict.doc_id, timestamp=timestamp, nickname=datadict['nickname'])

    # Get the list of attribute names for a bonfire
    @classmethod
    def attrs(cls):
        return ['Id', 'Timestamp', 'Nickname', 'Apps']

    # Return a list with attributes about the bonfire
    def rattrs(self):
        MAX_APPS_SHOWN = 2
        app_names = ', '.join(list(map(format_process_name, self.apps.keys()))[:MAX_APPS_SHOWN])
        if len(self.apps) > MAX_APPS_SHOWN:
            app_names += ' (+{} more)'.format(len(self.apps) - MAX_APPS_SHOWN)
        return [self.id, self.timestamp, self.nickname, app_names]
        
    def __iter__(self):
        for key in self.__dict__:
            if key == 'id':
                continue
            if key == 'timestamp':
                yield key, getattr(self, key).strftime('%m/%d/%Y %H:%M:%S')
                continue
            yield key, getattr(self, key)