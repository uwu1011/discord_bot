def isDateValid(date):
    date_list = date.split("/")
    try:
        year = int(date_list[0])
        month = int(date_list[1].lstrip("0"))
        day = int(date_list[2].lstrip("0"))
    except:
        return 1
    if len(date_list) != 3 or not((str(year) and str(month) and str(day)).isdigit()):
        return 1
    if len(date_list[1]) != 2 or len(date_list[2]) != 2:
        return 1
    else:
        if month == 0 or month > 12:
            return 2
        else:
            if month == 2:
                if (year % 4 == 0 and year % 100 != 0) or (year % 4 == 0 and year % 100 == 0 and year % 400==0):
                    if day == 0 or day > 29:
                        return 3
                    else:
                        return 4
                else:
                    if day == 0 or day > 28:
                        return 3
                    else:
                        return 4
            elif month in [1,3,5,7,8,10,12]:
                if day == 0 or day > 31:
                    return 3
                else:
                    return 4
            else:
                if day == 0 or day > 30:
                    return 3
                else:
                    return 4