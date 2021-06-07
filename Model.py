from AdPlacement import Waterfall

# Configurations: 返回match/no-match这个log信息的时长, ---在AdPlacement里更改
#                 每个广告类型的加载时长,  ---在AdID里更改
#                 每个预加载时机的等待时长, ---wait_time
#                 每个展示chance的预加载时机, ---preload
#                 展示chance ---chance

# type 可能的时长list，or range(start, stop, step), 需要到AdPlacement里更改
AdTypeList = {'tt_Native_Video': [0.001, 0.002, 0.003]}

preload = 2
chance = 500
wait_time = [0.008, 0.01]


waterfall = Waterfall()

waterfall.insert_group(1)
waterfall.insert_group(1)
waterfall.insert_group(1)

waterfall.insert_id(0, 'a', 10, 0.4, 'tt_Native_Video')
waterfall.insert_id(1, 'b', 8, 0.3, 'tt_Native_Video')
waterfall.insert_id(1, 'c', 7, 0.2, 'tt_Native_Video')
waterfall.insert_id(2, 'a', 6, 0.5, 'tt_Native_Video')
waterfall.insert_id(2,  'a', 5, 0.9, 'tt_Native_Video')
waterfall.insert_id(2, 'a', 4, 0.9, 'tt_Native_Video')

# final_structure = waterfall.generate_structure()
#
# print(final_structure)

for c in range(chance):
    for i in range(preload):
        mached_ad, dur = waterfall.request_waterfall()
        success = False
        if mached_ad is not None:
            if wait_time[i] > dur:
                success = True
            waterfall.return_impression(success)
            break


final_data = waterfall.generate_data()

print(final_data)

final_data.to_excel('final_data.xlsx')
