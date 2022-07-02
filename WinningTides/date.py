def is_dst(dt):
    from datetime import datetime, timedelta
    import pytz
    timeZone = pytz.timezone("Europe/London")
    aware_dt = timeZone.localize(dt)
    if aware_dt.dst() != timedelta(0,0):
        dt = dt + timedelta(hours=1)
        return str(dt) + " (BST)"
    else: 
       
        return str(dt) + " (UTC)"