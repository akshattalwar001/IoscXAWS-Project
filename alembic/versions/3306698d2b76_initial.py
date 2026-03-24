"""initial

Revision ID: 3306698d2b76
Revises: 
Create Date: 2026-03-17 23:16:54.973654

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
revision: str = '3306698d2b76'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('students',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('roll_number', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('branch', sa.String(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('mobile', sa.String(), nullable=False),
    sa.Column('address', sa.Text(), nullable=True),
    sa.Column('photo_path', sa.String(), nullable=True),
    sa.Column('signature_path', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('roll_number')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('role', sa.Enum('student', 'admin', name='roleEnum'), nullable=False),
    sa.Column('password_hash', sa.String(), nullable=False)
    )
    op.create_table('academic_documents',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('all_marksheets', sa.Boolean(), nullable=True),
    sa.Column('marksheets_path', sa.String(), nullable=True),
    sa.Column('provisional_cert', sa.Boolean(), nullable=True),
    sa.Column('provisional_cert_path', sa.String(), nullable=True),
    sa.Column('is_lost', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('student_id')
    )
    op.create_table('academic_records',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('sem1_cgpa', sa.Numeric(precision=4, scale=2), nullable=True),
    sa.Column('sem1_backlogs', sa.Integer(), nullable=True),
    sa.Column('sem2_cgpa', sa.Numeric(precision=4, scale=2), nullable=True),
    sa.Column('sem2_backlogs', sa.Integer(), nullable=True),
    sa.Column('sem3_cgpa', sa.Numeric(precision=4, scale=2), nullable=True),
    sa.Column('sem3_backlogs', sa.Integer(), nullable=True),
    sa.Column('sem4_cgpa', sa.Numeric(precision=4, scale=2), nullable=True),
    sa.Column('sem4_backlogs', sa.Integer(), nullable=True),
    sa.Column('sem5_cgpa', sa.Numeric(precision=4, scale=2), nullable=True),
    sa.Column('sem5_backlogs', sa.Integer(), nullable=True),
    sa.Column('sem6_cgpa', sa.Numeric(precision=4, scale=2), nullable=True),
    sa.Column('sem6_backlogs', sa.Integer(), nullable=True),
    sa.Column('sem7_cgpa', sa.Numeric(precision=4, scale=2), nullable=True),
    sa.Column('sem7_backlogs', sa.Integer(), nullable=True),
    sa.Column('sem8_cgpa', sa.Numeric(precision=4, scale=2), nullable=True),
    sa.Column('sem8_backlogs', sa.Integer(), nullable=True),
    sa.Column('attendance_status', sa.String(), nullable=True),
    sa.Column('club_activities', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('student_id')
    )
    op.create_table('documents',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('aadhaar_verified', sa.Boolean(), nullable=True),
    sa.Column('aadhaar_path', sa.String(), nullable=True),
    sa.Column('pan_verified', sa.Boolean(), nullable=True),
    sa.Column('pan_path', sa.String(), nullable=True),
    sa.Column('id_card_verified', sa.Boolean(), nullable=True),
    sa.Column('id_card_path', sa.String(), nullable=True),
    sa.Column('library_card', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('student_id')
    )
    op.create_table('financial_info',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('has_loan', sa.Boolean(), nullable=True),
    sa.Column('scholarship_type', sa.Enum('none', 'EWS', 'SC', 'Private', name='scholarshipenum'), nullable=True),
    sa.Column('scholarship_amount', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('student_id')
    )
    op.create_table('internships',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('internship_type', sa.Enum('Government', 'Private', name='internshiptypeenum'), nullable=False),
    sa.Column('company_name', sa.String(), nullable=False),
    sa.Column('duration', sa.String(), nullable=True),
    sa.Column('has_stipend', sa.Boolean(), nullable=True),
    sa.Column('stipend_amount', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('noc_records',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('noc_bl_dept', sa.Boolean(), nullable=True),
    sa.Column('noc_internet_internship', sa.Boolean(), nullable=True),
    sa.Column('noc_ncc', sa.Boolean(), nullable=True),
    sa.Column('noc_nss', sa.Boolean(), nullable=True),
    sa.Column('noc_inss', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('student_id')
    )
    op.create_table('parent_details',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('parent_name', sa.String(), nullable=False),
    sa.Column('profession', sa.String(), nullable=True),
    sa.Column('contact_number', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('student_id')
    )
    op.create_table('placement',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('internal_training', sa.Boolean(), nullable=True),
    sa.Column('is_placed', sa.Boolean(), nullable=True),
    sa.Column('company_name', sa.String(), nullable=True),
    sa.Column('package', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('opted_higher_studies', sa.Boolean(), nullable=True),
    sa.Column('opted_entrepreneurship', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('student_id')
    )
    op.create_table('research_papers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('paper_type', sa.Enum('Indian', 'Foreign', name='papertypeenum'), nullable=False),
    sa.Column('is_presentation', sa.Boolean(), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student_classification',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('is_hosteller', sa.Boolean(), nullable=True),
    sa.Column('category', sa.Enum('General', 'OBC', 'SC_ST', 'EWS', name='categoryenum'), nullable=False),
    sa.Column('sports_quota', sa.Boolean(), nullable=True),
    sa.Column('is_disabled', sa.Boolean(), nullable=True),
    sa.Column('is_single_child', sa.Boolean(), nullable=True),
    sa.Column('ncc', sa.Boolean(), nullable=True),
    sa.Column('nss', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('student_id')
    )

def downgrade() -> None:
    op.drop_table('student_classification')
    op.drop_table('research_papers')
    op.drop_table('placement')
    op.drop_table('parent_details')
    op.drop_table('noc_records')
    op.drop_table('internships')
    op.drop_table('financial_info')
    op.drop_table('documents')
    op.drop_table('academic_records')
    op.drop_table('academic_documents')
    op.drop_table('users')
    op.drop_table('students')
