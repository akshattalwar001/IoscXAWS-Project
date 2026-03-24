from fastapi import APIRouter
from app.routes import (
    student,
    auth,
    academic,
    parent,
    financial,
    documents,
    placement,
    internship,
    research,
    dashboard,
    classification,
    noc,
    academic_document
)

router = APIRouter()

router.include_router(student.router)
router.include_router(auth.router)
router.include_router(academic.router)
router.include_router(parent.router)
router.include_router(financial.router)
router.include_router(documents.router)
router.include_router(placement.router)
router.include_router(internship.router)
router.include_router(research.router)
router.include_router(dashboard.router)
router.include_router(classification.router)
router.include_router(noc.router)
router.include_router(academic_document.router)
