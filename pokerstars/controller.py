from pokerstars.config import fold_position
from pokerstars.config import call_position
from pokerstars.config import raise_position
from pokerstars.config import label_position
from pokerstars.config import window_close, sitout_confirm, join_game
from pokerstars.config import BB, SB
import pymouse
import pyscreenshot
import pykeyboard
import random
import time
import json

class Controller():
    def __init__(self, game_driver):
        self.m = pymouse.PyMouse()
        self.game_driver = game_driver

    def sit_out(self):
        m = self.m#{{{
        m.click(window_close[0], window_close[1], 1)
        time.sleep(0.5)
        m.click(sitout_confirm[0], sitout_confirm[1], 1)
        time.sleep(3)
        m.click(join_game[0], join_game[1], 1)#}}}

    def fold(self):
        m = self.m#{{{
        with open('pokerstars/last_control.json') as f:
            last_control = json.load(f)
        if time.time() - last_control < 1.5:
            return
        xr = round((random.random()-0.5)*50)
        yr = round((random.random()-0.5)*30)
        xp = fold_position[0] + xr
        yp = fold_position[1] + yr
        im = pyscreenshot.grab()
        fold_mark = 0
        while fold_mark == 0:
            for xchange in xrange(-20, 20):
                for ychange in xrange(-20, 20):
                    color = im.getpixel((fold_position[0]+xchange, fold_position[1]+ychange))
                    if color[0] > max(color[1:]) + 30:
                        fold_mark = 1
                        break
            im = pyscreenshot.grab()
        m.click(xp, yp)
        with open('pokerstars/last_control.json', 'w') as f:
            last_control = time.time()
            f.write(json.dumps(last_control))#}}}

    def call(self):
        def all_in():#{{{
            im = pyscreenshot.grab()
            for i in xrange(-20, 20):
                for j in xrange(-20, 20):
                    x = call_position[0] + i
                    y = call_position[1] + j
                    color = im.getpixel((x, y))
                    if color[0] > max(color[1:]) + 20:
                        return 0
            return 1
        with open('pokerstars/last_control.json') as f:
            last_control = json.load(f)
        if time.time() - last_control < 1.5:
            return
        m = self.m 
        all_in_mark = all_in()
        xr = round((random.random()-0.5)*50)
        yr = round((random.random()-0.5)*30)
        if not all_in_mark:
            xp = call_position[0] + xr
            yp = call_position[1] + yr
        else:
            xp = raise_position[0] + xr
            yp = raise_position[1] + yr
        m.click(xp, yp)
        with open('pokerstars/last_control.json', 'w') as f:
            last_control = time.time()
            f.write(json.dumps(last_control))#}}}

    def rais(self, amount):
        m = self.m#{{{ 
        with open('pokerstars/last_control.json') as f:
            last_control = json.load(f)
        if time.time() - last_control < 1.5:
            return
        amount = round(amount/BB)*BB
        if amount / self.game_driver.stack[0] > 0.6:
            amount = int(self.game_driver.stack[0]) + 1
        m = pymouse.PyMouse()
        k = pykeyboard.PyKeyboard()
        lxp = label_position[0]
        lyp = label_position[1]
        xp = raise_position[0]
        yp = raise_position[1]
        m.click(lxp+10, lyp)
        time.sleep(1)
        m.press(lxp+10, lyp, 1)
        m.move(lxp-300, lyp)
        m.release(lxp-300, lyp, 1)
        time.sleep(0.5)
        string = str(amount)
        for ch in string:
            k.tap_key(ch)
        time.sleep(0.5)
        with open('pokerstars/last_control.json', 'w') as f:
            last_control = time.time()
            f.write(json.dumps(last_control))
        m.click(xp, yp)#}}}

    def get_back(self):
        back_position = [raise_position[0], raise_position[1]-20]
        self.m.click(*back_position)
