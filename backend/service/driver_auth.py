import logging
from typing import Literal

from gotrue import AuthResponse
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session

from backend.entities.driver import Driver
from backend.repository import Repository


class ServiceDriverAuth:
    def __init__(self, repository: Repository):
        self.repository = repository

    # TODO
