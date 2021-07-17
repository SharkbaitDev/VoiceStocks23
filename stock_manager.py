from yahoo_fin import stock_info as si


def get_live_price(stock):
    return si.get_live_price(stock)


def get_day_gainers():
    return si.get_day_gainers()


def get_day_losers():
    return si.get_day_losers()


def get_most_active():
    return si.get_day_most_active()
