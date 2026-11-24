"""Session 1 upload API. Run from project root:
    python -m uvicorn backend.main:app --host 127.0.0.1 --port 8001

Development defaults below are configurable, NOT measured project commitments.
Upload limits apply after Starlette has parsed/spooled multipart: add ingress
body-size limits when deploying. The comparison lock is per process; use one
worker for this foundation. Deadline checks do not forcibly stop conversion.
"""
from __future__ import annotations

from pathlib import Path
from threading import Lock
from time import monotonic
from typing import Annotated
import logging
import math
import os
import tempfile
import uuid

from fastapi import FastAPI, File, HTTPException, UploadFile, Request
from fastapi.responses import JSONResponse

from .app.pipeline import (
    DocumentInput, MISSING_COMPONENTS, PipelineInputError, run_comparison,
)
from .app.demo_runner import run_demo_analysis

logger = logging.getLogger(__name__)


def _positive_int(name: str, default: int) -> int:
    value = int(os.getenv(name, str(default)))
    if value < 1:
        raise ValueError(f"{name} must be positive")
    return value


MAX_FILE_BYTES = _positive_int("LEGAL_MAX_FILE_BYTES", 20 * 1024 * 1024)
MAX_TOTAL_BYTES = _positive_int("LEGAL_MAX_TOTAL_BYTES", 60 * 1024 * 1024)
MAX_REFERENCE_FILES = _positive_int("LEGAL_MAX_REFERENCE_FILES", 5)
DEADLINE_SECONDS = float(os.getenv("LEGAL_DEADLINE_SECONDS", "300"))
if not math.isfinite(DEADLINE_SECONDS) or DEADLINE_SECONDS <= 0:
    raise ValueError("LEGAL_DEADLINE_SECONDS must be finite and positive")

app = FastAPI(title="Legal Document Change Detection API", version="0.3.0-session1")
app.state.analysis_runner = run_demo_analysis
_comparison_lock = Lock()


@app.get("/health")
def health(request: Request):
    return {"api": "ok", "comparison_ready": request.app.state.analysis_runner is not None,
            "mode": "LOCAL_RULES_PARTIAL", "model": "not_selected",
            "lightrag_connection": "not_checked",
            "missing_components": list(MISSING_COMPONENTS)
            if request.app.state.analysis_runner is None else []}


def _save_upload(upload: UploadFile, directory: Path, number: int,
                 document_id: str, role: str, total_bytes: list[int],
                 deadline: float) -> DocumentInput:
    name = (upload.filename or "").replace("\\", "/").rsplit("/", 1)[-1]
    suffix = Path(name).suffix.lower()
    if suffix not in {".docx", ".pdf"}:
        raise HTTPException(415, detail={"code": "UNSUPPORTED_FORMAT",
                                        "message": "Chi nhan DOCX hoac PDF co lop chu.",
                                        "document_id": document_id})
    destination = directory / f"input_{number}{suffix}"
    size = 0
    with destination.open("xb") as output:
        while True:
            if monotonic() >= deadline:
                raise HTTPException(504, detail={"code": "PROCESSING_TIMEOUT",
                                                "message": "Vuot thoi gian tiep nhan file."})
            chunk = upload.file.read(1024 * 1024)
            if not chunk:
                break
            size += len(chunk)
            total_bytes[0] += len(chunk)
            if size > MAX_FILE_BYTES or total_bytes[0] > MAX_TOTAL_BYTES:
                raise HTTPException(413, detail={"code": "UPLOAD_TOO_LARGE",
                                                "message": "File vuot gioi han cau hinh."})
            output.write(chunk)
    if size == 0:
        raise HTTPException(422, detail={"code": "EMPTY_FILE",
                                        "message": "File rong.", "document_id": document_id})
    return DocumentInput(document_id, role, name, destination)


@app.post("/api/compare")
def compare_documents(
    request: Request,
    doc_v1: Annotated[UploadFile | None, File(description="Legacy alias for base_file")] = None,
    doc_s: Annotated[UploadFile | None, File(description="Legacy alias for amendment_file")] = None,
    reference_files: Annotated[list[UploadFile] | None,
                               File(description="Tai lieu tham chieu")] = None,
    base_file: Annotated[UploadFile | None, File(description="Văn bản gốc V1")] = None,
    amendment_file: Annotated[UploadFile | None, File(description="Văn bản sửa đổi S")] = None,
):
    # A sync route runs outside the event loop. Do not wrap conversion with a
    # timeout that deletes files while its worker is still using those files.
    references = reference_files or []
    uploads = [upload for upload in [doc_v1, doc_s, base_file, amendment_file, *references]
               if upload is not None]
    acquired = False
    comparison_id = str(uuid.uuid4())
    try:
        for canonical, alias, name in [(base_file, doc_v1, 'base_file'),
                                       (amendment_file, doc_s, 'amendment_file')]:
            if canonical is not None and alias is not None:
                raise HTTPException(422, detail={'code': 'AMBIGUOUS_INPUT',
                                                'message': f'Chỉ gửi {name} hoặc alias tương ứng, không gửi cả hai.'})
            if canonical is None and alias is None:
                raise HTTPException(422, detail={'code': 'MISSING_FILE',
                                                'message': f'Thiếu file bắt buộc: {name}.'})
        primary_uploads = [base_file if base_file is not None else doc_v1,
                           amendment_file if amendment_file is not None else doc_s,
                           *references]
        if len(references) > MAX_REFERENCE_FILES:
            raise HTTPException(422, detail={"code": "TOO_MANY_REFERENCES",
                                            "message": "Qua so file tham chieu cau hinh."})
        acquired = _comparison_lock.acquire(blocking=False)
        if not acquired:
            raise HTTPException(503, detail={"code": "COMPARISON_BUSY",
                                            "message": "Dang xu ly lan so sanh khac."},
                                headers={"Retry-After": "5"})
        deadline = monotonic() + DEADLINE_SECONDS
        with tempfile.TemporaryDirectory(prefix="legal_upload_") as temporary:
            directory = Path(temporary)
            total = [0]
            roles = [("v1", "BASE"), ("s", "AMENDMENT")]
            roles.extend((f"ref_{i}", "REFERENCE") for i in range(1, len(references) + 1))
            documents = [
                _save_upload(upload, directory, i, document_id, role, total, deadline)
                for i, (upload, (document_id, role)) in enumerate(zip(primary_uploads, roles))
            ]
            report = run_comparison(
                documents, comparison_id, deadline=deadline,
                analysis_runner=request.app.state.analysis_runner,
            )
        codes = {error["code"] for error in report["errors"]}
        http_status = 200
        if report["status"] == "FAILED":
            http_status = (501 if "ANALYSIS_NOT_CONFIGURED" in codes
                           else 504 if "PROCESSING_TIMEOUT" in codes
                           else 500 if report["errors"] else 200)
        return JSONResponse(status_code=http_status, content=report,
                            headers={"X-Comparison-ID": comparison_id})
    except PipelineInputError as exc:
        raise HTTPException(422, detail={"comparison_id": comparison_id,
                                        "code": exc.code, "message": str(exc),
                                        "document_id": exc.document_id}) from exc
    except HTTPException:
        raise
    except Exception:
        logger.error("comparison=%s api failed", comparison_id)
        raise HTTPException(500, detail={"comparison_id": comparison_id,
                                        "code": "INTERNAL_ERROR",
                                        "message": "Khong the xu ly yeu cau."}) from None
    finally:
        for upload in uploads:
            try:
                upload.file.close()
            except OSError:
                pass
        if acquired:
            _comparison_lock.release()
