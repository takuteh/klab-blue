import datetime

def setFileNameByTime():
    # 現在時刻の取得
    dt_now = datetime.datetime.now()
    year = str(dt_now.year)
    month = str(dt_now.month).zfill(2)
    day = str(dt_now.day).zfill(2)
    hour = str(dt_now.hour).zfill(2)
    minute = str(dt_now.minute).zfill(2)
    second = str(dt_now.second).zfill(2)

    # 1桁目だけ取得
    microsecond = str(dt_now.microsecond)[0]

    return year + '-' + month + '-' + day + '-' + hour + '-' + minute + '-' + second + '-' + microsecond