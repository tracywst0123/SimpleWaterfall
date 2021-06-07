import numpy as np
import random


AdTypeList = {'tt_Native_Video': [0.001, 0.002, 0.003]}


class ID:
    def __init__(self, ad_id, floor, match_rate, adtype):
        """
        一个广告位ID

        :param floor: 底价 或 裸跑的预估价格
        :param match_rate: 预测的 match rate
        :param adtype: ['tt_Native_Video', 'gdt_Native_Image'] 注意每个库的video和image的返回时长也是不一样的
        """
        self.ad_id = ad_id
        self.floor = floor
        self.match_rate = match_rate
        self.adtype = adtype
        self.data = {'Request': 0,
                     'Matched': 0,
                     'Impression': 0}

    def generate_duration(self):
        dur_list = AdTypeList.get(self.adtype)
        duration = random.choice(dur_list)
        return duration

    def initiate_request(self):
        """
        :return: boolean of matched or not (1 for matched, 0 for no match);
                 ad returning duration
        """
        self.data['Request'] += 1
        matched = np.random.choice([1, 0], 1, p=[self.match_rate, 1-self.match_rate])

        if matched:
            self.data['Matched'] += 1

        return matched, self.generate_duration()

    def end_request(self, showed):
        if showed:
            self.data['Impression'] += 1

