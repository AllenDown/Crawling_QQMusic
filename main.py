#! /usr/bin/env python
# -*- coding: utf-8 -*-
from get_all_singers import urls, get_singers
import database
import get_music_info
import pprint
import requests
import database
from multiprocessing import Pool
import time

# get all singer information in the QQMusic
# if __name__ == "__main__":     
#     for url in urls:
#         get_singers(url)



# get all song_mid and album_mid in order to get the details of all songs
# if __name__ == '__main__':
#     singer_list = database.get_sheet('QQMusic', 'singer_list')
#     pool = Pool(4)
#     count = 0
#     while True:
#         try:
#             print('crawled singers : ', count)
#             # get 100 datas by once
#             data_list = []
#             datas = list(singer_list.find({}, {'_id': 0, 'Fsinger_mid': 1}).limit(100))
#             if len(datas) > 0:
#                 print('if start')
#                 time.sleep(2)
#                 for data in datas:
#                     data_list.append(data['Fsinger_mid'])
#                 pool.map(get_music_info.get_song_album_id, data_list)
#             else:
#                 break
#             count = count + 100
#         except:
#             continue


# get all song infomation from song and album ids
if __name__ == '__main__':
    song_album_id_list = database.get_sheet('QQMusic', 'song_album_id_list')
    pool = Pool(4)
    count = 0
    while True:
        try:
            print('crawled songs : ', count)
            # get 100 datas by once
            datas = list(song_album_id_list.find({}, {'_id': 0}).limit(100))
            if len(datas) > 0:
                pool.map(get_music_info.get_item_info, datas)
            else:
                break
            count = count + 100
        except:
            continue