from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import app.model.models as models
import app.schema.schemas as schemas


async def get_dashboard_stats(db: AsyncSession):

    try:
        total = (await db.execute(
            select(func.count()).select_from(models.Student)
        )).scalar()

        hostellers = (await db.execute(
            select(func.count()).select_from(models.StudentClassification)
            .where(models.StudentClassification.is_hosteller == True)
        )).scalar()

        ncc_count = (await db.execute(
            select(func.count()).select_from(models.StudentClassification)
            .where(models.StudentClassification.ncc == True)
        )).scalar()

        nss_count = (await db.execute(
            select(func.count()).select_from(models.StudentClassification)
            .where(models.StudentClassification.nss == True)
        )).scalar()

        sports_count = (await db.execute(
            select(func.count()).select_from(models.StudentClassification)
            .where(models.StudentClassification.sports_quota == True)
        )).scalar()

        disabled_count = (await db.execute(
            select(func.count()).select_from(models.StudentClassification)
            .where(models.StudentClassification.is_disabled == True)
        )).scalar()

        category_rows = (await db.execute(
            select(models.StudentClassification.category, func.count())
            .group_by(models.StudentClassification.category)
        )).all()

        category_breakdown = {str(row[0]): row[1] for row in category_rows}

        loan_count = (await db.execute(
            select(func.count()).select_from(models.FinancialInfo)
            .where(models.FinancialInfo.has_loan == True)
        )).scalar()

        scholarship_rows = (await db.execute(
            select(models.FinancialInfo.scholarship_type, func.count())
            .group_by(models.FinancialInfo.scholarship_type)
        )).all()

        scholarship_breakdown = {str(row[0]): row[1] for row in scholarship_rows}

        placed_count = (await db.execute(
            select(func.count()).select_from(models.Placement)
            .where(models.Placement.is_placed == True)
        )).scalar()

        higher_studies = (await db.execute(
            select(func.count()).select_from(models.Placement)
            .where(models.Placement.opted_higher_studies == True)
        )).scalar()

        entrepreneurship = (await db.execute(
            select(func.count()).select_from(models.Placement)
            .where(models.Placement.opted_entrepreneurship == True)
        )).scalar()

        internship_count = (await db.execute(
            select(func.count()).select_from(models.Internship)
        )).scalar()

        research_count = (await db.execute(
            select(func.count()).select_from(models.ResearchPaper)
        )).scalar()

        branch_rows = (await db.execute(
            select(models.Student.branch, func.count())
            .group_by(models.Student.branch)
        )).all()

        branch_wise = {row[0]: row[1] for row in branch_rows}

        year_rows = (await db.execute(
            select(models.Student.year, func.count())
            .group_by(models.Student.year)
        )).all()

        year_wise = {str(row[0]): row[1] for row in year_rows}

        return schemas.DashboardStats(
            total_students=total,
            hostellers=hostellers,
            day_scholars=total - hostellers,
            category_breakdown=category_breakdown,
            ncc_count=ncc_count,
            nss_count=nss_count,
            sports_quota_count=sports_count,
            disabled_count=disabled_count,
            loan_count=loan_count,
            scholarship_breakdown=scholarship_breakdown,
            placed_count=placed_count,
            higher_studies_count=higher_studies,
            entrepreneurship_count=entrepreneurship,
            internship_count=internship_count,
            research_count=research_count,
            branch_wise=branch_wise,
            year_wise=year_wise,
        )

    except Exception:
        raise