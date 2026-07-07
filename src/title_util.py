def extract_title(markdown):
    index = markdown.find("#")
    if index == -1:
        raise Exception("No h1 title found.")
    title_walker = index + 2
    title = ""
    while markdown[title_walker] != " ":
        title += markdown[title_walker]
        title_walker += 1
    return title