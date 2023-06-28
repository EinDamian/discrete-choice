from __future__ import annotations

class FileManager:
    """Interface that takes care of reading in files and makeing files for the export."""

    def export(self, path: str) -> bool:
        raise NotImplementedError

    def import_(self, path: str) -> bool:
        raise NotImplementedError
