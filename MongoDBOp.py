import pymongo
from loggerMainClass import scrapLogger

class DBop:
    def __init__(self):
        self.logger = scrapLogger.ineuron_scrap_logger()

        while True:
            try:
                self.logger.info("Enter Username and password to Connect to MongoDB")
                self.username = input("PLease enter the database Username : ")
                self.password = input("Please enter your password : ")
                self.logger.info(f"User establishing a MongoDB connection is {self.username}")
                self.url = f"mongodb+srv://{self.username}:{self.password}@cluster0.2pnukrk.mongodb.net/?retryWrites=true&w=majority"
                self.client = pymongo.MongoClient(self.url)
                self.client.admin.command("ping")
                self.logger.info("Connection Established!!")
                break
            except Exception as e:
                self.logger.error("Unable to establish connection, please enter valid username and password " + str(e))

    def createDB(self, db_name):
        """
        Function to create a DB in mongoDB atlas if it does not already exist
        :param db_name: Name of the Database to be created or used

        """
        try:
            self.database = self.client[db_name]

            # Check if database already exists

            if db_name in self.client.list_database_names():
                self.logger.info(f"Database {db_name}already Exists, you can proceed")
        except Exception as e:
            self.logger.error("ERROR while creating the database " + str(e))

    def createCollection(self, collection_name):
        """
        Function to create a collection if it does not already exist
        :param collection_name: Name of the collection to be created or used

        """
        try:
            self.collection = self.database[collection_name]
            # check if the collection is exists
            if collection_name in self.database.list_collection_names():
                self.logger.info(f"Collection {Collection_name} Exists, please continue ")
        except Exception as e:
            self.logger.info("ERROR while creating the collection" + str(e))

    def insertDocument(self, documents):
        """
        Function to insert records into MongoDB collection
        :param documents: Dictionary object with all the records to be inserted
        """
        try:
            self.logger.info("Inserting all the documents into MongoDB")
            if type(documents) == dict:
                all_record = self.collection.find()
                duplicate_record = False

                for key, value in documents.items():
                    for record in all_record:
                        if value["course_title"] == record["course_title"]:
                            duplicate_record = True
                            break
                    if duplicate_record == False:
                        self.collection.insert_one(value)
            else:
                self.logger.info("Documents is not in Dict format, please Check!!")

        except Exception as e:
            self.logger.error("Error while inserting" + str(e))

    def getRecords(self, collection_name):
        """
        Function to fetch data from a collection provided
        :param collection_name: Name of the collection to fetch data from
        :return: Cursor object with all the records
        """
        try:
            collection = self.database[collection_name]
            self.logger(f"Fetching documents from {self.collection}")
            data = collection.find()
            self.logger.info("Returning the cursor object with all the data fetched")
            return data
        except Exception as e:
            self.logger.error("Error!! while fetching data " + str(e))