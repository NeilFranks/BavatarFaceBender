import pyaudio  # from http://people.csail.mit.edu/hubert/pyaudio/
import audioop
import queue
from cmath import exp, pi
import numpy as np
from numpy import *
import pygame
from pygame.display import set_mode
from pygame.draw import rect
from pygame.locals import QUIT, KEYUP, K_ESCAPE, Rect
import math
import time

# from __builtin__ import False


width = 1620
height = 960

relativeVolume = True  # if true, factors in DC

device = 2  # 2 is stereo mix; 0 is mic

chunk = 2 ** 14  # how many samples to chunk together. 2**14 seems nice.
aScale = 100  # restricts size. 10 seems good
exponent = 1  # changes difference between highs and lows. 0.5 seems good
samplerate = 44100  # 44100 * 6 seems good (but is it bad practice?)

DC = 2  # direct current, will keep rolling average
DCRollLength = 200
DCQueue = queue.Queue(DCRollLength)

# for peak detection
dfft = []
dfftLength = 2048
dfftLengthLog2 = np.log2(dfftLength)
compareLength = 7
debugPeak = False
peakRollLength = 3
peakQueue = queue.Queue(peakRollLength)

# noteArr in dfft with sample rate of 44100
A = set([10, 20, 41, 82, 163, 327, 654, 1308])
ASh = set([11, 22, 43, 87, 173, 346, 693, 1386])
B = set([11, 23, 46, 92, 183, 367, 734, 1468])
C = set([6, 12, 24, 49, 97, 194, 389, 778, 1555])
CSh = set([6, 13, 26, 51, 103, 206, 412, 824, 1648])
D = set([7, 14, 27, 55, 109, 218, 436, 873, 1746])
DSh = set([7, 14, 29, 58, 116, 231, 462, 925, 1849])
E = set([8, 15, 31, 61, 122, 245, 490, 980, 1959])
F = set([8, 16, 32, 65, 130, 259, 519, 1038])
FSh = set([9, 17, 34, 69, 137, 275, 550, 1100])
G = set([9, 18, 36, 73, 146, 291, 583, 1165])
GSh = set([10, 19, 39, 77, 154, 309, 617, 1234])

noteArr = [A, ASh, B, C, CSh, D, DSh, E, F, FSh, G, GSh]
noteVals = A | ASh | B | C | CSh | D | DSh | E | F | FSh | G | GSh


noteNames = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]


def drawLevels(values):

    N = len(values)

    for x in range(N):
        if values[x] > 50:
            pygame.draw.rect(
                display,
                (255, 255, 255),
                Rect(x * width / N, height - (values[x] - 50) ** 1.5, 2, 2),
            )


def drawShape(scale):

    global dodCount

    # Pygame stuff
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


def mapSingleNote(peak):  # simple method of finding the index in array of notes
    if peak >= 12:  # start getting mostly unnique notes at 12
        for i in range(len(noteArr)):
            for note in noteArr[i]:
                # print "note:" + str(note)
                if peak > 0.9727 * note and peak < 1.029 * note:
                    print(noteNames[i])


def findNotes(peakInds, peakVals):

    numPeaks = len(peakInds)
    lowValWeight = 0.15  # for weighting lower freqs more than higher freqs

    N = len(noteArr)
    noteCount = [0] * N

    for i in range(N):
        for j in range(numPeaks):
            for note in noteArr[i]:
                # print "note:" + str(note)
                # check if frequency is close enough to a freq of note
                if peakInds[j] > 0.9727 * note and peakInds[j] < 1.029 * note:
                    # add the strength of the freq to the note in noteCount
                    noteCount[i] += (
                        peakVals[j]
                        * ((dfftLengthLog2 - np.log2(peakInds[j])) / dfftLengthLog2)
                        ** 2
                    )
                    # noteCount[i] += 1

    maxCount = max(noteCount)

    #     print peakInds
    #     print peakVals
    #     print noteCount

    # check if you registered frequencies high enough to indicate a unique note
    unique = (
        False
    )  # unique indices are 15 and above. everything below that is triggered by 2+ noteArr
    for ind in peakInds:
        if ind >= 12:
            unique = True

    if unique and maxCount > 0:
        for i in range(N):
            # print all notes at least 90% of power of max note
            if noteCount[i] >= 0.9 * maxCount:
                print(noteNames[i])


