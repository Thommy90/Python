from abc import ABC, abstractmethod

class StorageStrategy(ABC):
    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self, data):
        pass