from abc import ABC, abstractmethod

class LibraryItem(ABC):
    @abstractmethod
    def get_item_info(self):
        pass

    @abstractmethod
    def check_availability(self):
        pass