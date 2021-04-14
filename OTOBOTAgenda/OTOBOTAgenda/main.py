from importlib import import_module as im

string_matching = im('string_matching')

Date = string_matching.Date
Task = string_matching.Task
print(string_matching.COURSE_REGEX)
