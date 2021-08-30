import numpy as np

# algorithm for buying during market crash
def alg_01(stock_series, bond_series, stock_val, bond_val, 
            decr_perc, sell_perc, monthly_addn):
    """
    A single stock's current price maximum and current post-max 
    minimum are tracked. For each decrease in the risky asset price 
    of a certain percentage from its current maximum, a certain 
    percentage of bonds is sold and those funds are used 
    to purchase more of the risky asset

    Parameters
    ----------

    stock_series : pandas.core.series.Series
        A series of stock price data 

    bond_series : pandas.core.series.Series
        A series of bond price data 

    stock_val : float
        the current value of stock assets

    bond_val : float
        the current value of bond assets

    decr_perc : list
        A list of positive floats indicating at which percentage 
        decreases in the stock price from the current maximum 
        to sell the corresponding percentage of bonds and buy 
        more stock

    sell_perc : list
        A list of positive floats indicating the percentage of 
        current bonds to sell at the corresponding decrease 
        percentage in the stock 

    monthly_addn : float
        A monthly addition of captial to be added to 
        bond_value every 25 trading days

    Returns
    -------

    port_change : float
        A percentage representing the total change in value of the 
        portfolio

    """

    # assert percentages are valid
    assert all([0 < x and x < 100 for x in decr_perc])
    assert all([0 < x and x < 100 for x in sell_perc])

    # assert decrease and sell percentages are same size
    assert(len(decr_perc) == len(sell_perc))

    # assert stock price data and bond price data are the same length
    assert(stock_series.size == bond_series.size)

    # convert percentages to floats 
    decr_perc = [x/ 100 for x in decr_perc] 
    sell_perc = [x/ 100 for x in sell_perc] 


    # initialize current max, current min, current decrease,
    # current increase, portfolio value 
    s = stock_series.size
    max = stock_series[s-1]
    min = stock_series[s-1]
    current_decrease = 0.0
    init_port_val = stock_val + bond_val

    # loop over stock/bond price series, updating values 
    # keeping track of max and min
    for i in range(s-2, -1, -1):
        stock_change = stock_series[i]/stock_series[i+1] 
        stock_val = stock_val * stock_change
        bond_change = bond_series[i]/bond_series[i+1] 
        bond_val = bond_val * bond_change

        # monthly addition
        if i % 25 == 0:
            bond_val = bond_val + monthly_addn

        if stock_series.iloc[i] > max:
            max = stock_series.iloc[i]

        if stock_series.iloc[i] < min:
            min = stock_series.iloc[i]

            # if new decrease percentage is the same as first entry 
            # of input decrease percentages, buy and remove first entry
            current_decrease = 1 - min/max  # absolute value of percentage change
            while current_decrease > decr_perc[0]:
                sell_value = bond_val * sell_perc[0]
                bond_val = bond_val - sell_value
                stock_val = stock_val + sell_value
                decr_perc.pop(0)
                sell_perc.pop(0)
                
    fin_port_val = stock_val + bond_val
    port_change = fin_port_val/init_port_val - 1

    return port_change







#=============================================================================
#=============================================================================


# algorithm for buying on margin during market crash
def alg_02(series, margin_rate, margin, decrease_percentages, 
           decrease_buys, increase_percentages, increase_sells):
    """
    A single stock's current price maximum and current post-max 
    minimum are tracked. When the price decreases from its 
    current maximum by an initial percentage (initial_decrease), 
    an initial amount (initial_buy) of stock is bought on margin and 
    a fixed amount (uniform_buy) is continually bought for each 
    decrease by a specified percentage (uniform_decrease). When price 
    increases from its current minimum by an initial percentage 
    (initial_increase), an initial percentage (initial_sell) of margin-stock 
    is sold and a fixed percentage (uniform_sell) is continually 
    sold for each increase by a specified percentage (uniform_increase).

    Parameters
    ----------

    series : pandas.core.series.Series
        A series of price data

    margin_rate : float
        A positive percentage representing the margin rate 

    margin : float
        A positive number representing the amount of available margin 

    decrease_percentages : list
        A list of positive floats indicating at which percentage 
        decreases in the stock price from the current maximum to 
        buy on margin

    decrease_buys : list
        A list of positive floats indicating the percent of available 
        margin that is used to buy stock at the corresponding decrease percentage


    increase_percentages : list
        A list of positive floats indicating at which percentage 
        increases in the stock price from the current post-max 
        minimum to sell the margin-stock

    increase_sells : list
        A list of positive floats indicating the percent of the 
        current margin-stock equity that is sold  at the corresponding 
        increase percentage

    Returns
    -------

    return : float
        A percentage representing the return of the stock over 
        the given period of time using this algorithm

    """
    # assert percentages are valid
    assert all([0 < x and x < 100 for x in decrease_percentages])
    assert all([0 < x and x < 100 for x in decrease_buys])
    assert all([0 < x and x < 100 for x in increase_percentages])
    assert all([0 < x and x < 100 for x in increase_sells])

    # copy lists to not change originals
    decrease_percentages = decrease_percentages.copy()
    increase_percentages = increase_percentages.copy()

    # initialize current max, current min, current decrease,
    # current increase, margin-stock value 
    s = series.size
    max = series[s-1]
    min = series[s-1]
    current_decrease = 0.0
    current_increase = 0.0
    m_stock_val = 0.0

    # loop over series, keeping track of max and min
    for i in range(s-2, -1, -1):
        if series.iloc[i] > max:
            max = series.iloc[i]

        if series.iloc[i] < min:
            min = series.iloc[i]

            # if new decrease percentage is the same as first entry 
            # of input decrease percentages, buy and remove first entry
            current_decrease = (max - min) / max  # absolute value of percentage change
            while current_decrease > decrease_percentages[0]:
                m_stock_val = m_stock_val + decrease_buys[0] * margin / 100.0
                margin = margin - m_stock_val
                decrease_percentages.pop(0)

                # update money owed

    
