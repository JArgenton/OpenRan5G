from abc import ABC, abstractmethod
from enum import Enum
from tests.iperfr3_test import Iperf


class test(ABC):
    server = "127.0.0.1"
    @abstractmethod
    def execute():
        pass
    @abstractmethod
    def create_test(): 
        pass
    @abstractmethod
    def get_plot_data():
        pass
    @abstractmethod
    def save_me():
        pass
    @classmethod
    def get_name():
        pass


    