import pandas
from AdID import ID

Answer_duration = 0.0005


def request_group(g):
    parallel = g.get('parallel_count')
    id_list = g.get('id_list')
    group_duration = 0

    if parallel == 1:
        for ad in id_list:
            group_duration += Answer_duration
            matched_boolean, dur = ad.initiate_request()
            if matched_boolean:
                return ad, group_duration + dur

    elif parallel == 2:
        for i, k in zip(id_list, id_list[1:]):
            group_duration += Answer_duration
            matched_boolean1, dur1 = i.initiate_request()
            matched_boolean2, dur2 = k.initiate_request()

            if matched_boolean1 and matched_boolean2:
                if dur1 < dur2:
                    return i, group_duration + dur1
                else:
                    return k, group_duration + dur2

            elif matched_boolean1:
                return i, group_duration + dur1
            elif matched_boolean2:
                return k, group_duration + dur2
    else:
        raise Exception('parallel_count_error')

    return None, group_duration


class Waterfall:
    group_list = []
    # parallel_list = []
    current_matched_ad = None

    def insert_group(self, parallel_count=1):
        group_id = len(self.group_list)
        group_cur = {'group_id': group_id, 'parallel_count': parallel_count, 'id_list': []}
        self.group_list.append(group_cur)

    def insert_id(self, group_id, ad_id, floor, match_rate, adtype):
        id_cur = ID(ad_id, floor, match_rate, adtype)
        self.group_list[group_id]['id_list'].extend([id_cur])

    def request_waterfall(self):
        duration = 0
        for g in self.group_list:

            matched_ad, dur = request_group(g)
            duration += dur
            if matched_ad is not None:
                self.current_matched_ad = matched_ad
                return matched_ad, duration

        return None, duration

    def return_impression(self, success):
        self.current_matched_ad.end_request(success)
        self.current_matched_ad = None

    def generate_structure(self):
        COL = ['group_ID', 'parallel_count', 'ad_ID', 'type', 'eCPM', 'o_match_rate']
        waterfall_structure = pandas.DataFrame(columns=COL)
        if self.group_list is None:
            return waterfall_structure

        for g in self.group_list:

            group_ID = g.get('group_id')
            parallel_count = g.get('parallel_count')
            ad_list = g.get('id_list')

            for ad in ad_list:
                if ad is None:
                    continue
                ad_id = ad.ad_id
                ad_type = ad.adtype
                eCPM = ad.floor
                o_match_rate = ad.match_rate

                waterfall_structure.loc[len(waterfall_structure)] = [group_ID, parallel_count, ad_id,
                                                                     ad_type, eCPM, o_match_rate]

        return waterfall_structure

    def generate_data(self):
        COL = ['group_ID', 'parallel_count', 'ad_ID', 'type', 'eCPM', 'o_match_rate', 'request', 'matched',
               'impression', 'match_rate', 'show_rate', 'fill_rate', 'revenue']
        waterfall_data = pandas.DataFrame(columns=COL)

        if self.group_list is None:
            return waterfall_data

        for g in self.group_list:

            group_ID = g.get('group_id')
            parallel_count = g.get('parallel_count')
            ad_list = g.get('id_list')

            for ad in ad_list:
                if ad is None:
                    continue
                ad_id = ad.ad_id
                ad_type = ad.adtype
                eCPM = ad.floor
                o_match_rate = ad.match_rate

                data = ad.data
                request = data.get('Request')
                matched = data.get('Matched')
                impression = data.get('Impression')

                if request > 0:
                    match_rate = matched/request
                    fill_rate = impression/request
                else:
                    match_rate = 0
                    fill_rate = 0

                if matched > 0:
                    show_rate = impression/matched
                else:
                    show_rate = 0

                revenue = (eCPM * impression)/1000

                waterfall_data.loc[len(waterfall_data)] = [group_ID, parallel_count, ad_id, ad_type, eCPM,
                                                           o_match_rate, request, matched, impression, match_rate,
                                                           show_rate, fill_rate, revenue]

        return waterfall_data


