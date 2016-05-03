#!/bin/python3
# Evan Weiler 2016

import csv
import random

from utils import *

studentSurveyFile = open('student-survey.csv')
studentSurveyReader = csv.reader(studentSurveyFile, delimiter = ',', quotechar = '"')

facultySurveyFile = open('faculty-survey.csv')
facultySurveyReader = csv.reader(facultySurveyFile, delimiter = ',', quotechar = '"')

schedulerFile = open('scheduler.csv', 'w')
schedulerWriter = csv.writer(schedulerFile, delimiter = ',', quoting = csv.QUOTE_NONE, escapechar = '\\')

def buildStudentResponses():
    students = []
    studentHeaders = studentSurveyReader.__next__()
    for studentResponse in studentSurveyReader:
        students.append(parseResponse(studentResponse, studentLineFormat))
    return students

def buildFacultyResponses():
    facultyAvailabilty = {}
    facultyHeader = facultySurveyReader.__next__()
    for facultyResponse in facultySurveyReader:
        faculty = parseResponse(facultyResponse, facultyLineFormat)
        interests = []
        if faculty['firstInterest']:
            interests.append(faculty['firstInterest'])
        if faculty['secondInterest']:
            pass #interests.append(faculty['secondInterest'])
        if faculty['secondInterest']:
            pass #interests.append(faculty['secondInterest'])
        info = {
            'availablity' : faculty['availablity'].split(';'),
            'interests' : interests
        }
        facultyAvailabilty[faculty['name']] = info
    return facultyAvailabilty

def findPresentationsOfStudent(name, presentations):
    presentationIDs = []
    for idNum, presentation in enumerate(presentations):
        #Name is first element in presentation list, students may be a double major, so they can have multiple presentations
        if name in presentation[0]:
            presentationIDs.append(idNum)
    return presentationIDs

def getAdivisors(student):
        advisors = [student['firstAdvisor']]
        if student['secondAdvisor']:
            advisors.append(student['secondAdvisor'])
        return advisors

def getAdvisees(facultyName, students):
    advisees = []
    for student in students:
        if facultyName in getAdivisors(student):
            advisees.append(student['name'])
    return advisees

def findStudentInterests(student):
    interests = []
    if student['firstInterest']:
        interests.append(student['firstInterest'])
    if student['secondInterest']:
        interests.append(student['secondInterest'])
    return interests

def findFacultyInterestIDs(facultyMember, presentations):
    interests = facultyMember['interests']
    interestPresentationIDs = []
    for interest in interests:
        interestPresentationIDs.extend(findPresentationsOfStudent(interest, presentations))
    return interestPresentationIDs

def conflictForFaculty(students, faculty, presentations):
    for advisor in faculty:
        advisees = getAdvisees(advisor, students)
        noConflictPresentations = []
        for advisee in advisees:
            noConflictPresentations.extend(findPresentationsOfStudent(advisee, presentations))
        # conflict based on faculty interests
        facultyInterests = findFacultyInterestIDs(faculty[advisor], presentations)
        noConflictPresentations.extend(facultyInterests)
        if len(noConflictPresentations) > 1:
            noConflictPresentations.sort()
            firstPresentation = presentations[noConflictPresentations.pop(0)]
            for presentationID in noConflictPresentations:
                if presentationID not in firstPresentation:
                    firstPresentation.append(presentationID)

def conflictStudentInterests(students, presentations):
    for student in students:
        name = student['name']
        studentPresentationIDs = findPresentationsOfStudent(name, presentations)
        interests = findStudentInterests(student)
        interestPresentationIDs = []
        for interest in interests:
            interestPresentationIDs.extend(findPresentationsOfStudent(interest, presentations))
        for studentPresentationID in studentPresentationIDs:
            presentation = presentations[studentPresentationID]
            for interestPresentationID in interestPresentationIDs:
                if interestPresentationID not in presentation:
                    presentation.append(interestPresentationID)

def normalizeNoConflictColumns(presentations):
    longestRow = 0
    for presentation in presentations:
        lenPresentation = len(presentation)
        if lenPresentation > longestRow:
            longestRow = lenPresentation
    for presentation in presentations:
        additionalColumns = longestRow - len(presentation)
        presentation.extend([''] * additionalColumns)

def write(presentations):
    nonNoConflictHeaders = ['ID', 'Name'] + allTimes
    numNoConflictColumns = len(presentations[0]) - len(nonNoConflictHeaders) + 1
    schedulerWriter.writerow(nonNoConflictHeaders + ['no conflict'] * numNoConflictColumns)
    for presentationID, presentation in enumerate(presentations):
        presentation[0] = presentation[0].replace(",", "")
        schedulerWriter.writerow([presentationID] + presentation)

def getAvailabilityOfMoreAvailableDay(availablity):
    mostAvailableDay = ""
    mostAvailableDayOccurences = 0
    for day in days:
        occurences = 0
        for time in availablity:
            if day in time:
                occurences += 1
        if occurences > mostAvailableDayOccurences:
            mostAvailableDay = day
            mostAvailableDayOccurences = occurences
    return [time for time in availablity if mostAvailableDay in time]

def separateAvailability(availablity):
    # The second list is plus one to ensure that there is a gap between the two presentations
    return availablity[:(len(availablity) // 2)], availablity[(len(availablity) // 2 + 1):]

def generateCSV():
    faculty = buildFacultyResponses()
    students = buildStudentResponses()
    presentations = []

    for student in students:
        scheduleDays = days[:]

        # MAKES SCRIPT NON DETERMISTIC, but keeps math and cs talks spread over both days
        random.shuffle(scheduleDays)
        #

        majors = student['majors'].split(';')
        doubleMajorWantsSeparateDays = student['separateDays'] == '1'
        availablity = student['availablity'].split(';')
        for advisor in getAdivisors(student):
            # get the intersection of student list and advisor
            availablity = [time for time in availablity if time in faculty[advisor]['availablity']]
        for i, major in enumerate(majors):
            presentation = []
            presentation.append(student['name'] + ' (' + major + ')')
            # make sure student and advisors are available (Shilad made no distinction for which advisor is for which major)
            if len(majors) > 1:
                if doubleMajorWantsSeparateDays:
                    day = scheduleDays.pop()
                    thisPresentionAvailablity = [time for time in availablity if day in time]
                else:
                    # If a double major wants to present both on one day, use their most available day,
                    # and separate presentations into the first and second halves of the day with a gap in between.
                    # Blame Ari Weiland for this :)
                    mostAvailableDayAvailability = getAvailabilityOfMoreAvailableDay(availablity)
                    firstHalf, secondHalf = separateAvailability(mostAvailableDayAvailability)
                    if i == 0:
                        thisPresentionAvailablity = firstHalf
                    else:
                        thisPresentionAvailablity = secondHalf
            else:
                thisPresentionAvailablity = availablity
            for time in allTimes:
                if time in thisPresentionAvailablity:
                    presentation.append(1)
                else:
                    presentation.append(0)
            presentations.append(presentation)

    conflictForFaculty(students, faculty, presentations)
    conflictStudentInterests(students, presentations)
    #conflictFacultyInterests(faculty, presentations)
    normalizeNoConflictColumns(presentations)
    write(presentations)
    print(presentations)

generateCSV()

studentSurveyFile.close()
facultySurveyFile.close()
schedulerFile.close()
