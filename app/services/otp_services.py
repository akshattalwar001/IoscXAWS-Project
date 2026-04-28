import random
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.model.models import OTPStore

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
# Rate limit config
MAX_OTP_SENDS_PER_HOUR = 3      # max OTP requests per enrollment per hour
MAX_VERIFY_ATTEMPTS = 5         # max failed verify attempts before lockout
OTP_WINDOW_MINUTES = 10         # rolling window for send rate limit
OTP_EXPIRY_MINUTES = 10

def generate_otp():
    return str(random.randint(100000, 999999))


async def send_otp(db: AsyncSession, enrollment_number: str, email: str):
    now = datetime.utcnow()
    window_start = now - timedelta(minutes=OTP_WINDOW_MINUTES)

    # count OTPs sent in the last 10 minutes BEFORE deleting anything
    recent_result = await db.execute(
        select(OTPStore).where(
            OTPStore.enrollment_number == enrollment_number,
            OTPStore.created_at >= window_start
        )
    )
    recent_records = recent_result.scalars().all()

    if len(recent_records) >= MAX_OTP_SENDS_PER_HOUR:
        raise ValueError(
            f"Too many OTP requests. You can request a maximum of "
            f"{MAX_OTP_SENDS_PER_HOUR} OTPs per 10 minutes. Please try again later."
        )

    # Delete only OTPs outside the window (older than 10 mins)
    all_existing = await db.execute(
        select(OTPStore).where(
            OTPStore.enrollment_number == enrollment_number,
            OTPStore.created_at < window_start
        )
    )
    for row in all_existing.scalars().all():
        await db.delete(row)
    await db.commit()

    otp = generate_otp()
    expires_at = now + timedelta(minutes=OTP_EXPIRY_MINUTES)

    # send_count tracks how many times sent in this session (always 1 for new record)
    otp_record = OTPStore(
        enrollment_number=enrollment_number,
        email=email,
        otp=otp,
        expires_at=expires_at,
        is_used=False,
        created_at=now,
        send_count=len(recent_records) + 1,  # track position in rate limit window
        attempt_count=0
    )
    db.add(otp_record)
    await db.commit()

    # send email via Gmail SMTP
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "E-Student Cell — Your OTP"
    msg["From"] = GMAIL_USER
    msg["To"] = email

    remaining = MAX_OTP_SENDS_PER_HOUR - (len(recent_records) + 1)
    html = f"""
    <div style="font-family: sans-serif; max-width: 400px; margin: auto; padding: 24px;
                border: 1px solid #eee; border-radius: 8px;">
        <h2 style="color: #333;">E-Student Cell</h2>
        <p>Your OTP for registration is:</p>
        <h1 style="letter-spacing: 8px; color: #8B1A1A;">{otp}</h1>
        <p>This OTP is valid for <strong>{OTP_EXPIRY_MINUTES} minutes</strong>.</p>
        <p style="color: #999; font-size: 12px;">
            You have {remaining} OTP request(s) remaining in this 10 minute window.
        </p>
        <p style="color: #999; font-size: 12px;">If you didn't request this, ignore this email.</p>
    </div>
    """
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, email, msg.as_string())

    return True


async def verify_otp(db: AsyncSession, enrollment_number: str, email: str, otp: str):
    result = await db.execute(
        select(OTPStore).where(
            OTPStore.enrollment_number == enrollment_number,
            OTPStore.email == email,
            OTPStore.is_used == False
        )
    )
    record = result.scalars().first()

    if not record:
        raise ValueError("No active OTP found. Please request a new OTP.")

    
    if record.attempt_count >= MAX_VERIFY_ATTEMPTS:
        raise ValueError(
            f"Too many failed attempts. Please request a new OTP."
        )

    if datetime.utcnow() > record.expires_at:
        raise ValueError("OTP has expired. Please request a new OTP.")

    # wrong OTP
    if record.otp != otp:
        record.attempt_count += 1
        remaining = MAX_VERIFY_ATTEMPTS - record.attempt_count
        await db.commit()
        if remaining <= 0:
            raise ValueError("Too many failed attempts. Please request a new OTP.")
        raise ValueError(f"Invalid OTP. {remaining} attempt(s) remaining.")

    # correct OTP
    record.is_used = True
    await db.commit()
    return True