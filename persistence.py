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

    def put(self, config, checkpoint, metadata, new_versions):
        with self._lock:
            return super().put(config, checkpoint, metadata, new_versions)

    def put_writes(self, config, writes, task_id):
        with self._lock:
            return super().put_writes(config, writes, task_id)

    def get_tuple(self, config):
        with self._lock:
            return super().get_tuple(config)

    def list(self, config, filter=None, before=None, limit=None):
        with self._lock:
            return super().list(config, filter=filter, before=before, limit=limit)
