from .amqp_events import AMQPService
from .uploader import UploadService
from .converter import ConvertService


services = [
    AMQPService(),
    UploadService(),
    ConvertService(),
]

__all__ = ['services']

