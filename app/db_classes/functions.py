import time


def secondsToDate(second, retMH=False):
    struct = time.localtime(second)
    if retMH:
        return time.strftime('%Y-%m-%d %H:%M', struct)
    return time.strftime('%Y-%m-%d', struct)


def timeAgo(second):
    second = int(second)
    if second < 60:
        if second >= 11 and second <= 20:
            return f"{int(second)} секунд назад"
        match second % 10:
            case 1:
                return f"{int(second)} секунду назад"
            case 2 | 3 | 4:
                return f"{int(second)} секунды назад"
            case 5 | 6 | 7 | 8 | 9 | 0:
                return f"{int(second)} секунд назад"
    if second < 60 * 60:
        if int(second / 60) >= 11 and int(second / 60) <= 20:
            return f"{int(second / 60)} минут назад"
        match int(second / 60) % 10:
            case 1:
                return f"{int(second / 60)} минуту назад"
            case 2 | 3 | 4:
                return f"{int(second / 60)} минуты назад"
            case 5 | 6 | 7 | 8 | 9 | 0:
                return f"{int(second / 60)} минут назад"
    if second < 60 * 60 * 60:
        if int(second / 60 / 60) >= 11 and int(second / 60 / 60) <= 20:
            return f"{int(second / 60 / 60)} часов назад"
        match int(second / 60 / 60):
            case 1:
                return f"{int(second / 60 / 60)} час назад"
            case 2 | 3 | 4:
                return f"{int(second / 60 / 60)} часа назад"
            case 5 | 6 | 7 | 8 | 9 | 0:
                return f"{int(second / 60 / 60)} часов назад"
    return secondsToDate(time.time() - second)
