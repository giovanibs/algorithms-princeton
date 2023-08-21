from abc import ABC, abstractmethod


class Comparable(ABC):

    @abstractmethod
    def compare_to(self):
        ...
