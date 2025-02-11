from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import asyncio
from app.data.models import Faculty, Group
from app.data.repository import get_faculty_id_by_name

async def get_week_schedule_by_group(group, week):
    res = None
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto("https://isu.uust.ru/schedule_2024/")
            await page.get_by_placeholder("Введите название группы").click()
            await page.get_by_role("button", name=group).click()
            page.locator(".control-label")
            await page.locator("#week_choice").select_option(str(week))
            await page.wait_for_timeout(500)
            res = await page.get_by_role("table").inner_html()
        except Exception as e:
            print(e)
        finally:
            return res

def parse_schedule(schedule: str):
    res = []
    soup = BeautifulSoup(schedule, "html.parser")
    table_body = soup.find("tbody")
    for i in range(1, 7):
        day = []
        for j in range(1,10):
            cell = table_body.find("td", id=f"{j}_{i}_group")
            if cell is not None and cell.text != "":
                cell_divs = cell.find_all("div")
                for div in cell_divs:
                    lesson_name = div.text[:cell.text.index(")")+1]
                    teacher = div.find('button', onclick=lambda x: 'link_teacher' in x)
                    classroom = div.find('button', onclick=lambda x: 'link_class' in x)

                    additional = (div.text.replace(lesson_name, "")
                                  .replace(teacher.text if teacher is not None else "", "")
                                  .replace(classroom.text if classroom is not None else "", "")
                                  .strip())

                    lesson = {
                        "lesson_name": lesson_name,
                        "teacher": teacher.text if teacher is not None else None,
                        "classroom": classroom.text if classroom is not None else None,
                        "additional": additional
                    }
                    day.append(lesson)
        res.append(day)
    return res

async def get_faculties_list():
    res = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto("https://isu.uust.ru/schedule_2024/")
            select_element = page.locator("#fac_choice")
            options = await select_element.locator("option").all()
            option_texts = [await option.text_content() for option in options]
            count = 0
            print("Start parsing faculties")
            for option in option_texts:
                if option != "Выберите факультет":
                    fac_name = option
                    fac_city = "Уфа"
                    if fac_name.find("Ишимбай") != -1:
                        fac_city = "Ишимбай"
                    if fac_name.find("Кумертау") != -1:
                        fac_city = "Кумертау"
                    if fac_name.find("Бирск") != -1:
                        fac_city = "Бирск"
                    if fac_name.find("Нефтекамск") != -1:
                        fac_city = "Нефтекамск"
                    if fac_name.find("Сибай") != -1:
                        fac_city = "Сибай"
                    if fac_name.find("Стерлитамак") != -1:
                        fac_city = "Стерлитамак"
                    res.append(Faculty(id=count, name=fac_name, city=fac_city))
                    count += 1
                    print(f"Parsed: {count}/{len(option_texts)}")
        except Exception as e:
            print(e)
        finally:
            return res

async def get_groups_list():
    res = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto("https://isu.uust.ru/schedule_2024/")
            select_element = page.locator("#search_select_group")
            options = await select_element.locator(".link-button").all()
            count = 0
            print("Start parsing groups")
            for option in options[1845:]:
                group_name = await option.text_content()

                await page.locator("#search_input_group").click()
                await option.click()
                try:
                    select_element = page.locator("#fac_choice").locator("option[selected]:not([disabled])")
                    group_faculty_name = await select_element.text_content()
                    group_faculty_id = await get_faculty_id_by_name(group_faculty_name)
                except:
                    group_faculty_id = 0
                select_element = page.locator("#course_choice").locator("option[selected]:not([disabled])")
                group_course = int(await select_element.text_content())
                res.append(Group(id=count, name=group_name, course=group_course, faculty_id=group_faculty_id))
                count += 1
                print(f"Parsed: {count}/{len(options)}")
        except Exception as e:
            print(e)
        finally:
            return res

async def main():
    pass

if __name__ == "__main__":
    asyncio.run(main())