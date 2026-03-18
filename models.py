import enum
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Numeric,
    ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from database import Base

class CategoryEnum(str, enum.Enum):
    General = "General"
    OBC = "OBC"
    SC_ST = "SC_ST"
    EWS = "EWS"

class ScholarshipEnum(str, enum.Enum):
    none = "None"
    EWS = "EWS"
    SC = "SC"
    Private = "Private"

class InternshipTypeEnum(str, enum.Enum):
    Government = "Government"
    Private = "Private"

class PaperTypeEnum(str, enum.Enum):
    Indian = "Indian"
    Foreign = "Foreign"

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    roll_number = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    branch = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    email = Column(String, unique=True, nullable=False)
    mobile = Column(String, nullable=False)
    address = Column(Text, nullable=True)
    photo_path = Column(String, nullable=True)
    signature_path = Column(String, nullable=True)

    classification = relationship("StudentClassification", back_populates="student", uselist=False)
    parent_details = relationship("ParentDetails", back_populates="student", uselist=False)
    academic_records = relationship("AcademicRecords", back_populates="student", uselist=False)
    financial_info = relationship("FinancialInfo", back_populates="student", uselist=False)
    documents = relationship("Documents", back_populates="student", uselist=False)
    noc_records = relationship("NocRecords", back_populates="student", uselist=False)
    placement = relationship("Placement", back_populates="student", uselist=False)
    academic_documents = relationship("AcademicDocuments", back_populates="student", uselist=False)
    internships = relationship("Internship", back_populates="student")
    research_papers = relationship("ResearchPaper", back_populates="student")

class StudentClassification(Base):
    __tablename__ = "student_classification"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), unique=True, nullable=False)
    is_hosteller = Column(Boolean, default=False)
    category = Column(Enum(CategoryEnum), nullable=False)
    sports_quota = Column(Boolean, default=False)
    is_disabled = Column(Boolean, default=False)
    is_single_child = Column(Boolean, default=False)
    ncc = Column(Boolean, default=False)
    nss = Column(Boolean, default=False)

    student = relationship("Student", back_populates="classification")

class ParentDetails(Base):
    __tablename__ = "parent_details"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), unique=True, nullable=False)
    parent_name = Column(String, nullable=False)
    profession = Column(String)
    contact_number = Column(String)
    email = Column(String)

    student = relationship("Student", back_populates="parent_details")

class AcademicRecords(Base):
    __tablename__ = "academic_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), unique=True, nullable=False)

    sem1_cgpa = Column(Numeric(4, 2), nullable=True)
    sem1_backlogs = Column(Integer, default=0)
    sem2_cgpa = Column(Numeric(4, 2), nullable=True)
    sem2_backlogs = Column(Integer, default=0)
    sem3_cgpa = Column(Numeric(4, 2), nullable=True)
    sem3_backlogs = Column(Integer, default=0)
    sem4_cgpa = Column(Numeric(4, 2), nullable=True)
    sem4_backlogs = Column(Integer, default=0)
    sem5_cgpa = Column(Numeric(4, 2), nullable=True)
    sem5_backlogs = Column(Integer, default=0)
    sem6_cgpa = Column(Numeric(4, 2), nullable=True)
    sem6_backlogs = Column(Integer, default=0)
    sem7_cgpa = Column(Numeric(4, 2), nullable=True)
    sem7_backlogs = Column(Integer, default=0)
    sem8_cgpa = Column(Numeric(4, 2), nullable=True)
    sem8_backlogs = Column(Integer, default=0)

    attendance_status = Column(String)
    club_activities = Column(Text)

    student = relationship("Student", back_populates="academic_records")

class FinancialInfo(Base):
    __tablename__ = "financial_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), unique=True, nullable=False)
    has_loan = Column(Boolean, default=False)
    scholarship_type = Column(Enum(ScholarshipEnum), default=ScholarshipEnum.none)
    scholarship_amount = Column(Numeric(10, 2), nullable=True)

    student = relationship("Student", back_populates="financial_info")

class Internship(Base):
    __tablename__ = "internships"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    internship_type = Column(Enum(InternshipTypeEnum), nullable=False)
    company_name = Column(String, nullable=False)
    duration = Column(String)
    has_stipend = Column(Boolean, default=False)
    stipend_amount = Column(Numeric(10, 2), nullable=True)

    student = relationship("Student", back_populates="internships")

class ResearchPaper(Base):
    __tablename__ = "research_papers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    title = Column(String, nullable=False)
    paper_type = Column(Enum(PaperTypeEnum), nullable=False)
    is_presentation = Column(Boolean, default=False)
    year = Column(Integer)

    student = relationship("Student", back_populates="research_papers")

class Documents(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), unique=True, nullable=False)
    aadhaar_verified = Column(Boolean, default=False)
    aadhaar_path = Column(String, nullable=True)
    pan_verified = Column(Boolean, default=False)
    pan_path = Column(String, nullable=True)
    id_card_verified = Column(Boolean, default=False)
    id_card_path = Column(String, nullable=True)
    library_card = Column(Boolean, default=False)

    student = relationship("Student", back_populates="documents")

class NocRecords(Base):
    __tablename__ = "noc_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), unique=True, nullable=False)
    noc_bl_dept = Column(Boolean, default=False)
    noc_internet_internship = Column(Boolean, default=False)
    noc_ncc = Column(Boolean, default=False)
    noc_nss = Column(Boolean, default=False)
    noc_inss = Column(Boolean, default=False)

    student = relationship("Student", back_populates="noc_records")

class Placement(Base):
    __tablename__ = "placement"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), unique=True, nullable=False)
    internal_training = Column(Boolean, default=False)
    is_placed = Column(Boolean, default=False)
    company_name = Column(String, nullable=True)
    package = Column(Numeric(10, 2), nullable=True)
    opted_higher_studies = Column(Boolean, default=False)
    opted_entrepreneurship = Column(Boolean, default=False)

    student = relationship("Student", back_populates="placement")

class AcademicDocuments(Base):
    __tablename__ = "academic_documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), unique=True, nullable=False)
    all_marksheets = Column(Boolean, default=False)
    marksheets_path = Column(String, nullable=True)
    provisional_cert = Column(Boolean, default=False)
    provisional_cert_path = Column(String, nullable=True)
    is_lost = Column(Boolean, default=False)

    student = relationship("Student", back_populates="academic_documents")