def dfftArea(freqs, limit):

    N = len(freqs)
    area = 0

    for idx in range(N):
        if freqs[idx] > limit:
            area += freqs[idx] - limit

    return area


def findLR(freqs, limit, area):

    N = len(freqs)
    weightedSum = 0

    for idx in range(N):
        if freqs[idx] > limit:
            weightedSum += idx * float(freqs[idx] - limit) / area

    return weightedSum / N


def countCrosses(freqs, limit):

    N = len(freqs)
    crosses = 0

    for idx in range(N - 1):
        if (freqs[idx] > limit and freqs[idx + 1] <= limit) or (
            freqs[idx] <= limit and freqs[idx + 1] > limit
        ):
            crosses += 1

    return crosses


def findPeaks(freqs, limit, offset):
    # returns indices of peaks and their values
    """
    NOTE: crisp noise has distinct peaks. fuzzy noise is more uniform but still has peaks
    TODO: exploit with further scrutiny and conditions
    """

    indexList = []
    valueList = []

    N = len(freqs)

    subN = 3  # smaller section of dfft
    halfSubN = subN / 2
    subMean = -1  # initialize subMean

    # check all elements for peaks
    for idx in range(0, N):
        # silence is somewhere from teeens to 30s.
        # peak should be above a certain limit
        if freqs[idx] > limit and N > 0:

            if idx < halfSubN:  # looking at first subN/2 elements in freqs
                if freqs[idx] > freqs[idx + 1]:
                    indexList.append(idx + offset)
                    valueList.append(freqs[idx])
            elif idx > (N - 1) - halfSubN:  # looking at last subN/2 elements
                if freqs[idx] > freqs[idx - 1]:
                    indexList.append(idx + offset)
                    valueList.append(freqs[idx])
            else:  # looking at subN/2 : (N-1)-subN/2 elements
                if freqs[idx - 1] < freqs[idx] and freqs[idx] > freqs[idx + 1]:
                    indexList.append(idx + offset)
                    valueList.append(freqs[idx])

    return (indexList, valueList)


def getVolume(data, relativeVol):
    rms = audioop.rms(data, 2)
    level = min(rms / (2.0 ** 16) * aScale, 1.0)
    level = float(level) ** exponent
    # print 'Level:' + str(level)

    if relativeVol:
        # calculate DC; open up average and refind average
        if DCQueue.full():
            DCQueue.get(True, None)  # dequeue
            DCQueue.put(level, True, None)  # enqueue
        else:
            DCQueue.put(level, True, None)  # enqueue

        sum = 0
        for sample in list(DCQueue.queue):
            sum += sample
            # print 'sample: ' + str(sample)
            # print 'sum: ' + str(sum)

        DC = sum / DCQueue.qsize()
        # print 'DC:' + str(DC)

        if DC > 0:
            relativeLevel = level / DC
        else:
            relativeLevel = level

        # scale will be for the shape
        scale = relativeLevel
        # print scale
    else:
        scale = 200000 * level + 1
        # print scale

    return scale


def devices():

    # list audio input devices
    p = pyaudio.PyAudio()
    i = 0
    n = p.get_device_count()
    while i < n:
        device = p.get_device_info_by_index(i)
        if device["maxInputChannels"] > 0:
            print(str(i) + ": " + device["name"])
        i += 1


