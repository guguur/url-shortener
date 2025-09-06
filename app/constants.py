from enum import Enum, unique


@unique
class Environment(Enum):
    DEV = "dev"
    PROD = "prod"
