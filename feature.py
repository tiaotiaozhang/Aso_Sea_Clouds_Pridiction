#!usr/bin/python3
# -*- coding: utf-8 -*-
#----------------------------------------
# name: feature
# purpose: 雲海出現を予測するために必要な特徴量を作成する
# author: Katsuhiro MORISHITA, 森下功啓
# created: 2015-08-08
# lisence: MIT
#----------------------------------------
#地点A　阿蘇山頂, 地点B　阿蘇乙姫
import datetime
import timeKM


index_B = {"時刻":0, "降水量":1, "気温":2, "風速":3, "風向":4, "日照時間":5}
index_A = {"時刻":0, "現地気圧":1, "海面気圧":2, "降水量":3, "気温":4, "露点温度":5, "蒸気圧":6, "湿度":7, "風速":8, "風向":9, "日照時間":10, "全天日射量":11, "降雪":12, "積雪":13, "天気":14, "雲量":15, "視程":16}


def get_season(_date, weather_data_A, weather_data_B):
	""" 日付けをシーズン化したもの
	"""
	return int((_date - datetime.datetime(_date.year, 1, 1)).total_seconds() / (7 * 24 * 3600))


def get_temperature14_pointB(_date, weather_data_A, weather_data_B):
	""" 前日の14時の気温　地点B
	最高気温代わり
	"""
	_date -= datetime.timedelta(days=1)
	_date += datetime.timedelta(hours=14)
	one_data = weather_data_B[_date]
	if one_data == None:
			return
	temperature = one_data[index_B["気温"]]
	return temperature


def get_temperature06_pointB(_date, weather_data_A, weather_data_B):
	""" 前日の06時の気温　地点B
	最低気温代わり
	"""
	_date -= datetime.timedelta(days=1)
	_date += datetime.timedelta(hours=6)
	one_data = weather_data_B[_date]
	if one_data == None:
			return
	temperature = one_data[index_B["気温"]]
	return temperature
	pass


def get_average_temperature_3days_pointB(_date, weather_data_A, weather_data_B):
	""" 3日間の平均気温　地点B
	"""
	__date = _date - datetime.timedelta(days=3)
	temperature = []
	while __date < _date:
		one_data = weather_data_B[__date]
		if one_data == None:
			return
		temperature.append(one_data[index_B["気温"]])
		__date += datetime.timedelta(hours=1)
	#print(temperature)
	return sum(temperature) / float(len(temperature))


def get_rain_pointB(_date, weather_data_A, weather_data_B):
	""" 3日間の降水量　地点B
	"""
	__date = _date - datetime.timedelta(days=3)
	rain = []
	while __date < _date:
		one_data = weather_data_B[__date]
		if one_data == None:
			return
		rain.append(one_data[index_B["降水量"]])
		__date += datetime.timedelta(hours=1)
	#print(rain)
	return sum(rain)


def get_sunshine_pointA(_date, weather_data_A, weather_data_B):
	""" 前日の日照時間の累積　地点A
	"""
	__date = _date - datetime.timedelta(days=1)
	sunshine = []
	while __date < _date:
		one_data = weather_data_B[__date]
		if one_data == None:
			return
		#print(one_data)
		if len(one_data) > index_B["日照時間"]: # 欠測対策
			sunshine.append(one_data[index_B["日照時間"]])
		else:
			sunshine.append(0.0)
		__date += datetime.timedelta(hours=1)
	#print(sunshine)
	return sum(sunshine)


def get_temperature23_pointA(_date, weather_data_A, weather_data_B):
	""" 前日の23時における気温　地点A
	"""
	_date -= datetime.timedelta(days=1)
	_date += datetime.timedelta(hours=23)
	one_data = weather_data_A[_date]
	if one_data == None:
			return
	temperature = one_data[index_A["気温"]]
	return temperature


def get_temperature23_pointA(_date, weather_data_A, weather_data_B):
	""" 前日の23時における気温　地点B
	"""
	_date -= datetime.timedelta(days=1)
	_date += datetime.timedelta(hours=23)
	one_data = weather_data_B[_date]
	if one_data == None:
			return
	temperature = one_data[index_B["気温"]]
	return temperature
	pass


def get_temperature_diff23_pointAB(_date, weather_data_A, weather_data_B):
	""" 前日の23時における気温差　地点A-地点B
	"""
	_date -= datetime.timedelta(days=1)
	_date += datetime.timedelta(hours=23)
	one_data = weather_data_A[_date]
	if one_data == None:
			return
	temperature_A = one_data[index_A["気温"]]
	one_data = weather_data_B[_date]
	if one_data == None:
			return
	temperature_B = one_data[index_B["気温"]]
	return temperature_A - temperature_B

