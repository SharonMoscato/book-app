from enum import Enum

class Config(Enum):
    minio_endpoint = 'http://localhost:9000'  
    access_key = 'minioadmin' 
    secret_key = 'minioadmin' 
    bucket_name = 'data'  
    rating_threshold = 8
