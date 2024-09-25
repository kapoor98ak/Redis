from threading import Lock

class DataStore:
    def __init__(self):
        self._data = dict()
        self._lock = Lock()

    def __getitem__(self, key):
        item = self._data[key]
        return item

    def __setitem__(self, key, value):
            self._data[key] = value