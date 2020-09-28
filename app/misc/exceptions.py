class BaseAppException(Exception):
    code: int = 1000
    message: str = 'Base exception'


class RabbitMQNotConnected(BaseAppException):
    code = 1001
    message = 'RabbitMQ is not ready'
