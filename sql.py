#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
# CGIモジュールをインポート
import cgi
import cgitb
import pandas as pd
import os
# sqlite3（SQLサーバ）モジュールをインポート
import sqlite3

cgitb.enable()

filename= "sdvx.csv"

csv_file = "sdvx_stats_kai2.csv"

# データベースファイルのパスを設定
dbname = 'sdvx_stats.db'
#dbname = ':memory:'

if not os.path.exists("sdvx_stats.db"):
    csv_f = pd.read_csv(csv_file, header = None, sep=",")
    rows = []
    for i in range(1, len(csv_f)):
        rows.append(list(csv_f.iloc[i]))
    # テーブルの作成
    # 同時にCSVファイルの中身を書き込む
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    create_table = 'create table if not exists sdvx_stats (music_title,difficulty_name,level,artist,count,played,comp,ex_comp,uc,per,grade_C,grade_B,grade_A,grade_Ap,grade_AA,grade_AAp,grade_AAA,grade_AAAp,grade_S,grade_995,grade_998,avg_score,sd_score,avg_skill_u8,avg_skill_9,avg_skill_10,avg_skill_11,avg_skill_12_n,avg_skill_12_g,avg_skill_12_h,avg_vf_u7,avg_vf_8_i_ii,avg_vf_8_iii_iv,avg_vf_9_i,avg_vf_9_ii,avg_vf_9_iii,avg_vf_9_iv,avg_vf_10_i,avg_vf_10_ii)'
    cur.execute(create_table)
    cur.executemany(
        "INSERT INTO sdvx_stats (music_title,difficulty_name,level,artist,count,played,comp,ex_comp,uc,per,grade_C,grade_B,grade_A,grade_Ap,grade_AA,grade_AAp,grade_AAA,grade_AAAp,grade_S,grade_995,grade_998,avg_score,sd_score,avg_skill_u8,avg_skill_9,avg_skill_10,avg_skill_11,avg_skill_12_n,avg_skill_12_g,avg_skill_12_h,avg_vf_u7,avg_vf_8_i_ii,avg_vf_8_iii_iv,avg_vf_9_i,avg_vf_9_ii,avg_vf_9_iii,avg_vf_9_iv,avg_vf_10_i,avg_vf_10_ii) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", rows)
    con.commit()
    cur.close()
    con.close()

# データベース上の列名と, 対応する表示名リスト
level_item_lis = ["level"]
level_item_lis_name = ["レベル"]
artist_item_lis = ["artist"]
artist_item_lis_name = ["作曲者"]
count_lis = ["count"]
count_lis_name = ["プレイ人数"]
avg_lis = ["avg_score"]
avg_lis_name = ["平均スコア"]
clear_lis = ["played","comp","ex_comp","uc","per"]
clear_lis_name = ["PLAYED","COMP","EX COMP","UC","PUC"]
grade_lis = ["grade_B","grade_A","grade_Ap","grade_AA","grade_AAp","grade_AAA","grade_AAAp","grade_S","grade_995","grade_998"]
grade_lis_name = ["B","A","A+","AA","AA+","AAA","AAA+","S","995","998"]
avg_vf_lis = ["avg_vf_u7","avg_vf_8_i_ii","avg_vf_8_iii_iv","avg_vf_9_i","avg_vf_9_ii","avg_vf_9_iii","avg_vf_9_iv","avg_vf_10_i","avg_vf_10_ii"]
avg_vf_lis_name = ["～アルジェント","エルドラ1, 2","エルドラ3, 4","クリムゾン1","クリムゾン2","クリムゾン3","クリムゾン4","インペリアル1","インペリアル2"]
avg_skill_lis = ["avg_skill_u8","avg_skill_9","avg_skill_10","avg_skill_11","avg_skill_12_n","avg_skill_12_g","avg_skill_12_h"]
avg_skill_lis_name = ["～雷電","魔騎士","剛力羅","或帝滅斗","無枠暴龍天","金枠暴龍天","後光暴龍天"]
difficulties_lis = ["NOVICE","ADVANCED","EXHAUST","MAXIMUM","INFINITE","GRAVITY","HEAVENLY","VIVID","EXCEED"]

