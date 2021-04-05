import os

gatkExecutable = "/gatk/gatk"
defaultOutputFolder = "/data/readgroupBAM"


def runReadGroupAdd(inputFilePath:str, outputFolder:str=defaultOutputFolder, readgroupTable:dict=None):
    if readgroupTable is None:
        readgroupTable = {}
    if not os.path.isfile(inputFilePath):
        raise FileNotFoundError("Unable to find input file for adding read groups at %s" % inputFilePath)
    outputFileName = os.path.split(inputFilePath)[1][:-4] + ".readgroup.bam"
    fileBase = outputFileName.split(".")[0]
    defaultReadGroupString = "RGPL=Illumina RGLB=LaneX RGPU=NONE RGSM=%s" %fileBase
    if fileBase in readgroupTable:
        readGroupString = readgroupTable[fileBase]
        if not "RGPL=" in readGroupString:
            readGroupString += " RGPL=ILLUMINA"
    else:
        readGroupString = defaultReadGroupString
    outputFilePath = os.path.join(outputFolder, outputFileName)
    readgroupCommand = "%s AddOrReplaceReadGroups I=%s O=%s %s" %(gatkExecutable, inputFilePath, outputFilePath, readGroupString)
    print("RUN: %s" %readgroupCommand)
    exitStatus = os.system(readgroupCommand)
    if exitStatus != 0:
        raise RuntimeError("Add/replace read groups command failed with non-zero exit status of %s" % exitStatus)
    return outputFilePath