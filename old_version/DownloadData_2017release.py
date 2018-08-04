import pycurl
import io
import re

url = "https://gaokao.chsi.com.cn/zzbm/mdgs/detail.action?oid=476737030&lx=1&start="
last_page_start = 2880

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
	res = re.findall(pat,text);
	l = len(res)
	j=0
	while j<l :
		f.write('<tr><td>'+"华中科技大学"+'</td>'+re.sub('\s*',"",res[j]))
		f.write("\n")
		j = j+1
	
	b.close()
	print(" Success")
	i = i+30;
	
f.write("</table>\n")