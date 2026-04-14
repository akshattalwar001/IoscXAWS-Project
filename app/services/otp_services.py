import random
import resend
import os
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.model.models import OTPStore

resend.api_key = os.getenv("RESEND_API_KEY")

def generate_otp():
    return str(random.randint(100000, 999999))

async def send_otp(db: AsyncSession, enrollment_number: str, email: str):
    # Delete any existing OTPs for this enrollment
    existing = await db.execute(
        select(OTPStore).where(OTPStore.enrollment_number == enrollment_number)
    )
    for row in existing.scalars().all():
        await db.delete(row)
    await db.commit()

    otp = generate_otp()
    expires_at = (datetime.utcnow() + timedelta(minutes=10)).isoformat()

    otp_record = OTPStore(
        enrollment_number=enrollment_number,
        email=email,
        otp=otp,
        expires_at=expires_at,
        is_used=False
    )
    db.add(otp_record)
    await db.commit()

    # Send email via Resend
    resend.Emails.send({
        "from": os.getenv("RESEND_FROM_EMAIL"),
        "to": email,
        "subject": "E-Student Cell — Your OTP",
        "html": f"""
        <div style="font-family: sans-serif; max-width: 400px; margin: auto; padding: 24px; border: 1px solid #eee; border-radius: 8px;">
            <h2 style="color: #333;">E-Student Cell</h2>
            <p>Your OTP for registration is:</p>
            <h1 style="letter-spacing: 8px; color: #4f46e5;">{otp}</h1>
            <p>This OTP is valid for <strong>10 minutes</strong>.</p>
            <p style="color: #999; font-size: 12px;">If you didn't request this, ignore this email.</p>
        </div>
        """
    })
    return True

async def verify_otp(db: AsyncSession, enrollment_number: str, email: str, otp: str):
    result = await db.execute(
        select(OTPStore).where(
            OTPStore.enrollment_number == enrollment_number,
            OTPStore.email == email,
            OTPStore.otp == otp,
            OTPStore.is_used == False
        )
    )
    record = result.scalar_one_or_none()

    if not record:
        raise ValueError("Invalid OTP")

    if datetime.utcnow() > datetime.fromisoformat(record.expires_at):
        raise ValueError("OTP has expired")

    record.is_used = True
    await db.commit()
    return True