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
        # re-add skip check so re-runs are safe
        result = await db.execute(select(DBUser.username))
        existing_usernames = set(result.scalars().all())

        created = 0
        skipped = 0
        failed = 0

        for i, entry in enumerate(data):
            username = entry["username"]
            password = entry["password"]

            if username in existing_usernames:
                skipped += 1
                continue

            try:
                await create_new_user(db, username=username, plain_password=password, role=RoleEnum.student)
                print(f"[{i+1}/{len(data)}] Created: {username}")
                created += 1
            except Exception as e:
                print(f"[{i+1}/{len(data)}] Failed: {username} — {e}")
                failed += 1
                continue

        print(f"\nDone. Created: {created}, Skipped: {skipped}, Failed: {failed}")

asyncio.run(populate_users())