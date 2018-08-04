import pycurl
import io
import re
import time
import sys

last_page_start = 10000 #MAX item
sleep_time = 0;
#url = "https://gaokao.chsi.com.cn/zzbm/mdgs/detail.action?oid=476737030&lx=2&start="

f = open("data.xls","w+",encoding = 'utf-8')


def get_detail(url):
	
	#MATCH PATTEN
	#pat = '<tr>\s*<td>.*</td>\s*<td>.*</td>\s*<td>.*</td>\s*<td>.*</td>\s*</tr>'
	pat = '<td>.*</td>\s*<td>.*</td>\s*<td>.*</td>\s*<td>.*</td>\s*</tr>'
	school_name = "NULL"
	
	i=0;
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
		try:
			print("School Name:",tmp[0])
			school_name = tmp[0]
		except:
			print("Unexpected error:", sys.exc_info()[0])
			print("IN:",url+url2)
			print("Try again!")
			time.sleep(5)
			continue
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
		time.sleep(sleep_time);

def get_url(url):
	
	#MATCH PATTEN
	pat = '(?<=<a\shref="/zzbm/mdgs/).*(?=&amp;lx=2">)'
	
	print("Getting urls:")
	b = io.BytesIO()
	curl = pycurl.Curl()
	curl.setopt(curl.URL,url)
	curl.setopt(curl.USERAGENT, "Mozilla/4.0")
	curl.setopt(curl.SSL_VERIFYPEER,0)
	curl.setopt(curl.WRITEFUNCTION,b.write)
	curl.perform()
	
	#MATCH
	text = b.getvalue().decode('utf-8')
	res = re.findall(pat,text);
	return res
	
def main():
	res = get_url("https://gaokao.chsi.com.cn/zzbm/mdgs/orgs.action?lx=2")
	print("Getting ",len(res),"URLs")
	f.write("<table>\n")
	for x in res:
		if(re.match("subOrgs",x,flags=0) != None):
			#print(re.match("subOrgs",x,flags=0))
			print("Find Folder:::")
			tmp = get_url("https://gaokao.chsi.com.cn/zzbm/mdgs/"+str(x)+"&lx=2")
			print("Getting ",len(tmp),"URLs")
			for y in tmp:
				print("Collecting ",y,"==========")
				get_detail("https://gaokao.chsi.com.cn/zzbm/mdgs/"+str(y)+"&lx=2&start=")
		else:
			print("Collecting ",x,"==========")
			get_detail("https://gaokao.chsi.com.cn/zzbm/mdgs/"+str(x)+"&lx=2&start=")
	f.write("</table>")
	print("ALL DONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
				

main()


'''
res = get_url("https://gaokao.chsi.com.cn/zzbm/mdgs/subOrgs.action?oid=476734760&lx=2")
print("RES:",len(res))
for x in res:
	print(x)
#f.write("<table>\n")
#get_detail("https://gaokao.chsi.com.cn/zzbm/mdgs/"+str(res[3])+"&lx=2&start=")
#f.write("</table>")
'''
