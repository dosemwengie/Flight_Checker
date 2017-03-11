from pymongo import MongoClient
from optparse import OptionParser

def main():
	#Accept host/port parsed command, else use default values
	parser=OptionParser()
	parser.add_option("--host",dest="host",default="localhost")
	parser.add_option("-p","--port",dest="port",default=27017)
	(options,args)=parser.parse_args()
	
	#Create db connection
	client=MongoClient(host=options.host,port=options.port)
	
	#Retrieve db,else it will be created
	db=client.get_database('flight_tracker')

	#create collections if they do not exist
	col_names=db.collection_names()
	if 'criteria' not in col_names:
		db.create_collection('criteria')
	if 'users' not in col_names:
		db.create_collection('users')



if __name__=="__main__":
	main()
