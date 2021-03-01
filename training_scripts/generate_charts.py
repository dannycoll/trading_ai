from numpy import genfromtxt
import matplotlib.pyplot as plt
import mpl_finance
import numpy as np
import uuid
import datetime

#initial data file
pd = genfromtxt('./eurusd.csv', delimiter=',' ,dtype=str)

#target directories for the two categories
buy_dir = './data/train/buy/'
sell_dir = './data/train/sell/'

comp_ratios = []

def graphwerk(start, finish):
    #initialise variables
    open = []
    high = []
    low = []
    close = []
    volume = []
    date = []
    date_time = 0
    day = 0
    day_str = ''
    HA_open = []
    HA_close = []
    HA_high = []
    HA_low = []
    #get chart values for each position in the range
    for x in range(finish-start):
        cur_open = float(pd[start][1])
        open.append(cur_open)
        cur_high = float(pd[start][2])
        high.append(cur_high)
        cur_low = float(pd[start][3])
        low.append(cur_low)
        cur_close = float(pd[start][4])
        close.append(cur_close)
        cur_volume = float(pd[start][5])
        volume.append(cur_volume)
        if x == 0:
            cur_HA_open = (cur_open + cur_close) /2
        else:
            cur_HA_open = (HA_open[-1] + HA_close[-1]) /2
        HA_open.append(cur_HA_open)
        cur_HA_close = (cur_open + cur_close + cur_high + cur_low)/4
        HA_close.append(cur_HA_close)
        cur_HA_high = max([cur_HA_close, cur_HA_open, cur_high])
        HA_high.append(cur_HA_high)
        cur_HA_low = min([cur_HA_close, cur_HA_open, cur_low])
        HA_low.append(cur_HA_low)
        
        #change date string into a day of the week
        date.append(pd[start][0])
        date_time = pd[start][0]
        split = date_time.split(' ')
        date_split = split[0].split('.')
        day = datetime.datetime(int(date_split[2]), int(date_split[1]), int(date_split[0])).weekday()
        day_str = num_to_day(day)
        start = start + 1

        close_next = (float(pd[finish][4])+float(pd[finish][1])+float(pd[finish][2])+float(pd[finish][3]))/4

    fig = plt.figure(num=1, figsize=(3, 3), dpi=50, facecolor='white')
    dx = fig.add_subplot(111)
    plt.axis('off')
    mpl_finance.candlestick2_ochl(dx, HA_open, HA_close, HA_high, HA_low, width=1, colorup='g', colordown='r', alpha=1)

    plt.autoscale()
    plt.axis('off')
    comp_ratio = close_next / HA_close[-1]
    if (comp_ratio < 0.998 or comp_ratio > 1.002):
        if HA_close[-1] > close_next:
            print('close value is bigger')
            print('last value: ' + str(HA_close[-1]))
            print('next value: ' + str(close_next))
            print('sell')

            plt.savefig(sell_dir + day_str + str(uuid.uuid4()) +'.jpg', bbox_inches='tight')
        else:
            print('close value is smaller')
            print('last value: '+ str(HA_close[-1]))
            print('next value: ' + str(close_next))
            print('buy')
            plt.savefig(buy_dir + day_str + str(uuid.uuid4())+'.jpg', bbox_inches='tight')

    #clear all arrays
    open.clear()
    close.clear()
    volume.clear()
    high.clear()
    low.clear()
    HA_close.clear()
    HA_high.clear()
    HA_low.clear()
    HA_open.clear()
    plt.cla()
    plt.clf()

#convert number between 0-6 to a day of the week
def num_to_day(num):
    switcher = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday',
    }
    return switcher.get(num, "nothing")

#create all graphs
def generate_graphs():
    iter_count = int(len(pd)/4)
    print(iter_count)
    iter = 0

    for x in range(len(pd)-12):
        graphwerk(iter, iter+12)
        iter = iter + 2

    plot_comp_ratios()

#plot the comp_ratio values
def plot_comp_ratios():
    for x in range(len(pd)-1):
        close = float(pd[x][4])
        close_next = float(pd[x+1][4])
        comp_ratio = close_next / close
        if (comp_ratio < 0.998 or comp_ratio > 1.002):
            comp_ratios.append(comp_ratio)
    plt.plot(comp_ratios, 'o', color='k')
    print(len(comp_ratios))
    plt.savefig('./comp_ratios.jpg')