# 列を取り出すSQL文を作る関数
def sql_make(item, lis):
    sql = ""
    if item == None:
        return sql
    for index in item:
        sql += lis[int(index)] + ", "
    return sql

# 表のヘッダー部分を作る関数
def resultscon_make(item, item_name, count, per_check):
    results_header = ""
    if item == None:
        return results_header
    for i in range(len(item)):
        index = item[i]
        if item_name == clear_lis_name or item_name == grade_lis_name:
            if per_check == "0":
                results_header += "<th class=con_num id=" + str(count+i) + ">" + item_name[int(index)] + "(人)</th>\n"
            else:
                results_header += "<th class=con_num id=" + str(count+i) + ">" + item_name[int(index)] + "(%)</th>\n"
        else:
            results_header += "<th class=con id=" + str(count+i) + ">" + item_name[int(index)] + "</th>\n"
    return results_header

def remove_lis_make(lis, num):
    if lis != None:
        if type(lis) == str:
            lis = [str(num)] + [lis]
        else:
           lis = [str(num)] + lis
    return lis

def application(environ,start_response):
    html = ""
    # 利用するHTMLファイルをすべて開く
    f = open('home.html', 'r', encoding="utf-8")
    f_r = open('result.html', 'r', encoding="utf-8")
    f_s = open('ss.html', 'r', encoding="utf-8")
    f_a = open('about.html', 'r', encoding="utf-8")
    f_re = open('remove.html', 'r', encoding="utf-8")
    # フォームデータを取得
    form = cgi.FieldStorage(environ=environ,keep_blank_values=True)
    if ('submit' not in form and 'ss_music' not in form and 'about' not in form and 'remove-submit' not in form):
        # 入力フォームの内容が空の場合（初めてページを開いた場合も含む）
        
        # HTML(入力フォーム部分)
        while (True):
            line = f.readline()
            if line == "":
                break
            html += line
            
        con = sqlite3.connect(dbname)
        cur = con.cursor()
        con.text_factory = str
            
        page_data = {}
        page_data['results'] = ""
        page_data['results_header'] = "<tr>\n<th class = con id='-2'>RANK</th>\n<th class = con id='-1'>動画</th>\n<th class = con id='0'>楽曲名</th>\n<th class = con id='1'>難易度</th>\n"
            
        # トップページに載せる平均スコアランキングを作成
        sql = "SELECT music_title, difficulty_name, level, artist, avg_score, avg_vf_10_i, avg_skill_12_h FROM sdvx_stats " \
            + "WHERE (difficulty_name = 'EXHAUST' OR difficulty_name = 'MAXIMUM' OR difficulty_name = 'GRAVITY' OR difficulty_name = 'INFINITE' OR difficulty_name = 'HEAVENLY' OR difficulty_name = 'VIVID' OR difficulty_name = 'EXCEED') AND (level = '17' OR level = '18' OR level = '19' OR level = '20') " \
            + "ORDER BY avg_score ASC LIMIT 0, 10"
         
        # レベル, 作曲者, 全体の平均スコア, インペリアル1の平均スコア, 後光暴龍天の平均スコアをヘッダーに登録
        for item, item_lis in zip([[0], [0], [0], [7], [6]], [level_item_lis_name, artist_item_lis_name, avg_lis_name, avg_vf_lis_name, avg_skill_lis_name]):
            page_data['results_header'] += resultscon_make(item, item_lis, 0, 0)
        page_data['results_header'] += '</tr>\n'
        
        # 検索結果から表を作成
        cnt_rank = 0
        for row in cur.execute(sql):
            page_data['results'] += '<tr>\n'
            cnt_rank += 1
            for i in range(len(row)):
                if i == 0:
                    # 最初の列に順位, 次の列に動画, その次の列に楽曲名を追加
                    page_data['results'] += '<td class = rank>' +  str(cnt_rank) + '</td>\n'
                    page_data['results'] += '<td class = data_video><a href="https://www.youtube.com/results?search_query=' \
                                            + str(row[i]) \
                                            + '+sdvx"><img src="https://zodiac-18.github.io/zod.github.io/jikken/img/yt_icon.png" alt="動画" width="24" height="16" border="0"></a>'
                    page_data['results'] += '<td class = data' + str(i) + '>' \
                                        + str(row[i]) \
                                        + '</td>\n'
                elif i == 1:
                    page_data['results'] += '<td class = ' + str(row[i]) + '>' \
                                            + str(row[i]) \
                                            + '</td>\n'   
                else:
                    page_data['results'] += '<td class = data' + str(i) + '>' \
                                        + str(row[i]) \
                                        + '</td>\n'
        page_data['results'] += '</tr>\n'
        
        # 結果部分のHTML出力
        for key, value in page_data.items():
            html = html.replace('{% ' + key + ' %}', value)

        # カーソルと接続を閉じる
        cur.close()
        con.close()
        
    # 参考文献ページ(about.html)に遷移時
    elif ('about' in form):
        while (True):
                line = f_a.readline()
                if line == "":
                    break
                html += line

    # 偏差値計算ページに遷移時
    elif ('ss_music' in form):
        # 初期状態
        if ('submit' not in form):
            while (True):
                line = f_s.readline()
                if line == "":
                    break
                html += line
            
            # 偏差値計算の対象となる楽曲名を取得
            ss_music = form.getvalue("ss_music")

            page_data = {}
            page_data['ss_music'] = '"' + "".join(ss_music) + '"'
            page_data['results'] = "<p>スコアを入力してください。</p>\n"
            page_data['results_table'] = ""
            
            for key, value in page_data.items():
                html = html.replace('{% ' + key + ' %}', value)
        
        # スコア送信後
        else:   
            con = sqlite3.connect(dbname)
            cur = con.cursor()
            con.text_factory = str
            
            while (True):
                line = f_s.readline()
                if line == "":
                    break
                html += line
                
            difficulties=count=clear=grade=avg=avg_vf=avg_skill=music_name=level=level_two=artist=level_item=artist_item=[]
            # 偏差値計算を行う難易度
            ss_difficulty = form.getvalue("ss_difficulty")
                
            item_all = [level_item, artist_item, count, clear, grade, avg, avg_vf, avg_skill]
            item_lis = [level_item_lis, artist_item_lis, count_lis, clear_lis, grade_lis, avg_lis, avg_vf_lis, avg_skill_lis]
            item_lis_name = [level_item_lis_name, artist_item_lis_name, count_lis_name, clear_lis_name, grade_lis_name, avg_lis_name, avg_vf_lis_name, avg_skill_lis_name]
            all_item = [list(range(len(level_item_lis))),list(range(len(artist_item_lis))),list(range(len(count_lis))), list(range(len(clear_lis))), list(range(len(grade_lis))), list(range(len(avg_lis))), list(range(len(avg_vf_lis))), list(range(len(avg_skill_lis)))]
            
            # 偏差値計算の対象となる楽曲名と入力されたスコアを取得
            ss_music = form.getvalue("ss_music")
            ss_score = form.getvalue("ss_score")
                
            page_data = {}
            page_data['ss_music'] = '"' + "".join(ss_music) + '"'
            page_data['results'] = "<h3>あなたの偏差値は "
            page_data['results_table'] = "<table id='result_table'>\n<thead>\n<th class = con>楽曲名</th>\n<th class = con>難易度</th>\n"
            
            # 0~10,000,000までの数値以外や文字が入力された場合のフラグ
            error = False
            try:
                ss_score = int(ss_score)
                if ss_score < 0 or ss_score > 10000000:
                    error = True
                    page_data['results'] = "<h3>スコアは0～10,000,000の範囲で入力してください。</h3>\n"
            except ValueError:
                error = True
                page_data['results'] = "<h3>スコアは数値で入力してください。</h3>\n"
            
            # 楽曲名, 難易度名, プレイ人数は必ず検索する
            sql = "SELECT music_title, difficulty_name, count, "
            
            # SQL文とヘッダー作り
            item_all = all_item
            for item, item_lis, item_name in zip(item_all, item_lis, item_lis_name):
                if item != "count":
                    add_sql = sql_make(item, item_lis)
                    sql += add_sql
                    page_data['results_table'] += resultscon_make(item, item_name, 0, "0")
                
            page_data['results_table'] += "</tr>\n<tbody>\n"
            
            sql = sql.rstrip().rstrip(',')
            sql_add_diff = "'" + difficulties_lis[int(ss_difficulty)] + "'"
            if ss_difficulty == "3":
                sql_add_diff = "'MAXIMUM' OR difficulty_name = 'INFINITE' OR difficulty_name = 'GRAVITY' OR difficulty_name = 'HEAVENLY' OR difficulty_name = 'VIVID' OR difficulty_name = 'EXCEED'"
            sql_music = " from sdvx_stats WHERE (music_title like '%" + ss_music + "%') AND (difficulty_name = " + sql_add_diff + ")"          
            sql += sql_music
            
            sd_score_sql = "SELECT sd_score from sdvx_stats WHERE (music_title like '%" + ss_music + "%') AND (difficulty_name = " + sql_add_diff + ")"
            
            # 検索結果から表を作成
            for row in cur.execute(sql):
                page_data['results_table'] += '<tr>\n'
                for i in range(len(row)):
                    if i == 1:
                        page_data['results_table'] += '<td class = ' + str(row[i]) + '>' \
                                                + str(row[i]) \
                                                + '</td>\n'
                    elif i != 2:
                        page_data['results_table'] += '<td class = data' + str(i) + '>' \
                                                + str(row[i]) \
                                                + '</td>\n'
                    if i == 1:
                        view_diff = row[i]
                    if i == 21:
                        avg_score = int(row[i])
            
            page_data['results_table'] += '</tr>\n</tbody>\n</table>\n'
            for row in cur.execute(sd_score_sql):
                sd_score = int(row[0])
                #標準偏差が0(=スコア登録がない)の場合偏差値が産出できない
                if sd_score == 0:
                    error = True
                    page_data['results'] = "<h3>[ERROR]スコアデータがないため計算できません。</h3>\n"
            
            # 問題が発生しなければ偏差値を出力
            if not error:
                tscore = (int(ss_score)-avg_score)/sd_score*10+50
                page_data['results'] += str(tscore) + ' です。</h3>\n<h4>"' + ss_music + '" [' + view_diff + '] の統計データ</h4>\n'
            # 発生した場合は統計データのみ出力
            else:
                page_data['results'] += '<h4>"' + ss_music + '" [' + view_diff + '] の統計データ</h4>\n'
            cur.close()
            con.close()
            
            for key, value in page_data.items():
                html = html.replace('{% ' + key + ' %}', value)
        
    elif ('remove-submit' in form):
        con = sqlite3.connect(dbname)
        cur = con.cursor()
        con.text_factory = str
        
        while (True):
            line = f_re.readline()
            if line == "":
                break
            html += line

        remove_null = True
        remove_music_NOV = remove_lis_make(form.getvalue("remove_music_NOVICE"), 0)
        remove_music_ADV = remove_lis_make(form.getvalue("remove_music_ADVANCED"), 1)
        remove_music_EXH = remove_lis_make(form.getvalue("remove_music_EXHAUST"), 2)
        remove_music_MXM = remove_lis_make(form.getvalue("remove_music_MAXIMUM"), 3)
        remove_music_INF = remove_lis_make(form.getvalue("remove_music_INFINITE"), 4)
        remove_music_GRV = remove_lis_make(form.getvalue("remove_music_GRAVITY"), 5)
        remove_music_HVN = remove_lis_make(form.getvalue("remove_music_HEAVENLY"), 6)
        remove_music_VVD = remove_lis_make(form.getvalue("remove_music_VIVID"), 7)
        remove_music_XCD = remove_lis_make(form.getvalue("remove_music_EXCEED"), 8)

        remove_music_lis = [remove_music_NOV, remove_music_ADV, remove_music_EXH, remove_music_MXM, remove_music_INF, remove_music_GRV, remove_music_HVN, remove_music_VVD, remove_music_XCD]

        for remove_music in remove_music_lis:
            if remove_music != None:
                remove_null = False
                break

        page_data = {}
        if not remove_null:
            page_data['music_name'] = '<ul>\n'
            sql = 'DELETE from sdvx_stats WHERE ('
            for remove_music in remove_music_lis:
                if not remove_music == None:
                    if len(remove_music) > 2:
                        for music in remove_music[1:]:
                            remove_diff = difficulties_lis[remove_music_lis.index(remove_music)]
                            music = music.replace("'", "''")
                            sql += "music_title LIKE '" + music + "' AND difficulty_name = '" + remove_diff + "') OR ("
                            music = music.replace("''", "'")
                            page_data['music_name'] += '<li>' + music + ' [' + remove_diff + ']</li>\n'
                    else:
                        music = remove_music[1]
                        music = music.replace("'", "''")
                        remove_diff = difficulties_lis[remove_music_lis.index(remove_music)]
                        sql += "music_title LIKE '" + music + "' AND difficulty_name = '" + remove_diff + "') OR ("
                        music = music.replace("''", "'")
                        page_data['music_name'] += '<li>' + music + ' [' + remove_diff + ']</li>\n'
            page_data['music_name'] += '</ul>\n'
            sql = sql.rstrip("OR (")

            """
            テスト用
            sql_test = sql.lstrip("DELETE")
            sql_test = "SELECT *" + sql_test

            for row in cur.execute(sql_test):
                print(row)

            print("実行したSQL_TEST文\n")
            print(sql_test + "\n")
            """

            print("実行したSQL文\n")
            print(sql + "\n")
            cur.execute(sql)

            """
            テスト用
            for row in cur.execute(sql_test):
                print(row)
            """

            page_data['music_name'] += '<p>以上の譜面の統計データを削除しました。</p>\n'

        else:
            page_data['music_name'] = '<h3>【エラー】削除する譜面を選択してください。</h3>\n'

        con.commit()
        cur.close()
        con.close()
        
        for key, value in page_data.items():
            html = html.replace('{% ' + key + ' %}', value)
        
    else:
        # 入力フォームの内容が空でない場合

        # フォームデータから各フィールド値を取得
        #
        
        con = sqlite3.connect(dbname)
        cur = con.cursor()
        con.text_factory = str
        
        # 検索フィルタと表示項目取得
        difficulties = form.getvalue("difficulty")
        count = form.getvalue("count")
        clear = form.getvalue("clear")
        grade = form.getvalue("grade")
        avg = form.getvalue("avg")
        avg_vf = form.getvalue("avg_vf")
        avg_skill = form.getvalue("avg_skill")
        music_name = form.getvalue("music_name")
        # レベル1～10の取得
        level = form.getvalue("level")
        # レベル11～20の取得
        level_two = form.getvalue("level_two")
        artist = form.getvalue("artist")
        level_item = form.getvalue("level_item")
        artist_item = form.getvalue("artist_item")
        per_check = form.getvalue("percentage")
        
        # 表示項目のリスト, 表示項目を種類ごとにまとめたリスト, 表示項目リストの名前のリスト
        item_all = [level_item, artist_item, count, clear, grade, avg, avg_vf, avg_skill]
        item_lis = [level_item_lis, artist_item_lis, count_lis, clear_lis, grade_lis, avg_lis, avg_vf_lis, avg_skill_lis]
        item_lis_name = [level_item_lis_name, artist_item_lis_name, count_lis_name, clear_lis_name, grade_lis_name, avg_lis_name, avg_vf_lis_name, avg_skill_lis_name]
        all_item = [list(range(len(level_item_lis))),list(range(len(artist_item_lis))),list(range(len(count_lis))), list(range(len(clear_lis))), list(range(len(grade_lis))), list(range(len(avg_lis))), list(range(len(avg_vf_lis))), list(range(len(avg_skill_lis)))]
        
        #HTMLに追加するHTML文
        page_data = {}
        page_data['results'] = ""
        page_data['results_header'] = "<tr>\n"
        
        search_filter = True
        all_con = False
        # 表示項目の指定がなければ列すべて指定, あれば楽曲名と難易度名の列追加
        if not any(item_all):
            all_con = True
            
        sql = "SELECT music_title, difficulty_name, count, "
        con_temp = ["youtube", "music_title", "difficulty_name", "count"]
        
        # テーブルのヘッダーにあらかじめ動画, 楽曲名, 難易度を追加する
        page_data['results_header'] += "<th class = con id='0'>動画</th>\n<th class = con id='1'>楽曲名</th>\n<th class = con id='2'>難易度</th>\n"
        
        # SQL文の作成(列指定)
        count = 3
        count_check = False
        if all_con:
            item_all = all_item
        for item, item_lis, item_name in zip(item_all, item_lis, item_lis_name):
            if item != "count":
                add_sql = sql_make(item, item_lis)
                sql += add_sql
                temp = add_sql.rstrip().rstrip(',')
                if temp != "":
                    temp = temp.replace(" ","").split(',')
                    con_temp += temp
            if item == "count":
                count_check = True
            page_data['results_header'] += resultscon_make(item, item_name, count, per_check)
            if item != None:
                count += len(item)
        
        # 人数表示と%表示がある列のインデックス取得
        check_lis = []
        for i in range(len(con_temp)):
            name = con_temp[i]
            if any(map(name.__contains__, ("played","comp","ex_comp","uc","per","grade_B","grade_A","grade_Ap","grade_AA","grade_AAp","grade_AAA","grade_AAAp","grade_S","grade_995","grade_998"))):
                check_lis.append(i-1)
        
        sql = sql.rstrip().rstrip(',')
        
        page_data['results_header'] += "<th class = con>削除</th>\n</tr>\n"
        
        if difficulties == None and music_name == "" and artist == "" and level == None and level_two == None:
            search_filter = False
            sql += ' from sdvx_stats'
        else:
            sql += ' from sdvx_stats WHERE ('
        
        # SQL文の作成(条件指定)
        if search_filter:
            if difficulties != None:
                sql_difficulty = ""
                for i in range(len(difficulties)):
                    sql_difficulty += 'difficulty_name = ' + "\"" + difficulties_lis[int(difficulties[i])] + "\""
                    if i != len(difficulties) - 1:
                        sql_difficulty += ' OR '
                sql += sql_difficulty
                sql += ")"
            if music_name != "":
                if difficulties != None:
                    sql += " AND ("
                music_name = music_name.replace("'", "''")
                sql_music = "music_title like '%" + music_name + "%'"
                music_name = music_name.replace("''", "'")
                sql += sql_music
                sql += ")"
            if artist != "":
                if difficulties != None or music_name != "":
                    sql += " AND ("
                sql_artist = "artist like '%" + artist + "%'"
                sql += sql_artist
                sql += ")"
            if level != None or level_two != None:
                if difficulties != None or music_name != "" or artist != "":
                    sql += " AND ("
                sql_level = ""
                if level != None:
                    for i in range(len(level)):
                        sql_level += 'level = ' + "\"" + str(int(level[i])+1) + "\""
                        if i != len(level) - 1 or level_two != None:
                            sql_level += ' OR '
                if level_two != None:
                    for i in range(len(level_two)):
                        sql_level += 'level = ' + "\"" + str(int(level_two[i])+11) + "\""
                        if i != len(level_two) - 1:
                            sql_level += ' OR '
                sql += sql_level
                sql += ")"
                
        # 結果部分のHTML作成
        while (True):
            line = f_r.readline()
            if line == "":
                break
            html += line
               
        print("\n実行したSQL文\n" + sql + "\n")
        
        count_num = -1
        cnt_data = 0
        # 検索結果の表の作成
        for row in cur.execute(sql):
            cnt_data += 1
            page_data['results'] += '<tr>'
            minus = False
            for i in range(len(row)):
                if minus == True and i > 2:
                    j = i-1
                else:
                    j = i
                if i == 2:
                    count_num = int(row[i])
                if i == 0:
                    page_data['results'] += '<td class = data_video id = "0"><a href="https://www.youtube.com/results?search_query=' \
                                            + str(row[i]) \
                                            + '+sdvx"><img src="https://zodiac-18.github.io/zod.github.io/jikken/img/yt_icon.png" alt="動画" width="24" height="16" border="0"></a>'
                    page_data['results'] += '<td class = data' + str(i) + ' id = "1"' \
                                            + '><a href = "/?ss_music=' \
                                            + str(row[i]) \
                                            + '" class = data>' \
                                            + str(row[i]) \
                                            + '</a></td>\n'
                elif i == 1:
                    page_data['results'] += '<td class = ' + str(row[i]) + ' id = ' \
                                            + str(j+1) \
                                            + '>' \
                                            + str(row[i]) \
                                            + '</td>\n'                  
                elif i in check_lis:
                    # %表示用の計算
                    percent = round(int(row[i])/count_num*100, 3)
                    # 人数表示の場合
                    if per_check == "0":
                        page_data['results'] += '<td class = data' + str(i) + 'id = ' \
                                                    + str(j+1) \
                                                    + '>' \
                                                    + str(row[i]) \
                                                    + '</td>\n'
                    # %表示の場合
                    else:
                        # 1.00%以下なら色付け
                        if percent <= 1.00:
                            # 0%以上0.10%以下なら赤文字で表示
                            if 0 < percent <= 0.10:
                                page_data['results'] += '<td class = color id = ' \
                                                    + str(j+1) \
                                                    + '>' \
                                                    + str(percent) \
                                                    + '</td>\n'
                            # 0%(=スコア登録がない場合)は黒い太文字で表示
                            elif percent == 0.0:
                                page_data['results'] += '<td class = bold id = ' \
                                                    + str(j+1) \
                                                    + '>' \
                                                    + str(percent) \
                                                    + '</td>\n'
                            # 0.10%より大きく, 1.00%以下なら青文字で表示
                            else:
                                page_data['results'] += '<td class = color_blue id = ' \
                                                    + str(j+1) \
                                                    + '>' \
                                                    + str(percent) \
                                                    + '</td>\n'
                        # 1.00%より大きいなら色付けしない(黒文字).
                        else:
                            page_data['results'] += '<td class = data' + str(i) + ' id = ' \
                                                    + str(j+1)\
                                                    + '>' \
                                                    + str(percent) \
                                                    + '</td>\n'
                else:
                    # プレイ人数を表示しない場合IDの値を調整
                    if i == 2 and count_check == False:
                        minus = True
                        pass
                    else:
                        page_data['results'] += '<td class = data' + str(i) + ' id = ' \
                                            + str(j+1) \
                                            + '>' \
                                            + str(row[i]) \
                                            + '</td>\n'
            if i == len(row)-1:
                page_data['results'] += '<td class = remove onclick="getElementById(\'checkbox' + str(cnt_data) + '\').click();">\n<input type="checkbox" id="checkbox' + str(cnt_data) + '" name="remove_music_' + str(row[1]) + '" value="' \
                                    + str(row[0])\
                                    + '" onclick="this.click()">\n</td>'
            page_data['results'] += '</tr>\n'

        
        # 結果部分のHTML出力
        for key, value in page_data.items():
            html = html.replace('{% ' + key + ' %}', value)

        # カーソルと接続を閉じる
        cur.close()
        con.close()
        
    html = html.encode('utf-8')

    # レスポンス
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8'),
        ('Content-Length', str(len(html))) ])
    return [html]


# リファレンスWEBサーバを起動
#  ファイルを直接実行する（python3 test_wsgi.py）と，
#  リファレンスWEBサーバが起動し，http://localhost:8080 にアクセスすると
#  このサンプルの動作が確認できる．
#  コマンドライン引数にポート番号を指定（python3 test_wsgi.py ポート番号）した場合は，
#  http://localhost:ポート番号 にアクセスする．
    
from wsgiref import simple_server
if __name__ == '__main__':
    port = 8080
    if len(sys.argv) == 2:
        port = int(sys.argv[1])

    server = simple_server.make_server('', port, application)
    server.serve_forever()