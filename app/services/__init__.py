from .amqp_events import AMQPService
from .upload import UploadService
from .convert import ConvertService


services = [
    AMQPService(),
    UploadService(),
    ConvertService(),
]

__all__ = ['services']

