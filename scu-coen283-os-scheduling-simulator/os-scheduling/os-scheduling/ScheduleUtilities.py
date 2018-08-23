import os
import datetime

import Machine
import Process

"""
Utility functions for schedule toolset
"""

def open_output_file(fileName, ext):
    """
    opens an output file in the outputfile directory
    :param fileName: name of the file
    :param ext: extension  of the file
    :return: output file handle
    """

    # create an output directory
    outputPath = "./output"
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    # create a unique file extension name based on date
    # dateExt = datetime.datetime.today().strftime('%m_%d_%y')
    # dateExt = ""

    # open a file for saving & viewing the simulation in excel
    longFileName = outputPath + "/" + fileName
    theFile = None

    try:
        theFile = open(longFileName + ".csv", "w")
    except IOError:
        print("ERROR: opening the file " + longFileName)
        exit(-1)

    return theFile
