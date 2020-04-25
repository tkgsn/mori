#!/usr/bin/python3
from browser import document

def write_result(text):
    document["result"].text = text
    
day2ind = {"tuem": 2, "tuee":3, "wedm":4, "wede":5, "thum":6, "thue":7, "frim":8, "frie":9, "satm":10, "sate":11}
ind2day = {value: key for key, value in day2ind.items()}
day2text = {"tuem":"火曜日", "tuee":"火曜日", "wedm":"水曜日", "wede":"水曜日", "thum":"木曜日", "thue":"木曜日", "frim":"金曜日", "frie":"金曜日", "satm":"土曜日", "sate":"土曜日"}
    
def step(n_step, day):
    return ind2day[day2ind[day] + n_step]
    
def test():
    document["kabuka1"].readOnly = True
    
def judge():
    
    reset = False

    
    kabu_low_value = 90
    kabu_high_value = 110
    
    gensyou_lower_bound_fn = lambda day: kabu_low_value * (0.85 - 0.05 * day2ind[day])
    gensyou_upper_bound_fn = lambda day: kabu_high_value * (0.95 - 0.03 * day2ind[day])
    zouka_lower_bound = int(kabu_low_value * 0.9)
    zouka_upper_bound = int(kabu_high_value * 1.4)
    gekizou_lower_bound = int(kabu_low_value * 1.4)
    gekizou_upper_bound = int(kabu_high_value * 2)
    peak_lower_bound = kabu_low_value * 2
    peak_upper_bound = kabu_high_value * 6
    
    judge_gensyou = lambda day, kabuka: gensyou_lower_bound_fn(day) <= kabuka <= gensyou_upper_bound_fn(day)
    judge_zouka = lambda kabuka: zouka_lower_bound <= kabuka <= zouka_upper_bound 
    judge_gekizou = lambda kabuka: gekizou_lower_bound <= kabuka <= gekizou_upper_bound
    judge_peak = lambda kabuka: peak_lower_bound <= kabuka <= peak_upper_bound
    
    def switch(time):
        if time == "morning":
            kabuka1_field.readOnly = False
            kabuka2_field.readOnly = True
        else:
            kabuka1_field.readOnly = True
            kabuka2_field.readOnly = False
        
    
    def compute_possible_states(day, kabuka):
        return [judge_gensyou(day, kabuka), judge_zouka(kabuka), judge_gekizou(kabuka), judge_peak(kabuka)]
    
    def compute_intersection(vec1, vec2):
        return [elm1 * elm2 for elm1, elm2 in zip(vec1, vec2)]
    
    def infer_next_state(vec, day="tuem"):
        if day == "thue":
            return [0, vec[0], vec[1], vec[2]]
        else:
            return [vec[0], vec[0], vec[1], vec[1]]
        
    kabuka1_field = document["kabuka1"]
    kabuka2_field = document["kabuka2"]
    
    state = int(document["state"].value)
    day = document["day"].value
    
    kabuka1 = None
    kabuka2 = None
    
    if kabuka1_field.readOnly == False:
        if kabuka1_field.value == "":
            write_result("何か入力してくれ！おつかれ")
            return
        try:
            kabuka1 = int(kabuka1_field.value)
        except:
            write_result("半角数字で入力してくれ！おつかれ")
            return
    else:
        try:
            kabuka1 = int(kabuka1_field.value)
        except:
            pass
        
    if kabuka2_field.readOnly == False:
        if kabuka2_field.value == "":
            write_result("何か入力してくれ！おつかれ")
            return
        try:
            kabuka2 = int(kabuka2_field.value)
        except:
            write_result("半角数字で入力してくれ！おつかれ")
            return
    else:
        try:
            kabuka2 = int(kabuka2_field.value)
        except:
            pass
        
    if kabuka1 is None and kabuka2 is not None:
        kabuka1 = kabuka2
    
    if sum(compute_possible_states(day, kabuka1)) == 0:
        write_result("今週は跳ねないな！おつかれ")
        state = 100
    elif state == 0:
        morning_judge_vec = compute_possible_states(day[:3] + "m", kabuka1)
        evening_judge_vec = compute_possible_states(day[:3] + "e", kabuka2)
        inference_evening_judge_vec = infer_next_state(morning_judge_vec)
        intersection = compute_intersection(evening_judge_vec, inference_evening_judge_vec)
        
        print(intersection)
        
        if sum(intersection) == 0:
            write_result("今週は跳ねないな！おつかれ")
            state = 100
            
        if sum(intersection) == 1:
            if intersection[0] == 1:
                if day == "thue":
                    write_result("…天国か地獄だ！土曜日の午前の株価をみてみろ!おつかれ")
                    day = "satm"
                    state = 2
                else:
                    write_result("減少状態だ！明後日の午前の株価を見るんだ！おつかれ")
                    day = "thum"
                    state = 2
            elif intersection[1] == 1:
                write_result("増加状態だ！明日の午後がピークかもしれないな！おつかれ")
                n_step = 2
                day = step(n_step, day)
                reset = True
                state = 1
            elif intersection[2] == 1:
                write_result("激増状態だ！明日の午前がピークかもしれないよ！おつかれ")
                day = "wedm"
                state = 1
            else:
                write_result("ピークじゃないか！おつかれ")
                state = 100
        if sum(intersection) == 2:
            if intersection[0] == intersection[1] == 1:
                write_result("減少状態か増加状態だ！明日の午前の株価を見るんだ！おつかれ")
                n_step = 1
                day = step(n_step, day)
                state = 3
            elif intersection[1] == intersection[2] == 1:
                write_result("増加状態か激増状態だ！明日の午前か午後にピークがくるかもしれないぞ！おつかれ")
                day = "wedm"
                state = 1
            elif intersection[2] == intersection[3] == 1:
                n_step = 1
                day = step(n_step, day)
                write_result("激増状態かピークだ！これで満足するなら終わりだ！明日の午前に跳ねる可能性もあるぞ！おつかれ")
                state = 1
    elif state == 1:
        if judge_peak(kabuka1) and kabuka1 >= gekizou_upper_bound:
            write_result("ピークじゃないか!おつかれ")
            state = 100
        else:
            write_result("残念だな！また来週だ！おつかれ")
            state = 100
    elif state == 2:
        if judge_peak(kabuka1):
            if kabuka1 <= gekizou_upper_bound:
                write_result("ピークか！？これで満足するなら終わりだ！午後に跳ねる可能性もあるが、下がる可能性もあるな！どっちかはわからない！おつかれ")
                n_step = 1
                day = step(n_step, day)
                state = 1
            else:
                write_result("ピークだ！おつかれ")
                state = 100
        else:
            write_result("午後の株価を見てくれ！おつかれ")
            day = "thue"
            state = 0
    elif state == 3:
        write_result("午後も入力してみてくれ！おつかれ")
        day = day[:3] + "e"
        state = 0
        
        
            
    if state == 100:
        document["day"].value = "tuem"
        document["state"].value = 3
        day = "tuem"
    else:
        document["state"].value = state
        document["day"].value = day
    

    kabuka2_field.value = ""
        
    if day[3] == "m":
        kabuka1_field.value = ""
        switch("morning")
    else:
        switch("evening")
        
    if reset:
        kabuka1_field.value = ""
        reset = False
        
    document["day_text"].text = day2text[day]
    
    
