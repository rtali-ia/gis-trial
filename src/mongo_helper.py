from mongoengine import connect

def connect_to_mongo(db_name : str, host : str, port : int):
    try:
        connect(db_name, host=host, port=port)
        print('Connected to MongoDB')
            
    except Exception as e:
        print('Error connecting to MongoDB:', e)
        
        
if __name__ == '__main__':
    connect_to_mongo('GIS', 'localhost', 27017)