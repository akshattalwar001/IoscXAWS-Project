import asyncio
import json
from app.core.database import SessionLocal
from app.services.authHelper import create_new_user, RoleEnum
from sqlalchemy import select
from app.model.models import DBUser

async def populate_users():
    with open("clean_data.json", "r") as f:
        data = json.load(f)

    async with SessionLocal() as db:
        # Fetch all existing usernames in ONE query
        result = await db.execute(select(DBUser.username))
        existing_usernames = set(result.scalars().all())
        print(f"Found {len(existing_usernames)} existing users in DB")

        created = 0
        skipped = 0
        for entry in data:
            username = entry["username"]
            password = entry["password"]

            if username in existing_usernames:
                skipped += 1
                continue

            await create_new_user(db, username=username, plain_password=password, role=RoleEnum.student)
            print(f"Created user: {username}")
            created += 1

        print(f"\nDone. Created: {created}, Skipped: {skipped}")

asyncio.run(populate_users())