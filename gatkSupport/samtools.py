import os
import multiprocessing

samtoolsExecutable = "/usr/bin/samtools"
cpuCount = multiprocessing.cpu_count()


def samtoolsIndexBAM(inputFilePath:str, outputFilePath:str=None, forceRun:bool=False):
    if not outputFilePath:
        outputFilePath = inputFilePath + ".bai"
    if not forceRun and os.path.isfile(outputFilePath):
        return outputFilePath
    samtoolsIndexCommand = "%s index %s %s" % (samtoolsExecutable, inputFilePath, outputFilePath)
    print("RUN: %s" % samtoolsIndexCommand)
    exitStatus = os.system(samtoolsIndexCommand)
    if exitStatus != 0:
        raise RuntimeError("Index command returned a non-zero exit status.")
    return outputFilePath


def samtoolsSort(inputFilePath:str, outputFolder:str=None, sortByQname:bool=False):
    if not os.path.isfile(inputFilePath):
        raise FileNotFoundError("Unable to find input file base quality score recal at %s" % inputFilePath)
    if sortByQname:
        outputFileName = os.path.split(inputFilePath)[1][:-4] + ".resortedQN.bam"
        sortTypeFlag = " -n"
    else:
        outputFileName = os.path.split(inputFilePath)[1][:-4] + ".resorted.bam"
        sortTypeFlag = ""
    outputFilePath = os.path.join(outputFolder, outputFileName)
    samtoolsSortCommand = "%s sort -@%s%s -o %s %s" %(samtoolsExecutable, cpuCount, sortTypeFlag, outputFilePath, inputFilePath) #samtoolsSort automatically adding bam, fixing with the slice operation
    print("RUN: %s" %samtoolsSortCommand)
    exitStatus = os.system(samtoolsSortCommand)
    if exitStatus != 0:
        raise RuntimeError("BAM sort command returned a non-zero exit status.")
    return outputFilePath