"""
def judge_():
    
    if document["kabuka"].value == "":
        document["result"].text = "何か入力してください"
        return
    
    try:
        kabuka = int(document["kabuka"].value)
    except:
        document["result"].text = "半角数字で入力してください"
        return
    
    day2ind = {"tuem": 2, "tuee":3, "wedm":4, "wede":5, "thum":6, "thue":7}
    
    state = int(document["state"].value)
    
    kabu_low_value = 90
    kabu_high_value = 110
    
    gensyou_lower_bound_fn = lambda day: kabu_low_value * (0.85 - 0.05 * day2ind[day])
    gensyou_upper_bound_fn = lambda day: kabu_high_value * (0.95 - 0.03 * day2ind[day])
    initial_zouka_lower_bound = int(kabu_low_value * 0.9)
    initial_zouka_upper_bound = int(kabu_high_value * 1.4)
    initial_gekizou_lower_bound = int(kabu_low_value * 1.4)
    initial_gekizou_upper_bound = int(kabu_high_value * 2)
    peak_lower_bound = kabu_low_value * 2
    peak_upper_bound = kabu_high_value * 6
    
    judge_gensyou = lambda day, kabuka: gensyou_lower_bound_fn(day) <= kabuka <= gensyou_upper_bound_fn(day)
    judge_zouka = lambda kabuka: zouka_lower_bound <= kabuka <= zouka_upper_bound 
    judge_gekizou = lambda kabuka: gekizou_lower_bound <= kabuka <= gekizou_upper_bound
    judge_peak = lambda kabuka: peak_lower_bound <= kabuka <= peak_upper_bound
    
    def compute_possible_states(day, kabuka):
        return [judge_gensyou(day, kabuka), judge_zouka(kabuka), judge_gekizou(kabuka), judge_peak(kabuka)]
    
    def compute_intersection(vec1, vec2):
        return [elm1 | elm2 for elm1, elm2 in zip(vec1, vec2)]
    
    def infer_next_state(vec, day="tuem"):
        if day == "thue":
            return [0, vec[0], vec[1], vec[2]]
        else:
            return [vec[0], vec[0], vec[1], vec[1]]
    
    morning_kabuka = 
    evening_kabuka = 
    
    if state == 0:
        morning_judge_vec = compute_possible_states("tuem", morning_kabuka)
        evening_judge_vec = compute_possible_states("tuee", evening_kabuka)
        inference_evening_judge_vec = infer_next_state(morning_judge_vec)
        intersection = compute_intersection(evening_judge_vec, inference_evening_judge_vec)
        
        if sum(intersection) == 0:
            print("今週は跳ねないよ！おつかれ")
        
        
    if state == 0:
        document["result"].text = "これがもし、爆上げルートなら\n"

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
        elif initial_zouka_upper_bound <= kabuka <= initial_gekizou_upper_bound:
            document["result"].text += "激増中, 午後がピークでしょう。じゃなければまた来週"
            state = 100
        else:
            document["result"].text += "あ、これ爆上げルートじゃない。また来週"
            state = 100
    elif state == 1:
        if initial_gekizou_lower_bound <= kabuka <= initial_gekizou_upper_bound:
            document["result"].text = "明日の朝ピークかも"
            state = 2
        else:
            document["result"].text = "残念。また来週"
            state = 100
    elif state == 2:
        if kabu_low_value * 2 <= kabuka <= kabu_high_value * 6:
            document["result"].text = "おめでとう。ピークだと思います"
            state = 100
        else:
            document["result"].text = "残念。爆上げはしません。また来週"
            state = 100
    elif state == 3:
        next_gensyou_lower_bound = initial_gensyou_lower_bound - kabu_low_value * 0.05
        next_gensyou_upper_bound = initial_gensyou_upper_bound - kabu_high_value * 0.03

        if next_gensyou_lower_bound <= kabuka <= initial_zouka_lower_bound:
            document["result"].text = "減少中、木曜日の朝にしよう"
            document["kabuka_text"].text = "木曜日の朝の株の価格"
            state = 4
            
        elif initial_zouka_lower_bound <= kabuka <= next_gensyou_upper_bound:
            document["result"].text = "増加か減少状態。運が悪い。明日の朝を見てみよう"
            document["kabuka_text"].text = "水曜日の朝の株の価格"
            state = 7
            
        elif next_gensyou_upper_bound <= kabuka <= initial_zouka_upper_bound:
            document["result"].text = "増加状態、明日の午後がピークじゃなければ残念\n明日の午後にしよう"
            document["kabuka_text"].text = "水曜日の午後の株の価格"
            state = 6
        elif kabu_low_value * 2 <= kabuka <= kabu_high_value * 6:
            document["result"].text = "ピークやん。早い。おめでとう"
            state = 100
        else:
            document["result"].text = "おかしいなあ。また来週"
            state = 100

    elif state == 4:
        next_gensyou_lower_bound = initial_gensyou_lower_bound - kabu_low_value * 0.2
        next_gensyou_upper_bound = initial_gensyou_upper_bound - kabu_high_value * 0.12

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
    elif state == 7:
        
        next_gensyou_lower_bound = initial_gensyou_lower_bound - kabu_low_value * 0.1
        next_gensyou_upper_bound = initial_gensyou_upper_bound - kabu_high_value * 0.06
        
        if next_gensyou_lower_bound <= kabuka <= initial_zouka_lower_bound:
            document["result"].text = "減少状態、明日の朝を見てみよう"
            state = 4
        elif initial_zouka_lower_bound <= kabuka <= initial_gekizou_lower_bound:
            document["result"].text = "増加状態、明日の午前がピーク"
            state = 100
        elif initial_gekizou_lower_bound <= kabuka <= initial_zouka_upper_bound:
            document["result"].text = "増加状態か激増状態、今日の午後を見てみよう"
            document["kabuka_text"].text = "水曜日の午後の株価"
            state = 8
        elif initial_zouka_upper_bound <= kabuka <= initial_gekizou_upper_bound:
            document["result"].text = "激増状態、今日の午後がピーク"
            state = 100
            
    elif state == 8:
        
        if initial_gekizou_lower_bound <= kabuka <= initial_gekizou_upper_bound:
            document["result"].text = "激増"
            document["kabuka_text"].text = "木曜日の午前の株価"
            state = 8
        
    
    if state == 100:
        document["kabuka_text"].text = "火曜日の午前の株の価格"
        document["state"].value = 0
    else:
        document["state"].value = state
        
    document["kabuka"].value = ""
"""

    
execute_btn = document["execute"]
execute_btn.bind("click", judge)