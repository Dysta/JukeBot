from enum import Enum


class Environment(str, Enum):
    DEVELOPMENT = "dev"
    PRODUCTION = "prod"
