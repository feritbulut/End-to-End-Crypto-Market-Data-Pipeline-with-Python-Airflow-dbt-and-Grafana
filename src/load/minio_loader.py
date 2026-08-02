
import json
import logging
from datetime import datetime
from io import BytesIO
from minio import Minio
from minio.error import S3Error
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

logger = logging.getLogger(__name__)


class MinIOLoader:

    def __init__(self, endpoint: str, access_key: str, secret_key: str, secure: bool = False):
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        logger.info("MinIO client initialized")

    def save_json_to_raw(self, bucket_name: str, data: list, prefix: str = "coingecko") -> str:

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        object_name = f"raw/{prefix}_markets_{timestamp}.json"
        
        json_data = json.dumps(data, indent=2)
        json_bytes = json_data.encode('utf-8')
        
        try:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
                logger.info(f"Bucket '{bucket_name}' created")
            
            self.client.put_object(
                bucket_name,
                object_name,
                data=BytesIO(json_bytes),
                length=len(json_bytes),
                content_type="application/json"
            )
            logger.info(f"Successfully saved {object_name} to {bucket_name}")
            return object_name
            
        except S3Error as e:
            logger.error(f"Failed to save to MinIO: {e}")
            raise

    def read_json_from_raw(self, bucket_name: str, object_name: str) -> list:

        try:
            response = self.client.get_object(bucket_name, object_name)
            data = response.read()
            response.close()
            response.release_conn()
            
            json_data = json.loads(data.decode('utf-8'))
            logger.info(f"Successfully read {object_name} from {bucket_name}")
            return json_data
            
        except S3Error as e:
            logger.error(f"Failed to read from MinIO: {e}")
            raise

    def save_parquet_to_silver(self, bucket_name: str, df: pd.DataFrame, prefix: str = "coingecko") -> str:

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        object_name = f"silver/{prefix}_cleaned_{timestamp}.parquet"
        
        try:
            table = pa.Table.from_pandas(df)
            parquet_buffer = BytesIO()
            pq.write_table(table, parquet_buffer)
            parquet_buffer.seek(0)
            
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
                logger.info(f"Bucket '{bucket_name}' created")
            
            parquet_bytes = parquet_buffer.getvalue()
            self.client.put_object(
                bucket_name,
                object_name,
                data=BytesIO(parquet_bytes),
                length=len(parquet_bytes),
                content_type="application/octet-stream"
            )
            logger.info(f"Successfully saved {object_name} to {bucket_name}")
            return object_name
            
        except Exception as e:
            logger.error(f"Failed to save Parquet to MinIO: {e}")
            raise