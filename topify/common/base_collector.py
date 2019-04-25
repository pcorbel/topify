#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc


"""
The base collector.
Should be inherited from to implement a collector
"""


class BaseCollector(abc.ABC):
    @abc.abstractmethod
    def collect(self) -> NotImplementedError:
        return NotImplementedError("A collector must have a collect method")

    @property
    @abc.abstractmethod
    def _id(self) -> NotImplementedError:
        return NotImplementedError("A collector must have an _id field")
