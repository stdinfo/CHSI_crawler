import pycurl
import io
import re

#url = "https://gaokao.chsi.com.cn/zzbm/mdgs/detail.action?oid=476737030&lx=1&start="
url = "https://gaokao.chsi.com.cn/zzbm/mdgs/detail.action;jsessionid=02BDDC1BA13409A669D5250BDB3E351B?oid=476755697&lx=1&start="
last_page_start = 10000

i = 0
f = open("data.xls","w+")
#pat = '<tr>\s*<td>.*</td>\s*<td>.*</td>\s*<td>.*</td>\s*<td>.*</td>\s*</tr>'
pat = '<td>.*</td>\s*<td>.*</td>\s*<td>.*</td>\s*<td>.*</td>\s*</tr>'
f.write("<table>\n")

while i <= last_page_start :
	print("open page:",i/30)
	b = io.BytesIO()
	print("set curl")
	curl = pycurl.Curl()
	url2 = str(i)
	curl.setopt(curl.URL,url+url2)
	curl.setopt(curl.USERAGENT, "Mozilla/4.0")
	curl.setopt(curl.SSL_VERIFYPEER,0)
	curl.setopt(curl.WRITEFUNCTION,b.write)
	curl.perform()
	
	'''
	match and write
	'''
	text = b.getvalue().decode('utf-8')
	check = re.findall("暂无数据",text);
	if(len(check) != 0):
		break
	tmp = re.findall('(?<=\s)\S*(?=\s*名单公示\s*</h3>)',text)
	print("School Name:",tmp[0])
	school_name = tmp[0]
	res = re.findall(pat,text);
	l = len(res)
	j=1
	while j<l :
		f.write('<tr><td>'+school_name+'</td>'+re.sub('\s*',"",res[j]))
		f.write("\n")
		j = j+1
	
	b.close()
	print(" Success")
	i = i+30;
	
f.write("</table>\n")