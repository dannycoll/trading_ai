import os
import shutil
import random

current_dir = './data/train'

target_dir = './data/validate'

#If training model for specific days this function will sort the training data from buy/sell folders within
# the multiple day folders
def sort_from_days():
    for folder in os.listdir(current_dir):
        if folder == 'buy' or folder == 'sell':
            pass
        else:
            day_dir = os.path.join(current_dir, folder)
            for buy_or_sell in os.listdir(day_dir):
                buy_or_sell_dir = os.path.join(day_dir, buy_or_sell)
                for img in os.listdir(buy_or_sell_dir):
                    chance = random.randint(1,5)
                    if chance == 4:
                        shutil.move(
                            os.path.join(buy_or_sell_dir, img),
                            os.path.join(target_dir,folder,buy_or_sell,img)
                        )

#If training all the data together, this will just sort from 2 folders, buy & sell
def sort_from_buysell():
    for buy_or_sell in os.listdir(current_dir):
        buy_or_sell_dir = os.path.join(current_dir,buy_or_sell)
        for img in os.listdir(buy_or_sell_dir):
                    chance = random.randint(1,5)
                    if chance == 4:
                        shutil.move(
                            os.path.join(buy_or_sell_dir, img),
                            os.path.join(target_dir,buy_or_sell,img)
                        )