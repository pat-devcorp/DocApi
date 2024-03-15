# -*- coding: utf-8 -*-
import threading


class TimeoutError(Exception):
    pass


def timeout_function(func, args=(), kwargs={}, seconds=1):
    class InterruptableThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = None
            self.exc = None

        def run(self):
            try:
                self.result = func(*args, **kwargs)
            except Exception as e:
                self.exc = e

    thread = InterruptableThread()
    thread.daemon = True
    thread.start()
    thread.join(seconds)

    if thread.is_alive():
        raise TimeoutError("Function execution timed out")
    if thread.exc:
        raise thread.exc

    return thread.result
