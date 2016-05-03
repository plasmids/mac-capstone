#!/bin/python3
# Evan Weiler 2016

import csv

from utils import *

scheduledFile = open('output.csv')
scheduledReader = csv.reader(scheduledFile, delimiter = ',')

studentSurveyFile = open('student-survey.csv')
studentSurveyReader = csv.reader(studentSurveyFile, delimiter = ',', quotechar = '"')

sessionsFile = open('sessions.csv', 'w')
sessionsWriter = csv.writer(sessionsFile, delimiter = ',', quoting = csv.QUOTE_NONE, escapechar = '\\')

def mapStudentsToAdivisors():
    mapping = {}
    studentHeaders = studentSurveyReader.__next__()
    for studentResponse in studentSurveyReader:
        parsedResponse = parseResponse(studentResponse, studentLineFormat)
        advisors = ""
        if parsedResponse['firstAdvisor']:
            advisors += parsedResponse['firstAdvisor']
        if parsedResponse['secondAdvisor']:
            advisors += " / " + parsedResponse['secondAdvisor']
        mapping[parsedResponse['name'].replace(",", "")] = advisors
    return mapping

def addToGrid(grid, time, presentationName):
    for row in grid:
        if time in row[0]:
            row.append(presentationName)
            return

def addAdvisorName(mapping, presentationName):
    name = presentationName.split('(', 1)[0].rstrip()
    advisorName = mapping[name]
    return presentationName + " " + advisorName

def createSessionHeaders(sessionsGrid):
    headers = ["Time"]
    longestRow = 0
    for time in sessionsGrid:
        rowLen = len(time)
        if rowLen > longestRow:
            longestRow = rowLen
    for i in range(1, rowLen):
        headers.append("Room #" + str(i))
    return headers

def write(sessionsGrid):
    sessionsWriter.writerow(createSessionHeaders(sessionsGrid))
    for time in sessionsGrid:
        sessionsWriter.writerow(time)


def generateSessions():
    studentAdvisors = mapStudentsToAdivisors()
    times = scheduledReader.__next__()
    times.remove("Name")
    sessionsGrid = []
    for time in times:
        sessionsGrid.append([time])
    for presentation in scheduledReader:
        try:
            time = times[presentation.index('1') - 1]
        except ValueError:
            continue
        addToGrid(sessionsGrid, time, addAdvisorName(studentAdvisors, presentation[0]))
    print(sessionsGrid)
    write(sessionsGrid)


generateSessions()

scheduledFile.close()
studentSurveyFile.close()
sessionsFile.close()
