from app.routes import (
    student,
    auth,
    account,
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
    academic_document,
    register
)
from app.routes.documents import public_router as documents_public_router
from app.routes.academic_document import public_router as academic_document_public_router

router = APIRouter()

router.include_router(account.router)
router.include_router(student.router)
router.include_router(auth.router)
router.include_router(academic.router)
router.include_router(parent.router)
router.include_router(financial.router)
router.include_router(documents_public_router)
router.include_router(placement.router)
router.include_router(internship.router)
router.include_router(research.router)
router.include_router(dashboard.router)
router.include_router(classification.router)
router.include_router(noc.router)
router.include_router(academic_document_public_router)
router.include_router(register.router)
