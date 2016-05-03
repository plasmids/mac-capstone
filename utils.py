####### Change these based on this year's form output
studentLineFormat = "timestamp,username,name,majors,firstAdvisor,secondAdvisor,availablity,firstInterest,secondInterest,backToBackPartner,backToBackFirst,separateDays".split(',')
facultyLineFormat = "timestamp,username,name,capstoneFeedback,practiceTalksTue,practiceTalksThur,availablity,firstInterest,secondInterest,thirdInterest".split(',')
allTimes = "Wed 8:30 - 9:00 am;Wed 9:00 - 9:30 am;Wed 9:40 - 10:10 am;Wed 10:10 - 10:40 am;Wed 10:50 - 11:20 am;Wed 11:20 - 11:50 am;Wed 1:10 - 1:40 pm;Wed 1:40 - 2:10 pm;Wed 2:20 - 2:50 pm;Wed 2:50 - 3:20 pm;Wed 3:30 - 4:00 pm;Wed 4:00 - 4:30 pm;Wed 4:30 - 5:00 pm;Thu 8:30 - 9:00 am;Thu 9:00 - 9:30 am;Thu 9:40 - 10:10 am;Thu 10:10 - 10:40 am;Thu 10:40 - 11:10 am;Thu 1:20 - 1:50 pm;Thu 1:50 - 2:20 pm;Thu 2:20 - 2:50 pm".split(';')
days = ["Wed", "Thu"]
#######

def parseResponse(response, format):
    parsedFields = {}
    for i, field in enumerate(format):
        parsedFields[field] = response[i]
    return parsedFields
