from environs import Env

env = Env()
env.read_env()


class Environment:
    # Polygon.io API
    POLYGON_API_KEY = env.str("POLYGON_API_KEY")
