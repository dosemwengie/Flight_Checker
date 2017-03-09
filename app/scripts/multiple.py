import json,requests,heapq,operator
import random
from datetime import datetime

def do_work_multiple(target_price,price_max,flying_from,flying_to,date_from,date_to):
	
	proxy_list=[]
	email_list=[]
	final_list=[]
	airlines={}
	#Get Proxy IPs
	proxy_file=open('../proxy_list/HTTP_proxy','r')
	for proxies in proxy_file:
		proxies=proxies.split()
		ip=proxies[-2]
		port=proxies[-1]
		proxy_list.append(':'.join([ip,port]))
	pr_count=random.randint(0,len(proxy_list))
	proxy_file.close()
	python_obj=None
	for origin in flying_from:
		if not origin:
			continue
		proxy={'http':'http://%s'%(proxy_list[-1])}	
		price_point=float(price_max)*100
		target_point=float(target_price)*100
		while True:
			if not proxy_list:
				return None
			proxy={'http':'http://%s'%(proxy_list[-1])}
			
			print("Trying ",proxy_list[-1])

			try:
				res=requests.get("http://skiplagged.com/api/search.php?from=%s&to=%s&depart=%s&&return=%s&sort=cost"%(origin,flying_to,date_from,date_to),proxies=proxy)
				print("http://skiplagged.com/api/search.php?from=%s&to=%s&depart=%s&&return=%s&sort=cost"%(origin,flying_to,date_from,date_to))
				python_obj=json.loads(res.text)
                        	if res.status_code!=200:
                        	        flying_from.append(origin)
                        	        print(res.status_code,proxy)
                        	        proxy_list.pop()
                        	        continue
				else:
					print python_obj
					break
                	except Exception as e:
				print("%s not working===%s"%(proxy_list[-1],str(e)))
                        	flying_from.append(origin)
                        	proxy_list.pop()
                        	continue
		if not python_obj['airlines']:
			continue
		print("%s-->%s=%s"%(origin,flying_to,python_obj['depart'][0][0]))
                FROM=python_obj['info']['from'][1]
                TO=python_obj['info']['to'][1]
                for keys in python_obj['airlines'].keys():
                        if airlines.has_key(keys):
                                continue
                        else:
                                airlines[keys]=python_obj['airlines'][keys]
                if python_obj["return"]:
                        price=max(int(python_obj["depart"][0][0][0]),int(python_obj["return"][0][0][0]))
                        if price>price_point:
                                print("No flights found, cheapest flight=%.2f...exiting"%(float(price)/100))
                                continue
                        final_results={'MIN_TO':[],'MIN_FROM':[]}
                        for hashes in python_obj["depart"]:
                                print(hashes[0])
                                if len(hashes[0]) < 2:
                                        continue
                                if int(hashes[0][1])<=price:
                                        final_results['MIN_FROM'].append([python_obj["flights"][hashes[3]],hashes[0][1]])
                        for hashes in python_obj["return"]:
                                if int(hashes[0][0])<=price:
                                        final_results['MIN_TO'].append([python_obj["flights"][hashes[3]],hashes[0][0]])
                        depart_dict=[]
                        return_dict=[]
                        for keys in sorted(final_results['MIN_FROM'],key=operator.itemgetter(1)):
                                depart_dict.append([int(keys[1]),keys[0][0]])
                        for keys in sorted(final_results['MIN_TO'],key=operator.itemgetter(1)):
                                return_dict.append([int(keys[1]),keys[0][0]])
                        for departs in depart_dict:
                                for returns in return_dict:
                                        print(departs[0],returns[0])
                                        if (departs[0]+returns[0])<=price_point:
                                                flight_sum=(departs[0]+returns[0])
                                                final_list.append((flight_sum,departs[1],returns[1]))
                                        if (departs[0]+returns[0])<=target_point:
                                                flight_sum=(departs[0]+returns[0])
                                                email_list.append((flight_sum,departs[1],returns[1]))
                else:
			price=int(python_obj["depart"][0][0][0])
                        if price>price_point:
                                print("No flights found,cheapest flight %.2f...exiting"%(float(price)/100))
                                continue
                        final_results={'MIN_TO':[],'MIN_FROM':[]}
                        for hashes in python_obj["depart"]:
                                if len(hashes[0]) < 1:
                                        continue
                                if int(hashes[0][0])<=price_point:
                                         final_results['MIN_FROM'].append([python_obj["flights"][hashes[3]],hashes[0][0]])
                        depart_dict=[]
                        for keys in sorted(final_results['MIN_FROM'],key=operator.itemgetter(1)):
                                depart_dict.append([int(keys[1]),keys[0][0]])
                       
                        for departs in depart_dict:
                                if departs[0]<=price_point:
                                        final_list.append((departs[0],departs[1]))
                                      
                                if departs[0]<=target_point: 
                                        email_list.append((departs[0],departs[1]))
        if python_obj['return']:
                while final_list:
                        heapq.heapify(final_list)
                        num+=1
                        flight=heapq.heappop(final_list)
                        print("%d. TOTAL:$ %.2f"%(num,float(flight[0])/100))
                        print("\t\tDeparting")
			for values in flight[1]:
                                date1=values[2].find(':',-9)
                                date1=values[2][:date1]
                                date1=datetime.strptime(date1,"%Y-%m-%dT%H:%M").ctime()
                                date2=values[4].find(':',-9)
                                date2=values[4][:date2]
                                date2=datetime.strptime(date2,"%Y-%m-%dT%H:%M").ctime()
                                print("%s(%s) %s %s ---> %s %s"%(values[0],airlines[values[0][:2]],values[1],date1,values[3],date2))
                        print("\n")
                        print("\t\tReturning")
                        for values in flight[2]:
                                date1=values[2].find(':',-9)
                                date1=values[2][:date1]
                                date1=datetime.strptime(date1,"%Y-%m-%dT%H:%M").ctime()
                                date2=values[4].find(':',-9)
                                date2=values[4][:date2]
                                date2=datetime.strptime(date2,"%Y-%m-%dT%H:%M").ctime()
                                print("%s(%s) %s %s ---> %s %s"%(values[0],airlines[values[0][:2]],values[1],date1,values[3],date2))
                        print("\n")
                while email_list:
                        heapq.heapify(email_list)
                        inner+=1
                        flight=heapq.heappop(email_list)
                        for values in flight[1]:
                                date1=values[2].find(':',-9)
                                date1=values[2][:date1]
                                date1=datetime.strptime(date1,"%Y-%m-%dT%H:%M").ctime()
                                date2=values[4].find(':',-9)
                                date2=values[4][:date2]
                                date2=datetime.strptime(date2,"%Y-%m-%dT%H:%M").ctime()
                        for values in flight[2]:
                                date1=values[2].find(':',-9)
                                date1=values[2][:date1]
                                date1=datetime.strptime(date1,"%Y-%m-%dT%H:%M").ctime()
                                date2=values[4].find(':',-9)
                                date2=values[4][:date2]
                                date2=datetime.strptime(date2,"%Y-%m-%dT%H:%M").ctime()
        else:
                while final_list:
                        heapq.heapify(final_list)
                        num+=1
                        flight=heapq.heappop(final_list)
                        print("TOTAL:$%.2f"%(float(flight[0])/100))
                        print("\t\tDeparting")
                        for values in flight[1]:
                                date1=values[2].find(':',-9)
                                date1=values[2][:date1]
                                date1=datetime.strptime(date1,"%Y-%m-%dT%H:%M").ctime()
                                date2=values[4].find(':',-9)
                                date2=values[4][:date2]
                                date2=datetime.strptime(date2,"%Y-%m-%dT%H:%M").ctime()
                                print("%s(%s) %s %s ---> %s %s"%(values[0],airlines[values[0][:2]],values[1],date1,values[3],date2))
                        heapq.heapify(final_list)
                        print("\n")
                while email_list:
                        heapq.heapify(email_list)
                        inner+=1
                        flight=heapq.heappop(email_list)
                        for values in flight[1]:
                                date1=values[2].find(':',-9)
                                date1=values[2][:date1]
                                date1=datetime.strptime(date1,"%Y-%m-%dT%H:%M").ctime()
                                date2=values[4].find(':',-9)
				date2=values[4][:date2]
                                date2=datetime.strptime(date2,"%Y-%m-%dT%H:%M").ctime()
                                print("%s(%s) %s %s ---> %s %s"%(values[0],airlines[values[0][:2]],values[1],date1,values[3],date2))
                        heapq.heapify(final_list)
                        print("\n")
                while email_list:
                        heapq.heapify(email_list)
                        inner+=1
                        flight=heapq.heappop(email_list)
                        for values in flight[1]:
                                date1=values[2].find(':',-9)
                                date1=values[2][:date1]
                                date1=datetime.strptime(date1,"%Y-%m-%dT%H:%M").ctime()
                                date2=values[4].find(':',-9)
                                date2=values[4][:date2]
                                date2=datetime.strptime(date2,"%Y-%m-%dT%H:%M").ctime()
