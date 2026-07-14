import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile


class DocumentStorage:
    """
    Handles persistence of uploaded documents.
    """

    UPLOAD_DIRECTORY = Path("uploads")

    @classmethod
    def save(
        cls,
        file: UploadFile,
    ) -> Path:
        """
        Saves the uploaded document to the local uploads directory.

        A UUID is prepended to the filename to avoid collisions
        between files having the same name.
        """

        cls.UPLOAD_DIRECTORY.mkdir(
            exist_ok=True,
        )

        destination = (
            cls.UPLOAD_DIRECTORY
            / f"{uuid.uuid4()}_{file.filename}"
        )

        with destination.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        return destination

    @classmethod
    def delete(
        cls,
        file_path: Path,
    ) -> None:
        """
        Deletes a previously stored document.

        Useful for temporary uploads after parsing
        or future storage cleanup.
        """

        if file_path.exists():
            file_path.unlink()

