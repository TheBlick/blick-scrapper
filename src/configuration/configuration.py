import os


def load_required_env(env_name: str) -> str:
    if env_name not in os.environ or os.environ[env_name] == "":
        raise ConfigurationHelper.NecessaryParameterMissing(env_name)
    return os.environ[env_name]


class ConfigurationHelper:
    class NecessaryParameterMissing(Exception):
        def __init__(self, parameter):
            self.message = f"Configuration fetch failed. Necessary environment variable {parameter} is not set."
            super().__init__(self.message)

    def __init__(self, logger) -> None:
        self.logger = logger
        self.fetch_configurations()

    def fetch_configurations(self) -> None:
        """
        Fetches the required database configuration parameters from environment variables.
        """
        self.logger.info("Fetching configurations from environment variables.")
        self.__db_username = load_required_env("POSTGRES_USER")
        self.__db_password = load_required_env("POSTGRES_PASSWORD")
        self.__db_port = load_required_env("POSTGRES_PORT")
        self.__db_name = load_required_env("POSTGRES_DB")
        self.__db_host = load_required_env("POSTGRES_HOST")

        self.google_api_key = load_required_env("GOOGLE_API_KEY")
        self.google_cse_id = load_required_env("GOOGLE_CSE_ID")

    @property
    def database_uri(self) -> str:
        """
        Database URI to be used in SQLAlchemy.
        """
        # self.logger.info(f"postgresql+psycopg2://{self.__db_username}:{self.__db_password}@{self.__db_host}:{self.__db_port}/{self.__db_name}")
        return f"postgresql+psycopg2://{self.__db_username}:{self.__db_password}@{self.__db_host}:{self.__db_port}/{self.__db_name}"