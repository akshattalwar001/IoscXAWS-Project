import asyncio
import json
import random
from app.core.database import SessionLocal
from app.model.models import (
    Student, StudentClassification, CategoryEnum,
    ParentDetails, AcademicRecords, FinancialInfo, ScholarshipEnum,
    Documents, NocRecords, Placement, AcademicDocuments,
    Internship, InternshipTypeEnum, ResearchPaper
)

async def seed_data():
    with open("data.json", "r") as f:
        data = json.load(f)

    async with SessionLocal() as db:
        success_count = 0
        skip_count = 0

        for entry in data:
            roll_no = str(entry.get("ROLLNO"))
            name = entry.get("STUDENT NAME")
            batch = entry.get("BATCH", 2021)
            father_name = entry.get("FATHER'S NAME", "Unknown")
            branch = entry.get("PRGNAME", "Unknown")
            
            # Use year 1,2,3,4 based on batch (assuming current year is 2026 => 2021 batch is 4th year)
            year = 2026 - int(batch)
            if year < 1: year = 1
            if year > 4: year = 4

            # Attempt to create the student
            from sqlalchemy.future import select
            res = await db.execute(select(Student).where(Student.roll_number == roll_no))
            existing = res.scalar_one_or_none()

            if existing:
                skip_count += 1
                continue

            student = Student(
                roll_number=roll_no,
                name=name,
                branch=branch,
                year=year,
                email=f"student_{roll_no}@example.com",
                mobile=f"999{random.randint(1000000, 9999999)}",
                address="Delhi, India"
            )
            db.add(student)
            
            # Classification
            classification = StudentClassification(
                student_id=roll_no,
                is_hosteller=random.choice([True, False, False]),
                category=random.choice(list(CategoryEnum)),
                sports_quota=random.choice([True, False, False, False]),
                is_disabled=False,
                is_single_child=random.choice([True, False, False]),
                ncc=random.choice([True, False, False, False]),
                nss=random.choice([True, False, False])
            )
            db.add(classification)

            # Parent Details
            parent = ParentDetails(
                student_id=roll_no,
                parent_name=father_name,
                profession="Private Job",
                contact_number=f"888{random.randint(1000000, 9999999)}",
                email=f"parent_{roll_no}@example.com"
            )
            db.add(parent)
            
            # Financial Info
            schol_type = random.choice([ScholarshipEnum.none, ScholarshipEnum.none, ScholarshipEnum.EWS, ScholarshipEnum.SC, ScholarshipEnum.Private])
            financial = FinancialInfo(
                student_id=roll_no,
                has_loan=random.choice([True, False, False]),
                scholarship_type=schol_type,
                scholarship_amount=50000 if schol_type != ScholarshipEnum.none else 0
            )
            db.add(financial)

            # Placement
            is_placed = year >= 3 and random.choice([True, False])
            placement = Placement(
                student_id=roll_no,
                internal_training=True,
                is_placed=is_placed,
                company_name=random.choice(["TCS","Infosys","Wipro","Cognizant","Amazon"]) if is_placed else None,
                package=random.choice([500000, 700000, 1200000, 2000000]) if is_placed else None,
                opted_higher_studies=not is_placed and random.choice([True, False, False]),
                opted_entrepreneurship=False
            )
            db.add(placement)
            
            # Internship
            if year >= 2 and random.choice([True, False]):
                internship = Internship(
                    student_id=roll_no,
                    internship_type=random.choice(list(InternshipTypeEnum)),
                    company_name="Local Tech Corp",
                    duration="2 months",
                    has_stipend=True,
                    stipend_amount=10000
                )
                db.add(internship)

            # Required records to avoid None when loaded
            db.add(AcademicRecords(student_id=roll_no, sem1_cgpa=random.uniform(6.5, 9.5)))
            db.add(Documents(student_id=roll_no))
            db.add(NocRecords(student_id=roll_no))
            db.add(AcademicDocuments(student_id=roll_no))

            success_count += 1
            if success_count % 100 == 0:
                await db.commit()  # commit in chunks

        await db.commit()
        print(f"Db populating completed. Added: {success_count}, Skipped: {skip_count}")

if __name__ == "__main__":
    asyncio.run(seed_data())