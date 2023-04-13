from enum import Enum


class Topic(str, Enum):
    SAVE_USER = 'save_user'
    UPDATE_USER = 'update_user'


class GroupID(str, Enum):
    USER_GROUP = 'user-group'
