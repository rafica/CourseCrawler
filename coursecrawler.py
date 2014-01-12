from BeautifulSoup import BeautifulSoup
import urllib2
import re
import csv
link = "http://www.cs.columbia.edu/education/courses/list?yearterm=20133"
page = urllib2.urlopen(link)
soup = BeautifulSoup(page)

def removeTag(soup, tagname):
    for tag in soup.findAll(tagname):
        contents = tag.contents
        parent = tag.parent
        tag.extract()

cid = ""
title = ""
instructor = ""
day = ""
time= ""
location = ""
table = soup.find("table", {"class" : "schedule"})

f = open('course.csv' , 'w')

for row in table.findAll("tr"):
    cells = row.findAll("td")
    if len(cells) == 6:
        cid = cells[0].find(text=True)
        #print "cid" + cid
        title = cells[1].find(text=True)
        #print "title" + title
        instructor = cells[2].find(text=True)
        #print "instructor" + str(instructor)
        day = cells[3].find(text=True)
        #print "day" + day
        time = cells[4].find(text=True)
        #print "time" + time
        location = cells[5].find(text=True)
        #print "location" + location

    write_to_file = cid+","+title+","+str(instructor)+","+day+","+time+","+location+"\n"
    f.write(write_to_file)

f.close()

table.prettify()

title = ["Call Number", "Points", "Instructor", "Type", "Course Description", "Department", "Enrollment", "Number", "Section","Open To"]
title1 = ["Call Number","current", "maximum", "DayTimeLocation", "Points", "Instructor", "Type", "Course Description", "Department", "Enrollment", "Number", "Section","Open To"]
dictionary_list = []
dictionary ={}
test_file = open('coursedetails.csv', 'wb')
csvwriter = csv.DictWriter(test_file, delimiter=',',fieldnames = title1)
#csvwriter = csv.writerow(dict((fn,fn) for fn in title))
for anchor in table.findAll('a', href=True):
    l = anchor['href']
    if l[0:10]=="http://www":
        try:
            page = urllib2.urlopen(l)
    
            soup = BeautifulSoup(page)
            dictionary["DayTimeLocation"] ="null"
            
            for contents in soup.findAll("tr"):
                cells1 = contents.findAll("td")
                
                if len(cells1) == 2:
                    head = re.sub('<[^<]+?>', '', str(cells1[0]))
                    
                    if head[0:3]=="Day":
                        #print "yes"
                        dictionary["DayTimeLocation"]= re.sub('<[^<]+?>', '',str(cells1[1]))
                        #print dictionary["DayTimeLocation"]
                    
                        
                    for field in title:
                        if head == field:
                            dictionary[field]=re.sub('<[^<]+?>', '',str(cells1[1]))
                            if head == "Enrollment":
                                dictionary["current"] = dictionary["Enrollment"].split(' ',1)[0]
                                matchObj = re.match(r'.+\((\d+)\smax\).+',dictionary["Enrollment"])
                                if matchObj:
                                    dictionary["maximum"] = matchObj.group(1)
                                else:
                                    dictionary["maximum"] = 0
            dictionary_list.append(dictionary)
            dictionary ={}
            dictionary["DayTimeLocation"] = "null"
        
     
        except urllib2.HTTPError, err:
            if err.code == 404:
                print "Page not found"
            elif err.code == 403:
                print "access denied"
            else:
                print "something happened, error code " + err.code
        except urllib2.URLError,err:
            print "some other error happened:",err.reason

csvwriter.writerows(dictionary_list)
test_file.close()
