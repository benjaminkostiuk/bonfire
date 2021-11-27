from datetime import datetime

# Models a lit bonfire
class Fire():
    def __init__(self, processes_saved, id=None, timestamp=datetime.now(), nickname=None):
        self.id = id
        self.timestamp = timestamp
        self.processes_saved = processes_saved
        self.nickname = nickname

    # Overloaded constructor to build a fire from a dict
    @classmethod
    def fromdict(cls, datadict):
        timestamp = datetime.strptime(datadict['timestamp'], '%m/%d/%Y %H:%M:%S')
        return cls(datadict['processes_saved'], id=datadict.doc_id, timestamp=timestamp,nickname=datadict['nickname'])

    # Get the list of attribute names for a bonfire
    @classmethod
    def attrs(cls):
        return ['id', 'nickname', 'timestamp']

    # Return a list with attributes about the bonfire
    def rattrs(self):
        return [self.id, self.nickname, self.timestamp]
        
    def __iter__(self):
        for key in self.__dict__:
            if key == 'id':
                continue
            if key == 'timestamp':
                yield key, getattr(self, key).strftime('%m/%d/%Y %H:%M:%S')
                continue
            yield key, getattr(self, key)