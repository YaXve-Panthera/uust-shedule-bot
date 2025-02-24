from app.data.database import db
from app.data.models import Group, Faculty, WeekSchedule

async def get_groups_by_faculty(faculty_id: int):
    async with db.pool.acquire() as conn:
        query = "SELECT * FROM groups WHERE faculty_id = $1"
        result_rows = await conn.fetch(query, faculty_id)
        return [Group(**dict(row)) for row in result_rows]

async def get_faculties_by_city(city: str):
    async with db.pool.acquire() as conn:
        query = "SELECT * FROM faculties WHERE city = $1 VALUES ($1)"
        result_rows = await conn.fetch(query, city)
        return [Faculty(**dict(row)) for row in result_rows]

async def get_faculty_id_by_name(fac_name: str):
    async with db.pool.acquire() as conn:
        query = "SELECT * FROM faculties WHERE name = $1"
        res = await conn.fetchval(query, fac_name)
        return res

async def get_group_by_name(group_name: str):
    async with db.pool.acquire() as conn:
        query = "SELECT * FROM groups WHERE name = $1"
        res = await conn.fetchval(query, group_name)
        return res