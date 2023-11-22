import calendar

def convertMonthToNumber(date: str) -> str:
    [day, month] = date.split(' ')
    newDate: str = day + '.'
    months = calendar.month_name
    for i, other_month in enumerate(months):
        if month == other_month:
            if i > 10:
                return newDate + str(i)
            return newDate + '0'
        
def convertNamesToLowerCase(name: str) -> str:
    full_name = name.split()
    first_name = full_name[-1]
    surnames: list = full_name[:-1]
    # Oneliner that converts every capitalized surname to lowercase except the first character
    surnames_lower_case:list = list(map(lambda x: x[0] + x[1:].lower(), surnames))
    # Insert the first into the converted surname list to get a list representation of the full name
    surnames_lower_case.insert(0, first_name)
    # Join the list into a string seperated by whitespaces and return the name
    converted_name = " ".join(surnames_lower_case)
    return converted_name