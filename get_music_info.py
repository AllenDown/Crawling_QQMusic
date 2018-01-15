#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import database
import time

song_album_id_list = database.get_sheet('QQMusic', 'song_album_id_list')
delete_singer = database.get_sheet('QQMusic', 'singer_list')
song_item_info = database.get_sheet('QQMusic', 'song_item_info')


# get all songs from one singer and insert into database
def get_song_album_id(Fsinger_mid):
    print(Fsinger_mid)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'referer': 'https://y.qq.com/n/yqq/singer/{}.html'.format(Fsinger_mid)
    }
    begin = 0
    all_songs = []
    while True:
        # one page url with 30 songs or less
        url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg?g_tk=1964444483&jsonpCallback=MusicJsonCallbacksinger_track&loginUin=707813012&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&singermid={}&order=listen&begin={}&num=30&songstatus=1'.format(Fsinger_mid, begin)
        web_data = ''
        while web_data == '':
            try:
                web_data = requests.get(url, headers=headers)
            except:
                print('bad network, let us sleep for 5 seconds')
                time.sleep(5)
                continue
        # songs in one page
        songs = json.loads(web_data.text.lstrip(' MusicJsonCallbacksinger_track(').rstrip(' )'))['data']['list']
        if len(songs) != 0:
            for song in songs:
                data = {
                    'songmid': song['musicData']['songmid'],
                    'albummid': song['musicData']['albummid']
                }
                all_songs.append(data)
        else:
            break
        begin = begin + 30
    if len(all_songs) > 0:
        song_album_id_list.insert_many(all_songs)
        delete_singer.delete_one({'Fsinger_mid': Fsinger_mid})
    else:
        delete_singer.delete_one({'Fsinger_mid': Fsinger_mid})


# get all information from one song
def get_item_info(song):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'referer': 'https://y.qq.com/n/yqq/song/{}.html'.format(song['songmid'])
    }
    song_url = 'https://c.y.qq.com/v8/fcg-bin/fcg_play_single_song.fcg?songmid={}&tpl=yqq_song_detail&format=jsonp&callback=getOneSongInfoCallback&g_tk=1964444483&jsonpCallback=getOneSongInfoCallback&loginUin=707813012&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'.format(
        song['songmid'])
    album_url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_album_info_cp.fcg?albummid={}&g_tk=1964444483&jsonpCallback=getAlbumInfoCallback&loginUin=707813012&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'.format(song['albummid'])
    song_data = ''
    album_data = ''
    while song_data == '':
        try:
            song_data = requests.get(song_url, headers=headers)
        except:
            print('bad network, let us sleep for 5 seconds')
            time.sleep(5)
            continue
    while album_data == '':
        try:
            album_data = requests.get(album_url, headers=headers)
        except:
            print('bad network, let us sleep for 5 seconds')
            time.sleep(5)
            continue
    song_item = ''
    album_item = ''
    if song['songmid'] != '':
        song_item = json.loads(song_data.text.lstrip('getOneSongInfoCallback(').rstrip(')'))
    else:
        pass
    # print('song:', song_item)
    # some songs haven't album attr
    if song['albummid'] != '':
        album_item = json.loads(album_data.text.lstrip(' getAlbumInfoCallback(').rstrip(')'))
    else:
        pass
    # print('album', album_item)
    data = {
        "title": song_item['data'][0]['title'] if song_item['data'][0]['title'] else None,
        "singer": song_item['data'][0]['singer'] if song_item['data'][0]['singer'] else None,
        "total_song_num": album_item['data']['total_song_num'] if album_item['data']['total_song_num'] else None,
        "album": song_item['data'][0]['album']['title'] if song_item['data'][0]['album']['title'] else None,
        "date": song_item['data'][0]['time_public'] if song_item['data'][0]['time_public'] else None,
        "company": album_item['data']['company'] if album_item['data']['company'] else None,
        "language": album_item['data']['lan'] if album_item['data']['lan'] else None,
        "genre": album_item['data']['genre'] if album_item['data']['genre'] else None,
        "url": song_item['data'][0]['url'] if song_item['data'][0]['url'] else None,
        "songmid": song['songmid'] if song['songmid'] else None,
        "albummid": song['albummid'] if song['albummid'] else None
    }
    print(data)
    song_item_info.insert_one(data)
    song_album_id_list.delete_one({'songmid': song['songmid']})





