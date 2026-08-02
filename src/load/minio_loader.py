import json
import logging
from datetime import datetime
from io import BytesIO
from minio import Minio
from minio.error import S3Error

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