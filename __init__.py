#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = "H.YL"

from abc import abstractmethod


# define the class of State
class State(object):
    obj = None

    @abstractmethod
    def exec(self):
        pass

    @abstractmethod
    def exit(self):
        #  状态转移策略
        #  transitions = {}
        pass


class LongStrategeState(State):

    @abstractmethod
    def exec(self):
        pass

    @abstractmethod
    def exit(self):
        #  状态转移策略
        #  transitions = {
        #             0: [1, 2, 3, 4, 5],
        #             1: 0,
        #             5: None,
        #   }
        pass


class MidStrategeState(State):

    @abstractmethod
    def exec(self):
        pass

    @abstractmethod
    def exit(self):
        # # 状态转移策略
        #  transitions = {
        #             0: [1, 2, 3, 4, 5],
        #             1: 0,
        #             2: 0,
        #             3: 0,
        #             4: 0,
        #             5: None,
        #   }
        pass


class ShortStrategeState(State):

    @abstractmethod
    def exec(self):
        # TODO need to improve
        pass

    @abstractmethod
    def exit(self):
        pass