class filter:  # filter is used to only respond to certain frequencies at certain strengths
    class __metaclass__(type):
        def __iter__(self):
            for attr in dir(filter):
                if not attr.startswith("__"):
                    yield attr

    def __init__(self, startX, endX, Y):
        self.start = (startX, Y)
        self.end = (endX, Y)
        self.handleSize = 5
        self.moveStart = False
        self.moveEnd = False

    def draw(self):
        # draw line
        pygame.draw.line(display, (255, 0, 0), self.start, self.end, 1)

        # draw start point handle
        pygame.draw.rect(
            display,
            (0, 255, 255),
            Rect(
                self.start[0] - self.handleSize / 2,
                self.start[1] - self.handleSize / 2,
                self.handleSize,
                self.handleSize,
            ),
        )

        # draw end point handle
        pygame.draw.rect(
            display,
            (0, 255, 255),
            Rect(
                self.end[0] - self.handleSize / 2,
                self.end[1] - self.handleSize / 2,
                self.handleSize,
                self.handleSize,
            ),
        )

    def task(self, subDfft, filter, rangeStart, totalPeaks):

        peaksInRange = []
        peakValues = []
        # find peaks with indices within range
        for peakIdx in totalPeaks[0]:
            if (
                rangeStart < peakIdx < rangeStart + len(subDfft)
                and subDfft[peakIdx - rangeStart] > filter
            ):
                peaksInRange.append(peakIdx)
                peakValues.append(subDfft[peakIdx - rangeStart])
                # print peakIdx

        if len(peaksInRange) > 0:
            filterCrosses = countCrosses(subDfft, filter)
            area = dfftArea(subDfft, filter)
            LRPercent = findLR(subDfft, filter, area)
            # print peaksInRange
            noteArr = findNotes(peaksInRange, peakValues)
            # for peak in peaksInRange:
            # mapSingleNote(peak)

            pygame.draw.rect(
                display,
                (100, 100, 255),
                Rect(
                    self.start[0] + LRPercent * (self.end[0] - self.start[0]),
                    50,
                    30,
                    area,
                ),
            )
            pygame.display.flip()

    def updateStart(self, newStart):
        self.start = newStart

    def updateEnd(self, newEnd):
        self.end = newEnd

    def startOnLeft(self):

        # make sure start is always on the left
        if self.start[0] > self.end[0]:
            temp = self.start
            self.start = self.end
            self.end = temp
            temp = self.moveStart
            self.moveStart = self.moveEnd
            self.moveEnd = temp

    def inStart(self, coordinates):
        if (
            self.start[0] - self.handleSize
            < coordinates[0]
            < self.start[0] + self.handleSize
            and self.start[1] - self.handleSize
            < coordinates[1]
            < self.start[1] + self.handleSize
        ):
            return True
        else:
            return False

    def inEnd(self, coordinates):
        if (
            self.end[0] - self.handleSize
            < coordinates[0]
            < self.end[0] + self.handleSize
            and self.end[1] - self.handleSize
            < coordinates[1]
            < self.end[1] + self.handleSize
        ):
            return True
        else:
            return False


