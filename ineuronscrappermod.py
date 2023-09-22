import requests
from urllib.request import urlopen as uReq
from urllib.error import HTTPError
import urllib
from bs4 import BeautifulSoup as bs
import json
from loggerMainClass import scrapLogger


class ineuronScrapper :
    def __init__(self) :
        self.logger = scrapLogger.ineuron_scrap_logger()
        """
        Creates ineuronScrapper object. Sends a request to the ineuron url.
        """

        while True :
            try :
                self.ineuron_url = "https://ineuron.ai/courses?source=navbar"
                hdr = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
                Req = urllib.request.Request(self.ineuron_url, headers = hdr)
                self.uClient = uReq(Req)
                self.logger.info(f"URL entered for ineuron course scrapping : {self.ineuron_url}")
                self.ineuronPage = self.uClient.read()
                self.logger.info("Page Read")
                self.uClient.close()
                #print(self.ineuronPage)
            except HTTPError:
                self.logger.error("HTTPError: HTTP Error 403: Forbidden")
                break
            except Exception as e :
                self.logger.error("ERROR!! " + str(e))
            else :
                self.logger.info("constructor created successfully")
                break

    def getCourses(self):
        """
        Obtains all the course names listed on ineuron website.

        """
        try :
            self.ineuron_html = bs(self.ineuronPage, "html.parser")
            self.logger.info("Page parsed, html parser tree created")
            self.courselistbox = self.ineuron_html.find_all("script", {"id" : "__NEXT_DATA__"})
            self.courselistbox_dict = json.loads(self.courselistbox[0].text)
            self.courses = self.courselistbox_dict["props"]["pageProps"]["initialState"]["init"]["courses"].keys()
            self.logger.info("Obtained all course names")
            #print(self.courses)
            #print(type(self.courses))

        except Exception as e :
            self.logger.info("ERROR while getting all Courses f[__getCourses__]" + str(e))

    def getCoursedetails(self):
        """
        This function gathers course information for every course listed on ineuron website
        :return: Dictionary object with courses as the keu and their details in a dictionary as the value
        """
        try :
            self.coursedata = {}
            self.__getAllInstructors  = self.courselistbox_dict["props"]["pageProps"]["initialState"]["init"]["instructors"]
            self.logger.info("Getting all the course details")
            for course in self.courses :
                #print(course)
                if course not in self.coursedata :
                    self.coursedata[course] = {}

                course_urlslug = "https://ineuron.ai/course/" + course.replace(" ", "-") + "?source=course_listing_page"
                self.coursedata[course]["course_urlslug"] = course_urlslug

                courseRes = requests.get(course_urlslug)
                courseRes.encoding = "utf-8"
                course_html = bs(courseRes.text, "html.parser")
                courseinfo_dict = json.loads(course_html.find_all("script", {"id" : "__NEXT_DATA__"})[0].text)

                try :
                    course_title = courseinfo_dict["props"]["pageProps"]["data"]["title"]                  # course title
                    self.coursedata[course]["course_title"] = course_title
                except :
                    self.coursedata[course]["course_title"] = "NO Title"

                try :
                    jobGuarentee = courseinfo_dict["props"]["pageProps"]["data"]["isJobGuaranteeProgram"]  # job guarentee?
                    self.coursedata[course]["jobGuarentee"] = jobGuarentee
                except :
                    self.coursedata[course]["jobGuarentee"] = "NA"

                try :
                    inOneNeuron = courseinfo_dict["props"]["pageProps"]["data"]["courseInOneNeuron"]  # course in OneNeuron?
                    self.coursedata[course]["inOneNeuron"] = inOneNeuron
                except :
                    self.coursedata[course]["inOneNeuron"] = "NA"

                try :
                    batches = courseinfo_dict["props"]["pageProps"]["data"]["batches"]                 # batches
                    self.coursedata[course]["batches"] = batches
                except :
                    self.coursedata[course]["batches"] = "NA"

                try :
                    course_description = courseinfo_dict["props"]["pageProps"]["data"]["details"]["description"]   # course details
                    self.coursedata[course]["course_description"] = course_description
                except :
                    self.coursedata[course]["course_description"] = "NA"

                try :
                    classTimings = courseinfo_dict["props"]["pageProps"]["data"]["details"]["classTimings"]
                    self.coursedata[course]["classTimings"] = classTimings
                except :
                    self.coursedata[course]["classTimings"] = "NA"

                try :
                    pricing = courseinfo_dict["props"]["pageProps"]["data"]["details"]["pricing"]
                    self.coursedata[course]["pricing"] = pricing
                except :
                    self.coursedata[course]["pricing"] = "NA"

                # Get course instructors details
                instructor_details = {}
                for id in courseinfo_dict["props"]["pageProps"]["data"]["meta"]["instructors"] :
                    if id in self.__getAllInstructors.keys() :
                        name = self.__getAllInstructors[id]["name"]
                        instructor_details[name] = {}
                        try :
                            instructor_details[name]["social"] = self.__getAllInstructors[id]["social"]
                        except :
                            instructor_details[name]["social"] = "NA"

                        try :
                            instructor_details[name]["description"] = self.__getAllInstructors[id]["description"]
                        except :
                            instructor_details[name]["description"] = "NA"

                        try :
                            instructor_details[name]["email"] = self.__getAllInstructors[id]["email"]
                        except :
                            instructor_details[name]["email"] = "NA"

                self.coursedata[course]["instructors"] = instructor_details

                try :
                    duration = courseinfo_dict["props"]["pageProps"]["data"]["meta"]["duration"]          # course duration
                    self.coursedata[course]["duration"] = duration
                except :
                    self.coursedata[course]["duration"] = "NA"

                try :
                    certificateBenchmark = courseinfo_dict["props"]["pageProps"]["data"]["meta"]["certificateBenchmark"]  # certificate benchmark
                    self.coursedata[course]["certificateBenchmark"] = certificateBenchmark
                except :
                    self.coursedata[course]["certificateBenchmark"] = "NA"

                # getting all the curriculum titles and their items
                curriculum_details = {}
                for key in courseinfo_dict["props"]["pageProps"]["data"]["meta"]["curriculum"].keys():
                    try :
                        curriculum_title = courseinfo_dict["props"]["pageProps"]["data"]["meta"]["curriculum"][key]["title"]
                        if curriculum_title not in curriculum_details:
                            curriculum_details[curriculum_title] = []
                        for dict_ele in courseinfo_dict["props"]["pageProps"]["data"]["meta"]["curriculum"][key]["items"]:
                            curriculum_details[curriculum_title].append(dict_ele["title"])
                    except:
                        curriculum_title = "NA"
                #print(curriculum_details)
                self.coursedata[course]["curriculum"] = curriculum_details


                # getting all the project titles and their items
                project_details = {}
                for key in courseinfo_dict["props"]["pageProps"]["data"]["meta"]["projects"].keys():
                    try :
                        project_title = courseinfo_dict["props"]["pageProps"]["data"]["meta"]["projects"][key]["title"]
                        if project_title not in project_details:
                            project_details[project_title] = []
                        for dict_ele in courseinfo_dict["props"]["pageProps"]["data"]["meta"]["projects"][key]["items"]:
                            project_details[project_title].append(dict_ele["title"])
                    except :
                        project_title = "NA"
                # print(project_details)
                self.coursedata[course]["projects"] = project_details


                # getting learn, requirements and course features
                try :
                    self.coursedata[course]["overview"] = courseinfo_dict["props"]["pageProps"]["data"]["meta"]["overview"]
                except :
                    self.coursedata[course]["overview"] = "No Overview"

            self.logger.info("Parsed through all the courses, returning all course data for DB insertion")
            return self.coursedata


        except Exception as e:
            self.logger.error("ERROR!! while gathering course details " + str(e))
