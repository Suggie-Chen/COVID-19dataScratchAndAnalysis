import csv
import time
import re
from selenium import webdriver

date=time.strftime("%Y-%m-%d")
print(date)

base_url = "https://www.zq-ai.com/#/fe/xgfybigdata"    # 访问的地址

# base_url='file:///C:/Users/92994/Desktop/2020-12-1.html'
#base_url='file:///C:/Users/92994/Desktop/新冠html/2020-12-1.html'
driver = webdriver.Edge("C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe")
driver.implicitly_wait(1)  # 隐式等待时间,隐形等待是设置了一个最长等待时间，如果在规定时间内网页加载完成，则执行下一步，否则一直等到时间截止，然后执行下一步
driver.get(base_url) # 加载指定地址页面

table=[]
for i in range(0,188):#奇怪，为什么必须从下标0开始才能得到完整数据啊
	# if(i==0):continue
	dic=dict()

	name=driver.find_elements_by_xpath('//*[@id="app"]/div/section[2]/section/main/div/div[6]/'
									'div[4]/div[2]/table/tbody/tr[{}]/td[1]/div/a/span'.format(i))
	if len(name)>0:#这里很奇怪，有时候得到空数据
		name = name[0].get_attribute("innerHTML")
		dic['name']=name
		# print(i,name)


	total=driver.find_elements_by_xpath('//*[@id="app"]/div/section[2]/section/main/div/div[6]/'
										 'div[3]/table/tbody/tr[{}]/td[3]/div/span'.format(i))
	if len(total)>0:
		dic['totalNum']=total[0].text
		# print(i,dic['total'])


	deadNum=driver.find_elements_by_xpath('//*[@id="app"]/div/section[2]/section/main/div/div[6]/'
										  'div[3]/table/tbody/tr[{}]/td[9]/div/span'.format(i))
	if len(deadNum)>0:
		dic['deadNum']=deadNum[0].text
		# print(i,dic['deadNum'])

	new=driver.find_elements_by_xpath('//*[@id="app"]/div/section[2]/section/main/div/div[6]/'
									  'div[3]/table/tbody/tr[{}]/td[2]/div/span'.format(i))
	if len(new)>0:
		dic['newNum']=new[0].text
		# print(i,dic['new'])


	deadRate=driver.find_elements_by_xpath('//*[@id="app"]/div/section[2]/section/main/div/div[6]'
										   '/div[3]/table/tbody/tr[{}]/td[10]/div/span'.format(i))
	if len(deadRate) > 0:
		dic['deadRate'] = deadRate[0].text

	totalPopulation=driver.find_elements_by_xpath('//*[@id="app"]/div/section[2]/section/main/div/div[6]'
												  '/div[3]/table/tbody/tr[{}]/td[12]/div/span'.format(i))
	if(len(totalPopulation)>0):
		dic['totalPopulation'] =totalPopulation[0].text
		temp=re.sub("\D", "", dic['totalPopulation'])
		if temp!='':
			popnum=int(temp)
			dic['infecRate'] = round(float(dic['totalNum']) / popnum/100,6)
	# infecRate=driver.find_elements_by_xpath('//*[@id="app"]/div/section[2]/section/main/div/div[6]'
	# 									'/div[3]/table/tbody/tr[{}]/td[11]/div/span'.format(i))


	if len(dic)>0:
		table.append(dic)

# print(table)

#全球
d=dict()
d['name'] = "全球"

d['totalPopulation']=758520
addnew = driver.find_elements_by_xpath('//*[@id="pane-world"]/div[2]/div/div[1]/div/div[1]/span')
addnew = addnew[0].text
addnew = addnew.replace("+",'')
# addnew = int(addnew)
d['newNum']=addnew

total_confirmed = driver.find_elements_by_xpath('//*[@id="pane-world"]/div[2]/div/div[1]/div/div[2]')
total_confirmed = total_confirmed[0].text
# total_confirmed = int(total_confirmed)
d['totalNum']=total_confirmed

death = driver.find_elements_by_xpath('//*[@id="pane-world"]/div[2]/div/div[3]/div/div[2]')
death = death[0].text
# death = int(death)
d['deadNum']=death

death_rate = driver.find_elements_by_xpath('//*[@id="pane-world"]/div[2]/div/div[6]/div/div[2]')
death_rate = death_rate[0].text
death_rate = death_rate.replace("%",'')
# death_rate = float(death_rate)
d['deadRate']=death_rate
if d['totalNum']!='':
	d['infecRate']=round(float(d['totalNum']) / d['totalPopulation']/100,6)
table.append(d)

# #点击切换标签页
# driver.find_element_by_id('tab-china').click()
# #中国
# dc=dict()
# dc['name'] = "中国"
# addnew = driver.find_elements_by_xpath('//*[@id="pane-china"]/div[2]/div/div[1]/div/div[1]/span')
# addnew = addnew[0].text
# addnew = addnew.replace("+",'')
# # addnew = int(addnew)
# dc['newNum']=addnew
#
# dc['totalPopulation']=140005
#
# total_confirmed = driver.find_elements_by_xpath('//*[@id="pane-china"]/div[2]/div/div[1]/div/div[2]')
# total_confirmed = total_confirmed[0].text
# # total_confirmed = int(total_confirmed)
# dc['totalNum']=total_confirmed
#
# death = driver.find_elements_by_xpath('//*[@id="pane-china"]/div[2]/div/div[3]/div/div[2]')
# death = death[0].text
# # death = int(death)
# dc['deadNum']=death
# if death!='':
# 	dc['deadRate']=float(death)/dc['totalPopulation']
# if dc['totalNum']!='':
# 	dc['infecRate'] = round(float(dc['totalNum']) / dc['totalPopulation']/100,6)
# table.append(dc)
# test.csv表示如果在当前目录下没有此文件的话，则创建一个csv文件
# a表示以“追加”的形式写入，如果是“w”的话，表示在写入之前会清空原文件中的数据
# newline是数据之间不加空行
# encoding='utf-8'表示编码格式为utf-8，如果不希望在excel中打开csv文件出现中文乱码的话，将其去掉不写也行。
header=['name', 'totalNum', 'newNum','deadNum','totalPopulation', 'deadRate','infecRate' ]#把列名给提取出来，用列表形式呈现
print(header)
with open(date+'.csv', 'w', newline='') as f:#, encoding='utf-8'
	writer = csv.DictWriter(f, fieldnames=header)  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
	writer.writeheader()  # 写入列名
	writer.writerows(table)  # 写入数据