def get_temperature_diff18to23_pointA(_date, weather_data_A, weather_data_B):
	""" 前日の18時-23時における気温差　地点A
	"""
	_date -= datetime.timedelta(days=1)
	time1 = _date + datetime.timedelta(hours=18)
	time2 = _date + datetime.timedelta(hours=23)
	one_data = weather_data_A[time1]
	if one_data == None:
			return
	temperature_1 = one_data[index_A["気温"]]
	one_data = weather_data_A[time2]
	if one_data == None:
			return
	temperature_2 = one_data[index_A["気温"]]
	return temperature_1 - temperature_2

def get_temperature_diff18to23_pointB(_date, weather_data_A, weather_data_B):
	""" 前日の18時-23時における気温差　地点B
	"""
	_date -= datetime.timedelta(days=1)
	time1 = _date + datetime.timedelta(hours=18)
	time2 = _date + datetime.timedelta(hours=23)
	one_data = weather_data_B[time1]
	if one_data == None:
			return
	temperature_1 = one_data[index_B["気温"]]
	one_data = weather_data_B[time2]
	if one_data == None:
			return
	temperature_2 = one_data[index_B["気温"]]
	return temperature_1 - temperature_2


def get_temperature_diff06to14_pointA(_date, weather_data_A, weather_data_B):
	""" 前日の06時-14時における気温差　地点A
	"""
	_date -= datetime.timedelta(days=1)
	time1 = _date + datetime.timedelta(hours=6)
	time2 = _date + datetime.timedelta(hours=14)
	one_data = weather_data_A[time1]
	if one_data == None:
			return
	temperature_1 = one_data[index_A["気温"]]
	one_data = weather_data_A[time2]
	if one_data == None:
			return
	temperature_2 = one_data[index_A["気温"]]
	if temperature_1 != None and temperature_2 != None:
		return temperature_1 - temperature_2
	else:
		return None


def get_temperature_diff06to14_pointB(_date, weather_data_A, weather_data_B):
	""" 前日の06時-14時における気温差　地点B
	"""
	_date -= datetime.timedelta(days=1)
	time1 = _date + datetime.timedelta(hours=6)
	time2 = _date + datetime.timedelta(hours=14)
	one_data = weather_data_B[time1]
	if one_data == None:
			return
	temperature_1 = one_data[index_B["気温"]]
	one_data = weather_data_B[time2]
	if one_data == None:
			return
	temperature_2 = one_data[index_B["気温"]]
	return temperature_1 - temperature_2


def get_wind23_pointB(_date, weather_data_A, weather_data_B):
	""" 前日の23時における風速　地点B
	"""
	_date -= datetime.timedelta(days=1)
	_date += datetime.timedelta(hours=23)
	one_data = weather_data_B[_date]
	if one_data == None:
			return
	wind = one_data[index_B["風速"]]
	return wind

def get_wind_direction_23_pointA(_date, weather_data_A, weather_data_B):
	""" 前日の23時における風向　地点A
	"""
	_date -= datetime.timedelta(days=1)
	_date += datetime.timedelta(hours=23)
	one_data = weather_data_A[_date]
	#print(weather_data_A)
	if one_data == None:
			return
	direction = one_data[index_A["風向"]]
	#print(one_data)
	exit()
	#print(direction)
	if direction != None:
		label = ["北", "北北東", "北東", "東北東", "東", "東南東", "南東", "南南東", "南", "南南西", "南西", "西南西", "西", "西北西", "北西", "北北西", "静穏"]
		return label.index(direction)#int(label.index(direction) / 4)
	else:
		return None

def get_wind_night_pointA(_date, weather_data_A, weather_data_B):
	""" 前日の21-23時における風速　地点A
	"""
	_date -= datetime.timedelta(days=1)
	time = _date + datetime.timedelta(hours=21)
	time_end = _date + datetime.timedelta(hours=23)
	wind = []
	while time <= time_end:
		one_data = weather_data_A[time]
		if one_data == None:
			return
		wind.append(one_data[index_A["風速"]])
		time += datetime.timedelta(hours=1)
	#print(wind)
	if None in wind:
		return None
	else:
		return sum(wind) / float(len(wind))


def get_dew_temperature23_pointA(_date, weather_data_A, weather_data_B):
	""" 前日の23時における露点温度　地点A
	"""
	_date -= datetime.timedelta(days=1)
	_date += datetime.timedelta(hours=23)
	one_data = weather_data_A[_date]
	if one_data == None:
			return
	temperature = one_data[index_A["露点温度"]]
	return temperature
	pass


def get_vapor_pressure23_pointA(_date, weather_data_A, weather_data_B):
	""" 前日の23時における蒸気圧　地点A
	"""
	_date -= datetime.timedelta(days=1)
	_date += datetime.timedelta(hours=23)
	one_data = weather_data_A[_date]
	if one_data == None:
			return
	vapor_pressure = one_data[index_A["蒸気圧"]]
	return vapor_pressure
	pass


