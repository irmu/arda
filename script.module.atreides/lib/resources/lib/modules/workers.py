# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
#  As long as you retain this notice you can do whatever you want with this
# stuff. Just please ask before copying. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Atreides
# Addon id: plugin.video.atreides
# Addon Provider: House Atreides

'''
2019/07/07: Added hanging_threads from the below git, but with modifications for my needs and wants:
            https://github.com/niccokunzmann/hanging_threads/blob/master/hanging_threads.py
'''
import linecache
import threading
import time
import sys

from resources.lib.modules import control, log_utils

SECONDS_FROZEN = int(control.setting('thread.frozen'))   # seconds
TEST_INTERVAL = int(control.setting('thread.interval'))  # milliseconds


class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):
        self._target(*self._args)


def start_monitoring(seconds_frozen=SECONDS_FROZEN, test_interval=TEST_INTERVAL):
    """Start monitoring for hanging threads.
    seconds_frozen - How much time should thread hang to activate
    printing stack trace - default(8)
    tests_interval - Sleep time of monitoring thread (in milliseconds)
    - default(100)
    """
    thread = StoppableThread(target=monitor, args=(seconds_frozen, test_interval))
    thread.daemon = True
    thread.start()
    return thread


class StoppableThread(threading.Thread):
    """Thread class with a stop() method.
    The thread itself has to check regularly for the is_stopped()
    condition.
    """
    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stopped = False

    def stop(self):
        self._stopped = True

    def is_stopped(self):
        return self._stopped


def monitor(seconds_frozen, test_interval):
    """Monitoring thread function.
    Checks if thread is hanging for time defined by
    ``seconds_frozen`` parameter every ``test_interval`` milliseconds.
    """
    current_thread = threading.current_thread()
    hanging_threads = set()
    old_threads = {}  # Threads found on previous iteration.

    while not current_thread.is_stopped():
        new_threads = get_current_frames()

        # Report died threads.
        for thread_id in old_threads.keys():
            if thread_id not in new_threads and thread_id in hanging_threads:
                log_died_thread(thread_id)

        # Process live threads.
        time.sleep(test_interval/1000.)
        now = time.time()
        then = now - seconds_frozen
        for thread_id, thread_data in new_threads.items():
            # Don't report the monitor thread.
            if thread_id == current_thread.ident:
                continue
            frame = thread_data['frame']
            # If thread is new or it's stack is changed then update time.
            if (thread_id not in old_threads or frame != old_threads[thread_id]['frame']):
                thread_data['time'] = now
                # If the thread was hanging then report awaked thread.
                if thread_id in hanging_threads:
                    hanging_threads.remove(thread_id)
                    log_awaked_thread(thread_id)
            else:
                # If stack is not changed then keep old time.
                last_change_time = old_threads[thread_id]['time']
                thread_data['time'] = last_change_time
                # Check if this is a new hanging thread.
                if (thread_id not in hanging_threads and last_change_time < then):
                    # Gotcha!
                    hanging_threads.add(thread_id)
                    # Report the hanged thread.
                    log_hanged_thread(thread_id, frame)
        old_threads = new_threads


def get_current_frames():
    """Return current threads prepared for
    further processing.
    """
    ret = dict()
    for thread_id, frame in sys._current_frames().items():
        ret[thread_id] = {'frame': thread2list(frame), 'time': None}
    return ret

def frame2string(frame):
    """Return info about frame.
    Keyword arg:
        frame
    Return string in format:
    File {file name}, line {line number}, in
    {name of parent of code object} {newline}
    Line from file at line number
    """

    lineno = frame.f_lineno  # or f_lasti
    co = frame.f_code
    filename = co.co_filename
    name = co.co_name
    s = '\tFile "{0}", line {1}, in {2}'.format(filename, lineno, name)
    line = linecache.getline(filename, lineno, frame.f_globals).lstrip()
    return s + '\n\t\t' + line


def thread2list(frame):
    """Return list with string frame representation of each frame of
    thread.
    """
    l = []
    while frame:
        l.insert(0, frame2string(frame))
        frame = frame.f_back
    return l


def log_hanged_thread(thread_id, frame):
    """Print the stack trace of the deadlock after hanging
    `seconds_frozen`.
    """
    message = 'Thread Monitoring: Thread %s hangs - %s' % (thread_id, ''.join(frame))
    if 'atreides' in message:
        log_utils.log(message)


def log_awaked_thread(thread_id):
    """Print message about awaked thread that was considered as
    hanging.
    """
    message = 'Thread Monitoring: Thread %s resumed' % (thread_id)
    log_utils.log(message)


def log_died_thread(thread_id):
    """Print message about died thread that was considered as
    hanging.
    """
    message = 'Thread Monitoring: Thread %s closed' % (thread_id)
    log_utils.log(message)
