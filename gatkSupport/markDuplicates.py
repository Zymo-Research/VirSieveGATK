import os

gatkExecutable = "/gatk/gatk"
defaultOutputFolder = "/data/dedupBAM"


def runMarkDuplicatesSparkParallel(inputFilePath:str, outputFolder:str=defaultOutputFolder, referenceSequence:str=None):
    if not os.path.isfile(inputFilePath):
        raise FileNotFoundError("Unable to find input file for marking duplicates at %s" % inputFilePath)
    outputFileName = os.path.split(inputFilePath)[1][:-4] + ".dedup.bam"
    outputFilePath = os.path.join(outputFolder, outputFileName)
    dedupCommand = "%s MarkDuplicatesSpark --spark-master local[*] --input %s --output %s" %(gatkExecutable, inputFilePath, outputFilePath)
    print("RUN: %s" %dedupCommand)
    exitStatus = os.system(dedupCommand)
    if exitStatus != 0:
        raise RuntimeError("Mark duplicates command failed with non-zero exit status of %s" % exitStatus)
    return outputFilePath