from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, EmailStr, ConfigDict
from app.model.models import CategoryEnum, ScholarshipEnum, InternshipTypeEnum, PaperTypeEnum

class StudentBase(BaseModel):
    roll_number: str
    name: str
    branch: str
    year: int
    email: EmailStr
    mobile: str
    address: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    branch: Optional[str] = None
    year: Optional[int] = None
    email: Optional[EmailStr] = None
    mobile: Optional[str] = None
    address: Optional[str] = None

class StudentResponse(StudentBase):
    model_config = ConfigDict(from_attributes=True)
    photo_path: Optional[str] = None
    signature_path: Optional[str] = None

class ClassificationBase(BaseModel):
    is_hosteller: bool = False
    category: CategoryEnum
    sports_quota: bool = False
    is_disabled: bool = False
    is_single_child: bool = False
    ncc: bool = False
    nss: bool = False

class ClassificationCreate(ClassificationBase):
    pass

class ClassificationResponse(ClassificationBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    student_id: str

class ParentBase(BaseModel):
    parent_name: str
    profession: Optional[str] = None
    contact_number: Optional[str] = None
    email: Optional[str] = None

class ParentCreate(ParentBase):
    pass

class ParentResponse(ParentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    student_id: str

class AcademicBase(BaseModel):
    sem1_cgpa: Optional[Decimal] = None
    sem1_backlogs: int = 0
    sem2_cgpa: Optional[Decimal] = None
    sem2_backlogs: int = 0
    sem3_cgpa: Optional[Decimal] = None
    sem3_backlogs: int = 0
    sem4_cgpa: Optional[Decimal] = None
    sem4_backlogs: int = 0
    sem5_cgpa: Optional[Decimal] = None
    sem5_backlogs: int = 0
    sem6_cgpa: Optional[Decimal] = None
    sem6_backlogs: int = 0
    sem7_cgpa: Optional[Decimal] = None
    sem7_backlogs: int = 0
    sem8_cgpa: Optional[Decimal] = None
    sem8_backlogs: int = 0
    attendance_status: Optional[str] = None
    club_activities: Optional[str] = None

class AcademicCreate(AcademicBase):
    pass

class AcademicResponse(AcademicBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    student_id: str

class FinancialBase(BaseModel):
    has_loan: bool = False
    scholarship_type: ScholarshipEnum = ScholarshipEnum.none
    scholarship_amount: Optional[Decimal] = None

class FinancialCreate(FinancialBase):
    pass

class FinancialResponse(FinancialBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    student_id: str

class InternshipBase(BaseModel):
    internship_type: InternshipTypeEnum
    company_name: str
    duration: Optional[str] = None
    has_stipend: bool = False
    stipend_amount: Optional[Decimal] = None

class InternshipCreate(InternshipBase):
    pass

class InternshipResponse(InternshipBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    student_id: str

class ResearchBase(BaseModel):
    title: str
    paper_type: PaperTypeEnum
    is_presentation: bool = False
    year: Optional[int] = None

class ResearchCreate(ResearchBase):
    pass

class ResearchResponse(ResearchBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    student_id: str

class DocumentsBase(BaseModel):
    aadhaar_verified: bool = False
    pan_verified: bool = False
    id_card_verified: bool = False
    library_card: bool = False

class DocumentsCreate(DocumentsBase):
    pass

class DocumentsResponse(DocumentsBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    student_id: str
    aadhaar_path: Optional[str] = None
    pan_path: Optional[str] = None
    id_card_path: Optional[str] = None

class NocBase(BaseModel):
    noc_bl_dept: bool = False
    noc_internet_internship: bool = False
    noc_ncc: bool = False
    noc_nss: bool = False
    noc_inss: bool = False

class NocCreate(NocBase):
    pass

class NocResponse(NocBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    student_id: str

class PlacementBase(BaseModel):
    internal_training: bool = False
    is_placed: bool = False
    company_name: Optional[str] = None
    package: Optional[Decimal] = None
    opted_higher_studies: bool = False
    opted_entrepreneurship: bool = False

class PlacementCreate(PlacementBase):
    pass

class PlacementResponse(PlacementBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    student_id: str

class AcademicDocsBase(BaseModel):
    all_marksheets: bool = False
    provisional_cert: bool = False
    is_lost: bool = False

class AcademicDocsCreate(AcademicDocsBase):
    pass

class AcademicDocsResponse(AcademicDocsBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    student_id: str
    marksheets_path: Optional[str] = None
    provisional_cert_path: Optional[str] = None

class FullStudentProfile(StudentResponse):
    classification: Optional[ClassificationResponse] = None
    parent_details: Optional[ParentResponse] = None
    academic_records: Optional[AcademicResponse] = None
    financial_info: Optional[FinancialResponse] = None
    documents: Optional[DocumentsResponse] = None
    noc_records: Optional[NocResponse] = None
    placement: Optional[PlacementResponse] = None
    academic_documents: Optional[AcademicDocsResponse] = None
    internships: List[InternshipResponse] = []
    research_papers: List[ResearchResponse] = []

class DashboardStats(BaseModel):
    total_students: int
    hostellers: int
    day_scholars: int
    category_breakdown: dict
    ncc_count: int
    nss_count: int
    sports_quota_count: int
    disabled_count: int
    loan_count: int
    scholarship_breakdown: dict
    placed_count: int
    higher_studies_count: int
    entrepreneurship_count: int
    internship_count: int
    research_count: int
    branch_wise: dict
    year_wise: dict
