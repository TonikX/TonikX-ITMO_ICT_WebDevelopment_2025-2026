from aioboto3 import Session as AsyncS3Session
from boto3 import Session as SyncS3Session
from botocore.client import BaseClient
from botocore.config import Config
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src import config

engine = create_async_engine(config.DB_URL, echo=True, pool_size=20)
async_session: async_sessionmaker = async_sessionmaker(engine, expire_on_commit=False)


async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def get_s3_session_async() -> BaseClient:
    session = AsyncS3Session()
    client = session.client('s3', endpoint_url=config.S3_URL, aws_access_key_id=config.S3_ACCESS_KEY,
                            aws_secret_access_key=config.S3_SECRET_KEY, config=Config(signature_version='s3v4'))
    return client

def get_s3_session_sync() -> BaseClient:
    session = SyncS3Session()
    client = session.client('s3', endpoint_url=config.S3_URL, aws_access_key_id=config.S3_ACCESS_KEY,
                            aws_secret_access_key=config.S3_SECRET_KEY, config=Config(signature_version='s3v4'))
    return client
