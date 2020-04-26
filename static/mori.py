#!/usr/bin/python3
from browser import document

def write_result(text):
    document["result"].text = text
    
day2ind = {"tuem": 2, "tuee":3, "wedm":4, "wede":5, "thum":6, "thue":7, "frim":8, "frie":9, "satm":10, "sate":11}
ind2day = {value: key for key, value in day2ind.items()}
day2text = {"tuem":"火曜日午前", "tuee":"火曜日午後", "wedm":"水曜日午前", "wede":"水曜日午後", "thum":"木曜日午前", "thue":"木曜日午後", "frim":"金曜日午前", "frie":"金曜日午後", "satm":"土曜日午前", "sate":"土曜日午後"}
    
def step(n_step, day):
    return ind2day[day2ind[day] + n_step]

    
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
            
            kabuka1_text.style = {"opacity": 1}
            kabuka2_text.style = {"opacity": 0.3}
        else:
            kabuka1_field.readOnly = True
            kabuka2_field.readOnly = False
            
            kabuka1_text.style = {"opacity": 0.3}
            kabuka2_text.style = {"opacity": 1}
        
    
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
    
    kabuka1_text = document["kabuka_text1"]
    kabuka2_text = document["kabuka_text2"]
    
    state = int(document["state"].value)
    day = document["day"].value
    
    kabuka1 = None
    kabuka2 = None
    
    if kabuka1_field.readOnly == False:
        if kabuka1_field.value == "":
            write_result("何か入力してくれ。おつかれ")
            return
        try:
            kabuka1 = int(kabuka1_field.value)
        except:
            write_result("半角数字で入力してくれ。おつかれ")
            return
    else:
        try:
            kabuka1 = int(kabuka1_field.value)
        except:
            pass
        
    if kabuka2_field.readOnly == False:
        if kabuka2_field.value == "":
            write_result("何か入力してくれ。おつかれ")
            return
        try:
            kabuka2 = int(kabuka2_field.value)
        except:
            write_result("半角数字で入力してくれ。おつかれ")
            return
    else:
        try:
            kabuka2 = int(kabuka2_field.value)
        except:
            pass
        
    if kabuka1 is None and kabuka2 is not None:
        kabuka1 = kabuka2
    
    if sum(compute_possible_states(day, kabuka1)) == 0:
        write_result("今週は跳ねないぞ。おつかれ")
        state = 100
    elif state == 0:
        morning_judge_vec = compute_possible_states(day[:3] + "m", kabuka1)
        evening_judge_vec = compute_possible_states(day[:3] + "e", kabuka2)
        inference_evening_judge_vec = infer_next_state(morning_judge_vec)
        intersection = compute_intersection(evening_judge_vec, inference_evening_judge_vec)
        
        print(intersection)
        
        if sum(intersection) == 0:
            write_result("今週は跳ねないぞ。おつかれ")
            state = 100
            
        if sum(intersection) == 1:
            if intersection[0] == 1:
                if day == "thue":
                    write_result("明後日の午前が底かピークだ。株価を入力してくれ。おつかれ")
                    n_step = 3
                    day = step(n_step, day)
                    state = 1
                else:
                    write_result("減少状態だな。明後日の午前の株価を入力してくれ。おつかれ")
                    n_step = 3
                    day = step(n_step, day)
                    state = 2
            elif intersection[1] == 1:
                write_result("増加状態だな。明日の午後がピークかもしれない。おつかれ")
                n_step = 2
                day = step(n_step, day)
                reset = True
                state = 1
            elif intersection[2] == 1:
                write_result("激増状態だな。明日の午前がピークかもしれないな。おつかれ")
                n_step = 1
                day = step(n_step, day)
                state = 1
            else:
                write_result("ピークだな。おつかれ")
                state = 100
        if sum(intersection) == 2:
            if intersection[0] == intersection[1] == 1:
                write_result("減少状態か増加状態だな。明日の午前の株価を入力してくれ。おつかれ")
                n_step = 1
                day = step(n_step, day)
                state = 3
            elif intersection[1] == intersection[2] == 1:
                write_result("増加状態か激増状態だ。明日の午前か午後にピークがくるかもしれないな。おつかれ")
                n_step = 1
                day = step(n_step, day)
                state = 1
            elif intersection[2] == intersection[3] == 1:
                n_step = 1
                day = step(n_step, day)
                write_result("激増状態かピークだな。ピークかもしれないが、明日の午前に跳ねる可能性もあるな。おつかれ")
                state = 1
    elif state == 1:
        if judge_peak(kabuka1) and kabuka1 >= gekizou_upper_bound:
            write_result("ピークだな。おつかれ")
            state = 100
        else:
            write_result("残念だな。おつかれ")
            state = 100
    elif state == 2:
        if judge_peak(kabuka1):
            if kabuka1 <= gekizou_upper_bound:
                write_result("ピークかもな。これで満足するなら終われ。午後に跳ねる可能性もあるが、下がる可能性もあるからな。どっちかはわからない。おつかれ")
                n_step = 1
                day = step(n_step, day)
                state = 1
            else:
                write_result("ピークだな。おつかれ")
                state = 100
        else:
            write_result("午後の株価を入力してくれ。おつかれ")
            n_step = 1
            day = step(n_step, day)
            state = 0
    elif state == 3:
        write_result("午後の株価を入力してくれ。おつかれ")
        day = day[:3] + "e"
        state = 0
        
        
            
    if state == 100:
        document["day"].value = "tuem"
        document["state"].value = 3
        document["result"].text += "。さっ、次の火曜日、午前の株価を入力してくれ。おつかれ"
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
    
execute_btn = document["execute"]
execute_btn.bind("click", judge)