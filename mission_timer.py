"""
Mission Timer

I want a way of keeping track of many projects and their start and end dates.
e.g. for undergraduate projects.

Ideally this would take the form of a NASA style mission clock displaying
four key pieces of information:

1) Start time
2) Ellapsed time
3) Remaining time
4) End time

I can imagine providing information to this from a simple text file that
contains

i) Project name
ii) Start time
iii) End time

Then a python script will use Tinker to display a gui and update the displayed
times according to an ongoing update cycle.

Probably the best structure for this is for each mission to be represented by
a class. Then the Tinker display would be a base structure to create the base
canvas and update cycle. Each mission class would provide the Tinker code for
drawing the four time elements.

Not sure how to run to Tkinter update cycle. There's a function Tkinter.after
that seems to be the key

"""

import time
import datetime
from datetime import timedelta
import Tkinter
from Tkconstants import *
import numpy as np
#from PIL import Image, ImageTk

#ultimately read in information from a CSV file
missionfile = "missionfile.csv"

def unpacktime(totalseconds):
    """ There must be an inbuilt function for this
    but convert seconds into day, seconds for use in
    deltatime
    
    returns days, seconds
    """
    
    day = 3600 * 24  #number of seconds in a day
    
    days = totalseconds / day
    seconds = totalseconds - days * day
    
    return days, seconds

def strfdelta(delta):
    """
    Take a timedelta and reformat to a nice looking string
    """
    s = delta.total_seconds()
    days, remainder = divmod(s, 3600*24)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '%i:%02i:%02i:%02i' % (days, hours, minutes, seconds)


class Mission:
    """
    Class containing information for Mission clocks
    """
    def __init__(self, startTime, endTime, name="Default Mission"):
        """
        Provide start and end times in seconds from UNIX epoch
        """

        self.name = name

        try:
            self.startTime = self.calendarDateToSeconds(startTime)
        except:
            self.startTime = startTime

        try:
            self.endTime = self.calendarDateToSeconds(endTime)
        except:
            self.endTime = endTime


        #Now calculate all times
        self.updateTimes()

    def __repr__(self):
        start = time.asctime(time.localtime(self.startTime))
        end = time.asctime(time.localtime(self.endTime))
        return "Mission(Start: %s End: %s)" % (start, end)


    def calendarDateToSeconds(self, usetime):
        """
        From input create a time_struct and convert to seconds from the
        UNIX base epoch

        Input sequence with (day, month, year, hour, minutes)
        """

        day, month, year, hour, minutes = usetime

        #fill in some default values - DOESNT GET WEEKDAY RIGHT
        #MUST BE SOME BETTER WAY OF SETTING THIS
        seconds = 0
        wday = 0
        yday = 1
        isdst = -1

        #Create time structure
        #moment = time.struct_time(
        #    [year, month, day, hour, minutes, seconds, wday, yday, isdst])

        moment = datetime.datetime(year, month, day, hour, minutes)

        #print moment.timetuple()
        #print time.asctime(moment)

        momentsec = time.mktime(moment.timetuple())

        return momentsec
    

    def drawclock(self, time):
        """ Initial draw of the graphical display
        """
        pass
        


    def updateTimes(self):
        """ Recalculate key times based on system clock
        """

        systime = time.time()
        self.ellapsedTime = systime - self.startTime
        self.remainingTime = self.endTime - systime

        return (self.startTime, self.endTime, self.ellapsedTime, self.remainingTime)
              

    def updateFaces(self):
        """ Redraw the graphical display of the times
        """

        # First get the (start, ellapsed, remaining, end) times
        # in a format that is useful for displaying things.
        start = time.asctime(time.localtime(self.startTime))
        print start
        
        days, seconds = unpacktime(self.ellapsedTime)
        ellapsed = timedelta(days, seconds)
        print ellapsed

        days, seconds = unpacktime(self.remainingTime)
        remaining = timedelta(days, seconds)
        print remaining

        end = time.asctime(time.localtime(self.endTime))
        print end
        return (start, end, ellapsed, remaining)

        
    def updateAll(self):
        """
        update time stamps and redraw
        """
        time = self.updateTimes()
        self.updateFaces()
        return times

