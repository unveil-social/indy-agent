""" Simple router for routing messages to a module by family type.
"""

import re
from typing import Callable
from modules import Module
from model import Message, Agent
from . import BaseRouter, RouteAlreadyRegisteredException

class FamilyRouter(BaseRouter):
    """ Simple router for handling Sovrin Messages.

        Uses python dictionary to correlate a message type to a callback.
    """
    def __init__(self):
        self.routes = {}

    def register(self, msg_family: str, module: Module):
        """ Register a callback for messages with a given type.
        """
        if msg_family in self.routes.keys():
            raise RouteAlreadyRegisteredException()

        self.routes[msg_family] = module

    async def route(self, msg: Message):
        """ Route a message to it's registered callback.
        """
        family = FamilyRouter.family_from_type(msg.type)
        if family in self.routes.keys():
            module = self.routes[family]
            return await module.route(msg)

    @staticmethod
    def family_from_type(msg_type: str) -> str:
        matches = re.match(".+/(.+?)/\d.\d/.+", msg_type)
        if not matches:
            raise UnparsableMessageFamilyException()

        return matches.group(1)
