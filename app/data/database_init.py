import asyncio
from collections import Counter
from app.data.database import db
from app.data.models import Group, Faculty
from app.parser.parser import get_faculties_list, get_groups_list

async def insert_faculties():
    faculties = await get_faculties_list()
    faculties_data = [(faculty.name, faculty.city) for faculty in faculties]

    async with db.pool.acquire() as conn:
        query = "INSERT INTO faculties (name, city) VALUES ($1, $2)"
        await conn.executemany(query, faculties_data)

async def insert_groups():
    groups = await get_groups_list()
    groups_data = [(group.name, group.course, group.faculty_id) for group in groups]
    async with db.pool.acquire() as conn:
        query = "INSERT INTO groups (name, course, faculty_id) VALUES ($1, $2, $3)"
        await conn.executemany(query, groups_data)

async def lower_names():
    async with db.pool.acquire() as conn:
        try:
            # Fetch all group names from the database
            query = "SELECT id, name FROM groups"
            result = await conn.fetch(query)

            # Convert each group name to lowercase and update in the database
            for row in result:
                group_id, old_name = row['id'], row['name'].lower()
                update_query = "UPDATE groups SET name = $1 WHERE id = $2"
                await conn.execute(update_query, old_name, group_id)
        except Exception as e:
            print(f"Error updating group names: {e}")

async def find_duplicate_group_names():
    async with db.pool.acquire() as conn:
        try:
            # Fetch all group names from the database
            query = "SELECT name FROM groups"
            result = await conn.fetch(query)

            # Extract names and count occurrences
            names = [row['name'] for row in result]
            name_counts = Counter(names)

            # Find duplicates
            duplicates = [name for name, count in name_counts.items() if count > 1]

            return duplicates

        except Exception as e:
            print(f"Error finding duplicate group names: {e}")
            return []

async def main():
    await db.connect()
    try:
        await insert_faculties()
        await insert_groups()
        await lower_names()
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())