class Face:
    """ Class to handle the drawing of the clock faces

    Takes as argument a Mission instance and a Tkinter Canvas instance
    """

    facecount = 0 
    
    def __init__(self, mission, parent):

        #counter of all Face instances
        Face.facecount += 1
        self.facenumber = 1

        self.cwidth = 10
        self.cheight = 1
        self.parent = parent
        self.mission = mission

        #frame = Tkinter.Frame(parent, relief=RIDGE, borderwidth=2)
        #frame.pack(fill=BOTH, expand=1)
        #frame.grid(row=(self.facecount-1), column=1)
        label = Tkinter.Label(parent, text=self.mission.name)
        #label.pack(fill=X, expand=1)
        label.grid(row=(Face.facecount-1), column=self.facenumber)

        #Store ID pointers for faces in a list
        self.faces = []
        start, end, ellapsed, remaining = self.mission.updateTimes()
        timelabel = time.strftime("%d/%m/%y",time.localtime(start))
        self.faces.append(self.drawFace(timelabel, parent))

        days, seconds = unpacktime(ellapsed)
        ellapsed = timedelta(days, seconds)
        timelabel = strfdelta(ellapsed)
        self.faces.append(self.drawFace(timelabel, parent))

        days, seconds = unpacktime(remaining)
        remaining = timedelta(days, seconds)
        timelabel = strfdelta(remaining)
        self.faces.append(self.drawFace(timelabel, parent))

        timelabel = time.strftime("%d/%m/%y",time.localtime(end))
        self.faces.append(self.drawFace(timelabel, parent))

        #Update faces and start loop
        self.updateFaces()
        
        
    def drawFace(self, timelabel, parent):
        #ID= Tkinter.Canvas(parent, width=self.cwidth, height=self.cheight)
        v = Tkinter.StringVar()
        ID = Tkinter.Label(parent, textvariable=v, height =self.cheight, width = self.cwidth)
        v.set(timelabel)
        #ID.pack(side=LEFT)
        self.facenumber += 1
        ID.grid(row=(Face.facecount-1), column=self.facenumber)
        
        return ID, v


    def updateFaces(self):
        #print self.mission.name
        start, end, ellapsed, remaining = self.mission.updateTimes()
        for i, (ID, v) in enumerate(self.faces):
            if i==0:                        
                timelabel = time.strftime("%d/%m/%y",time.localtime(start))
            elif i==1:
                days, seconds = unpacktime(ellapsed)
                ellapsed = timedelta(days, seconds)
                timelabel = strfdelta(ellapsed)
            elif i==2:
                days, seconds = unpacktime(remaining)
                remaining = timedelta(days, seconds)
                timelabel = strfdelta(remaining)                
            elif i==3:                        
                timelabel = time.strftime("%d/%m/%y",time.localtime(end))                
            v.set(timelabel)
        
        #finally begin an autoupdate cycle of the clock faces
        self.parent.after(10, self.updateFaces)


def parsemissionfile(filename = missionfile):
    """
    Readin the Mission data from a comma separated file containing
    Name, DD-MM-YYYY, DD-MM-YYYY
    format entries.

    Returns a list of Mission instances.
    """

    missions = []
    file = open(filename)
    for line in file:
        data = line.strip().split(',')
        if len(data) == 3:
            name = data[0]
            date1 = data[1].split('-')
            date2 = data[2].split('-')
            missions.append(
                Mission([int(date1[0]),int(date1[1]),int(date1[2]),23,59],
                        [int(date2[0]),int(date2[1]),int(date2[2]),23,59],
                        name)
                )

    #Return missions sorted by the one that will expire soonest
    return sorted(missions, key=lambda x: x.remainingTime, reverse=False)
    #return missions
            

def main():
    root = Tkinter.Tk()

    #mission1 = Mission([26,7,2015,12,00], [27,12,2015,12,00],"Test 1")
    #myapp1 = Face(mission1, root)

    
    #mission2 = Mission([26,1,2014,12,00], [27,12,2015,12,00], "Test 2")
    #myapp = Face(mission2, root)

    #read in the mission data from missionfile
    missions = parsemissionfile(missionfile)
    myapps = []

    #initialise the clock faces, which triggers an autoupdate cycle
    for mission in missions:
        myapps.append(Face(mission, root))
    
    
    root.mainloop()

if __name__ == '__main__':
    main()
