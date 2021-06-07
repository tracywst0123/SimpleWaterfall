import numpy as np
from AdPlacement import Waterfall
from AdID import ID


if __name__ == '__main__':
    w = Waterfall()

    w.insert_group(1)

    w.insert_id(0, 'absc', 2, 0.2, 'tt_Native_Video')

    print(w.group_list)

