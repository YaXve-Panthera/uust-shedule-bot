from app.data.repository import get_group_by_name


async def group_name_validate(group_name: str):
    #group_name.lower()
    #res = await get_group_by_name(group_name)
    if group_name == "1":
        return True
    else:
        return False