import pymongo
from threading import Thread
from multiple import do_work_multiple
from datetime import datetime
	
client=pymongo.MongoClient()
db=client.get_database('flight_tracker')
criteria=db.get_collection('criteria')
users=db.get_collection('users')
records=criteria.find()

def main():
	for record in records:
		objectid=record['ObjectId']
		pref=record['preference']
		for choice in pref:
			#print choice
			target_price=choice['target_price']
			price_max=choice['price_max']
			flying_from=[choice['flying_from']]
			flying_to=choice['flying_to']
			date_from=choice['date_from'].strftime("%Y-%m-%d")
			date_to=choice['date_to'].strftime("%Y-%m-%d")
			active=choice['active']
			#t=Thread(target=launch,args=(target_price,price_max,flying_from,flying_to,date_from,date_to))
			#t.start()
			launch(target_price,price_max,flying_from,flying_to,date_from,date_to)
		
	client.close()

def launch(target_price,price_max,flying_from,flying_to,date_from,date_to):

		results=do_work_multiple(target_price,price_max,flying_from,flying_to,date_from,date_to)
		print results
		if results and active=='Y':
			cursor=users.find_one({"_id":objectid})
			email=cursor['email']
			#Send Notification
			criteria.update({"ObjectId":objectid,"preference.target_price":target_price,"preference.price_max":price_max,"preference.flying_from":flying_from,"preference.flying_to":flying_to,"preference.date_from":date_from,"preference.date_to":date_to,"preference.active":active}, { "$set": {"preference.$.active":"N"},"$push":{"result": { "$each" : results }}})
				


if __name__=="__main__":
	main()
