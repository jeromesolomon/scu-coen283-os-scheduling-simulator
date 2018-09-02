import os
import datetime

import Machine
import Process

"""
Utility functions for schedule toolset
"""


def open_output_file(algorithmName, fileName, ext, mode):
    """
    opens an output file in the outputfile directory
    :param fileName: name of the file
    :param ext: extension  of the file
    :return: output file handle
    """

    # create a unique folder name based on date
    dirExt = datetime.datetime.today().strftime('%m_%d_%y_%H_%M_%S')
    dirExt = algorithmName

    outputPath = "./output/" + dirExt
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    # open a file for saving & viewing the simulation in excel
    longFileName = outputPath + "/" + fileName

    # try to open the file
    theFile = None
    theFileName = longFileName + "." + ext

    try:
        # remove the file if it already exists
        if os.path.isfile(theFileName):
            os.remove(theFileName)

        # try to open the file
        theFile = open(theFileName, mode)

    except IOError:
        print("ERROR: opening the file " + longFileName)
        exit(-1)

    return theFile
