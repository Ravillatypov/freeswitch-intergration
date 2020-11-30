from .amqp_events import AMQPService
from .convert import ConvertService
from .upload import UploadService

services = [
    AMQPService(),
    UploadService(),
    ConvertService(),
]

__all__ = ['services']
