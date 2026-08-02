import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class MinIOConfig:
    endpoint: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    access_key: str = os.getenv("MINIO_ROOT_USER", "minioadmin")
    secret_key: str = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin123")
    bucket_name: str = "crypto-raw-data"


@dataclass
class PostgresConfig:
    host: str = os.getenv("POSTGRES_HOST", "localhost")
    port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    user: str = os.getenv("POSTGRES_USER", "crypto_user")
    password: str = os.getenv("POSTGRES_PASSWORD", "crypto_password_123")
    database: str = os.getenv("POSTGRES_DB", "crypto_dw")
    
    @property
    def connection_url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class AppConfig:
    minio: MinIOConfig = field(default_factory=MinIOConfig)
    postgres: PostgresConfig = field(default_factory=PostgresConfig)