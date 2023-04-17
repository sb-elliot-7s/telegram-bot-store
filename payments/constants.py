from enum import Enum


class Topic(str, Enum):
    SAVE_PAYMENTS_DATA = 'save_payments_data'


class GroupID(str, Enum):
    PAYMENTS_GROUP_ID = 'payments_group_id'
