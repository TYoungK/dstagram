from storages.backends.s3boto3 import S3Boto3Storage

__all__ = (
    'MediaStorage',
    'StaticStorage',
    'ProfileStorage',
)

class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False

class ProfileStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = True

class StaticStorage(S3Boto3Storage):
    location = 'static'
    file_overwrite = False
