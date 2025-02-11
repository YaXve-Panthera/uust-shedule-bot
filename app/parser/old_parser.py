


def get_group_names():
    try:
        search_element = driver.find_element(By.ID, "search_input_group")
        search_element.click()
        group_names_element = driver.find_element(By.ID, "search_select_group").find_elements(By.CLASS_NAME, "link-button")
        print("element found")
    finally:
        print("quit")
    group_names = []
    for elem in group_names_element:
        group_names.append(elem.text)

    print(group_names)
    print(len(group_names))

def get_faculty_names():
    try:
        fac_element = Select(driver.find_element(By.ID, "fac_choice"))
        fac_names_elements = fac_element.options
        print("element found")
    finally:
        print("quit")

    fac_names = []
    for elem in fac_names_elements:
        if elem.text != "Выберите факультет":
            fac_names.append(elem.text)

    print(fac_names)
    print(len(fac_names))
    return fac_names

def get_courses_of_faculty(fac_name):
    courses_names_element = []
    try:
        fac_element = Select(driver.find_element(By.ID, "fac_choice"))
        fac_element.select_by_visible_text(fac_name)

        course_element = Select(driver.find_element(By.ID, "course_choice"))
        courses_names_element = course_element.options
        print("elements found")
    except:
        print("troubles in " + fac_name)
    courses_names = []
    for elem in courses_names_element:
        if elem.text != "Выберите курс":
            courses_names.append(elem.text)

    print(courses_names)
    print(len(courses_names))
    return courses_names

def get_groups(course):
    groups_names_element = []
    try:
        course_element = Select(driver.find_element(By.ID, "course_choice"))
        course_element.select_by_visible_text(course)

        group_element = Select(driver.find_element(By.ID, "group_choice"))
        groups_names_element = group_element.options
        print("elements found")
    except:
        print("troubles in " + course)
    groups_names = []
    for elem in groups_names_element:
        if elem.text != "Выберите группу":
            groups_names.append(elem.text)

    print(groups_names)
    print(len(groups_names))
    return groups_names

def get_groups_json():
    with open("data.json", "w") as fh:
        json.dump([1, 2, 3, 4, 5], fh)
