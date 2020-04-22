#!/usr/bin/python3
from browser import document
    
    
    
def judge():
    state = int(document["state"].value)
    
    kabu_low_value = 90
    kabu_high_value = 110
    
    initial_gensyou_lower_bound = int(kabu_low_value * 0.75)
    initial_gensyou_upper_bound = int(kabu_high_value * 0.81)
    
    initial_zouka_lower_bound = int(kabu_low_value * 0.9)
    initial_zouka_upper_bound = int(kabu_high_value * 1.4)
    
    initial_gekizou_lower_bound = int(kabu_low_value * 1.4)
    initial_gekizou_upper_bound = int(kabu_high_value * 2)

    if state == 0:
        document["result"].text = "これがもし、爆上げルートなら\n"
        kabuka = int(document["kabuka"].value)

        if initial_gensyou_lower_bound <= kabuka <= initial_zouka_lower_bound:
            document["result"].text += "減少状態、とりあえず午後を見てみよう"
            document["kabuka_text"].text = "火曜日の午後の株の価格"
            state = 3
        elif initial_zouka_lower_bound <= kabuka <= initial_gensyou_upper_bound:
            document["result"].text += "減少状態 or 増加状態、とりあえず午後をみよう"
            document["kabuka_text"].text = "火曜日の午後の株の価格"
            state = 3
        elif initial_gensyou_upper_bound <= kabuka <= initial_gekizou_lower_bound:
            document["result"].text += "増加状態、とりあえず午後をみよう"
            document["kabuka_text"].text = "火曜日の午後の株の価格"
            state = 1
        elif initial_gekizou_lower_bound <= kabuka <= initial_zouka_upper_bound:
            document["result"].text += "増加状態 or 激増状態"
            document["result"].text += "\n今日の午後と明日の朝みて、ピークじゃなければまた来週"
            state = 100
        elif initial_zouka_upper_bound <= kabuka <= initial_gekizou_uppder_bound:
            document["result"].text += "激増中, 午後がピークでしょう。じゃなければまた来週"
            state = 100
        else:
            document["result"].text += "あ、これ爆上げルートじゃない。また来週"
            state = 100
    elif state == 1:
        kabuka = int(document["kabuka"].value)
        if initial_gekizou_lower_bound <= kabuka <= initial_gekizou_upper_bound:
            document["result"].text = "明日の朝ピークかも"
            state = 2
        else:
            document["result"].text = "残念。また来週"
            state = 100
    elif state == 2:
        kabuka = int(document["kabuka"].value)
        if kabu_low_value * 2 <= kabuka <= kabu_high_value * 6:
            document["result"].text = "おめでとう。ピークだと思います"
            state = 100
        else:
            document["result"].text = "残念。爆上げはしません。また来週"
            state = 100
    elif state == 3:
        next_gensyou_lower_bound = initial_gensyou_lower_bound - kabu_low_value * 0.05
        next_gensyou_upper_bound = initial_gensyou_upper_bound - kabu_high_value * 0.03
        kabuka = int(document["kabuka"].value)

        if next_gensyou_lower_bound <= kabuka <= initial_zouka_lower_bound:
            document["result"].text = "減少中、木曜日の朝にしよう"
            document["kabuka_text"].text = "木曜日の朝の株の価格"
            state = 4
            
        elif next_gensyou_upper_bound <= tuee <= initial_zouka_upper_bound:
            document["result"].text = "増加状態、明日の午後がピークじゃなければ残念\n明日の午後にしよう"
            document["kabuka_text"].text = "水曜日の午後の株の価格"
            state = 6
        elif kabu_low_value * 2 <= tuee <= kabu_high_value * 6:
            document["result"].text = "ピークやん。早い。おめでとう"
            state = 100
        else:
            document["result"].text = "おかしいなあ。また来週"
            state = 100

    elif state == 4:
        
        next_gensyou_lower_bound = initial_gensyou_lower_bound - kabu_low_value * 0.2
        next_gensyou_upper_bound = initial_gensyou_upper_bound - kabu_high_value * 0.12
        
        kabuka = int(document["kabuka"].value)

        if next_gensyou_lower_bound <= kabuka <= next_gensyou_upper_bound:
            document["result"].text = "天国か地獄。土曜日の朝までとぼう"
            document["kabuka_text"].text = "土曜日の午前の株の価格"
            state = 5
        elif initial_zouka_lower_bound <= kabuka <= initial_zouka_upper_bound:
            document["result"].text = "明日の午後がピークかも。じゃなければ来週"
            state = 100
        elif initial_gekizou_lower_bound <= kabuka <= initial_gekizou_upper_bound:
            document["result"].text = "明日の朝がピークかも。じゃなければ来週"
            state = 100
            
    elif state == 5:

        kabuka = int(document["kabuka"].value)
        
        if kabu_low_value * 2 <= kabuka <= kabu_high_value * 6:
            document["result"].text = "おめでとう。ピークだよ。急いで時間を戻そう"
            state = 100
        else:
            document["result"].text = "ドンマイ。来週45%で爆上げくるから期待しよ"
            state = 100
    elif state == 6:
        kabuka = int(document["kabuka"].value)
        if kabu_low_value * 2 <= kabuka <= kabu_high_value * 6:
            document["result"].text = "おめでとう。ピークだと思います"
            state = 100
        else:
            document["result"].text = "残念。爆上げはしません。また来週"
            state = 100
    
    if state == 100:
        document["kabuka_text"].text = "火曜日の午前の株の価格"
        document["state"].value = 0
    else:
        document["state"].value = state
        
    document["kabuka"].value = ""

execute_btn = document["execute"]
execute_btn.bind("click", judge)