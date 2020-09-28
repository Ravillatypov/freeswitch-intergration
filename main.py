from aiomisc import entrypoint, ThreadPoolExecutor

from app.misc.hooks import on_start, on_stop
from app.services import services


def main():
    entrypoint.PRE_START.connect(on_start)
    entrypoint.POST_STOP.connect(on_stop)

    with entrypoint(*services) as loop:
        loop.set_default_executor(ThreadPoolExecutor(4))
        loop.run_forever()


if __name__ == '__main__':
    main()