def listen():

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=2,
        rate=samplerate,
        input=True,
        frames_per_buffer=chunk,
        input_device_index=device,
    )

    pygame.init()
    global display
    display = pygame.display.set_mode((width, height))
    display.fill((0, 0, 0))

    filters = []
    #     # filter on roughly every octave
    #     filters.append(filter(0, 40, 910))
    #     filters.append(filter(40, 80, 900))
    #     filters.append(filter(80, 160, 895))
    #     filters.append(filter(160, 320, 900))
    #     filters.append(filter(320, 640, 920))
    #     filters.append(filter(640, 1280, 935))
    #     filters.append(filter(1280, width, 930))

    filters.append(filter(0, 85, 910))  # left hand of piano
    # filters.append(filter(100, width, 930))

    for i in range(10):
        data = stream.read(chunk)  # data has anomolies for first few reading

    while True:
        data = stream.read(chunk)  # data has anomolies for first few reading

        volume = getVolume(data, relativeVolume)

        # drawShape(volume)

        arr = np.frombuffer(data, np.int16)
        dfft = 10.0 * np.log10(abs(np.fft.rfft(arr)))
        # dfft has CHUNK/2 floats

        # looks to me like only first 200 or so are relevant
        dfft = dfft[0:dfftLength]

        # (peakFreqs, peakValues) = findPeaks(dfft)

        display.fill((0, 0, 0))
        drawLevels(dfft)
        for f in filters:
            f.draw()

        pygame.display.flip()

        #             if debugPeak:
        #                  print dfft
        #                  print 'freqs: ' + str(peakFreqs)
        #                  print 'values: ' + str(peakValues)
        #
        #              if len(peakValues) > 0:
        #                  # sort values, greatest in front
        #                  sortedPeakValues = sorted(peakValues)
        #                  sortedPeakValues.reverse()
        #
        #                  sortedPeakFreqs = []
        #                  for peak in sortedPeakValues:
        #                      idx = peakValues.index(peak)
        #                      sortedPeakFreqs.append(peakFreqs[idx])
        #
        #                  # print 'f: ' + str(sortedPeakFreqs)
        #                  # print 'v: ' + str(sortedPeakValues)
        #                  if not peakQueue.full():
        #                      peakQueue.put(sortedPeakFreqs, True, None)  # enqueue
        #                  else:
        #                      peakQueue.get(True, None)  # dequeue
        #                      peakQueue.put(sortedPeakFreqs, True, None)  # enqueue
        #
        #                  print 'Start'
        #                  for q in list(peakQueue.queue):
        #                      print q

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cursor = pygame.mouse.get_pos()

                # check if clicked on filter handle, and if you did then
                # indicate it with boolean. stay true until mousebuttonup
                for f in filters:
                    if f.inStart(cursor) and not f.moveEnd:
                        f.moveStart = True
                    elif f.inEnd(cursor) and not f.moveStart:
                        f.moveEnd = True

            elif event.type == pygame.MOUSEBUTTONUP:
                for f in filters:
                    f.moveStart = False
                    f.moveEnd = False

        for f in filters:
            if f.moveStart:
                cursor = pygame.mouse.get_pos()

                # only support horizontal lines
                f.updateStart(cursor)
                f.updateEnd((f.end[0], cursor[1]))

                f.startOnLeft()

            elif f.moveEnd:
                cursor = pygame.mouse.get_pos()

                # only support horizontal lines
                f.updateStart((f.start[0], cursor[1]))
                f.updateEnd(cursor)

                f.startOnLeft()

            # check if at least one level in dfft crosses filter
            if f.end[0] * dfftLength / width - f.start[0] * dfftLength / width > 0:
                maxInRange = max(
                    dfft[
                        math.floor(f.start[0] * dfftLength / width) : math.floor(f.end[0] * dfftLength / width)
                    ]
                )  # compensate for how dfft was displayed

                maxIndex = list(dfft).index(maxInRange)

                diff = f.start[1] - (height - (dfft[maxIndex] - 50) ** 1.5)
                if diff > 0:
                    # send (dfft values in range, equivalent cutoff due to
                    # filter) to a task
                    rangeStart = f.start[0] * dfftLength / width
                    rangeEnd = f.end[0] * dfftLength / width

                    relativeFilter = float(height - f.start[1]) ** (0.6667) + 50

                    totalPeaks = findPeaks(dfft, 0, 0)

                    f.task(
                        dfft[rangeStart:rangeEnd],
                        relativeFilter,
                        rangeStart,
                        totalPeaks,
                    )

    # close everything
    stream.stop_stream()
    stream.close()
    p.terminate()

def hmm():
    # Import and initialize the pygame library
    import pygame
    pygame.init()

    # Set up the drawing window
    screen = pygame.display.set_mode([500, 500])

    # Run until the user asks to quit
    running = True
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with white
        screen.fill((255, 255, 255))

        # Draw a solid blue circle in the center
        pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

        # Flip the display
        pygame.display.flip()

# Done! Time to quit.
pygame.quit()


# devices()
# listen()
hmm()
