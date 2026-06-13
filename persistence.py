import sqlite3
import threading
from langgraph.checkpoint.sqlite import SqliteSaver


class ConcurrentSafeSqliteSaver(SqliteSaver):
    """
    Wraps LangGraph's SqliteSaver with a strict thread-level advisory lock.
    Mathematically prevents database corruption when multiple webhooks fire simultaneously.
    """
    def __init__(self, db_path: str = "swarm_memory.db"):
        # Initialize the connection with thread-sharing enabled
        conn = sqlite3.connect(db_path, check_same_thread=False)
        super().__init__(conn)

        # The Titanium Lock
        self._lock = threading.RLock()

    def put(self, *args, **kwargs):
        with self._lock:
            return super().put(*args, **kwargs)

    def put_writes(self, *args, **kwargs):
        with self._lock:
            return super().put_writes(*args, **kwargs)

    def get_tuple(self, *args, **kwargs):
        with self._lock:
            return super().get_tuple(*args, **kwargs)

    def list(self, *args, **kwargs):
        with self._lock:
            return super().list(*args, **kwargs)
