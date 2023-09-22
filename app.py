from flask import Flask, render_template, request, jsonify
from flask_cors import CORS,cross_origin
from ineuronscrappermod import ineuronScrapper
from MongoDBOp import DBop
from loggerMainClass import scrapLogger


app = Flask(__name__)
logger = scrapLogger.ineuron_scrap_logger()

"""c = ineuronScrapper()
c.getCourses()
all_documents = c.getCoursedetails()
dbObj = DBop()
dbObj.createDB("IneuronCoursesData")
dbObj.createCollection("IneuronCourse_collection")
dbObj.insertDocument(all_documents)

counter = 0
for record in dbObj.getRecords("IneuronCourse_collection"):
    print(record)
    counter += 1
    if counter == 5:
        break"""

@app.route("/", methods = ["GET"])
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route("/scrap", methods = ["GET", "POST"])
@cross_origin()
def scrap():
    if request.method == "POST":
        try:
            c = ineuronScrapper()
            c.getCourses()
            all_documents = c.getCoursedetails()
            #return(all_documents)


            courses_list = []

            for course in all_documents :
                courses_list.append(all_documents[course])

            dbObj = DBop()
            dbObj.createDB("IneuronCoursesData")
            dbObj.createCollection("IneuronCourse_collection")
            dbObj.insertDocument(all_documents)
            return render_template("results.html", courses = courses_list)

        except Exception as e:
            logger.error("ERROR!! in scrap function ", str(e))

    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8001, debug=True)