def get_diff_air_pressure23_pointA(_date, weather_data_A, weather_data_B):
	""" 前日の23時と前々日の23時における気圧差　地点A
	"""
	_date -= datetime.timedelta(days=2)
	_date += datetime.timedelta(hours=23)
	one_data = weather_data_A[_date]
	if one_data == None:
		return
	pressure1 = one_data[index_A["現地気圧"]]
	_date += datetime.timedelta(hours=24) # 24時間後=前日の23時
	one_data = weather_data_A[_date]
	if one_data == None:
		return
	pressure2 = one_data[index_A["現地気圧"]]
	return pressure1 - pressure2


def get_bias_air_pressure23_pointA(_date, weather_data_A, weather_data_B):
	""" 前日の23時における気圧の平均からのズレ　地点A
	"""
	time = _date - datetime.timedelta(days=30)
	time += datetime.timedelta(hours=23)
	p = []
	while time < _date:
		if not time in weather_data_A:
			time += datetime.timedelta(days=1)
			continue
		one_data = weather_data_A[time]
		if one_data == None:
			time += datetime.timedelta(days=1)
			continue
		p.append(one_data[index_A["現地気圧"]])
		time += datetime.timedelta(days=1)
	average_p = sum(p) / float(len(p))
	return p[-1] - average_p



def get_humidity23_pointA(_date, weather_data_A, weather_data_B):
	""" 前日の23時における湿度　地点A
	"""
	_date -= datetime.timedelta(days=1)
	_date += datetime.timedelta(hours=23)
	one_data = weather_data_A[_date]
	if one_data == None:
			return
	humidity = one_data[index_A["気温"]]
	return humidity
	pass


def get_sight_range23_pointA(_date, weather_data_A, weather_data_B):
	""" 前日の23時における視程　地点A
	"""
	_date -= datetime.timedelta(days=1)
	_date += datetime.timedelta(hours=23)
	one_data = weather_data_A[_date]
	#print(one_data)
	if one_data == None:
			return
	sight_range = one_data[index_A["視程"]]
	return sight_range
	pass




def get_weather_dict(lines, th):
	""" 気象データの辞書を返す
	"""
	weather_dict = {}
	for line in lines:
		line = line.rstrip()
		if "時" in line:
			continue
		field = line.split(",")
		t = field[0]
		t = timeKM.getTime(t)
		field = field[1:]
		new_field = []
		for mem in field:
			fuga = mem.replace(".", "")
			fuga = fuga.replace(" )", "") # 観測上のおかしなデータにくっつく記号
			if len(fuga) > 0:
				if "-" == fuga[0]:
					fuga = fuga[1:]
			if fuga.isdigit() == True:
				mem = mem.replace(" )", "")
				new_field.append(float(mem))
			else:
				if mem == "":
					new_field.append(0.0)
				elif mem == "×":         # 恐らく、非観測項目にくっつく記号
					new_field.append(None)
				else:
					new_field.append(mem)
		if len(new_field) >= th:
			weather_dict[t] = new_field
		else:
			weather_dict[t] = None
	return weather_dict


def read_weather_data(fpath, th):
	"""
	気象データを読み込む
	"""
	weather_dict = {}
	with open(fpath, "r", encoding="utf-8-sig") as fr:
		lines = fr.readlines()
		weather_dict = get_weather_dict(lines, th)
	return weather_dict


def create_feature(_date, weather_data_A, weather_data_B):
	""" 特徴ベクトルを作る
	"""
	_feature = [
		get_season(_date, weather_data_A, weather_data_B), \
		get_temperature14_pointB(_date, weather_data_A, weather_data_B), \
		get_temperature06_pointB(_date, weather_data_A, weather_data_B), \
		get_average_temperature_3days_pointB(_date, weather_data_A, weather_data_B), \
		get_rain_pointB(_date, weather_data_A, weather_data_B), \
		get_sunshine_pointA(_date, weather_data_A, weather_data_B), \
		get_temperature23_pointA(_date, weather_data_A, weather_data_B), \
		get_temperature_diff23_pointAB(_date, weather_data_A, weather_data_B), \
		get_temperature_diff18to23_pointA(_date, weather_data_A, weather_data_B), \
		get_temperature_diff18to23_pointB(_date, weather_data_A, weather_data_B), \
		get_temperature_diff06to14_pointA(_date, weather_data_A, weather_data_B), \
		get_temperature_diff06to14_pointB(_date, weather_data_A, weather_data_B), \
		get_wind23_pointB(_date, weather_data_A, weather_data_B), \
		get_wind_direction_23_pointA(_date, weather_data_A, weather_data_B), \
		get_wind_night_pointA(_date, weather_data_A, weather_data_B), \
		get_dew_temperature23_pointA(_date, weather_data_A, weather_data_B), \
		get_vapor_pressure23_pointA(_date, weather_data_A, weather_data_B), \
		get_diff_air_pressure23_pointA(_date, weather_data_A, weather_data_B), \
		get_bias_air_pressure23_pointA(_date, weather_data_A, weather_data_B), \
		get_humidity23_pointA(_date, weather_data_A, weather_data_B) \
		#get_sight_range23_pointA(_date, weather_data_A, weather_data_B) \ # 視程は噴火で観測されなくなっている
		]
	return _feature

