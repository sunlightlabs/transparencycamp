from storages.backends.s3boto import S3BotoStorage
from django.core.files.storage import get_storage_class


class CachedS3BotoStorage(S3BotoStorage):
    """
    S3 storage backend that saves the files locally, too.
    """
    def __init__(self, *args, **kwargs):
        super(CachedS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        name = super(CachedS3BotoStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name

StaticRootS3BotoStorage = lambda: CachedS3BotoStorage(location='2.0/static')
MediaRootS3BotoStorage = lambda: S3BotoStorage(location='2.0/media')
