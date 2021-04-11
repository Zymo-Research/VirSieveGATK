import os

gatkExecutable = "/gatk/gatk"
defaultOutputFolder = "/data/rawVC/coverage"
defaultRefSeq = "/home/gatk/references/Sars_cov_2.ASM985889v3.dna_sm.toplevel.fa.gz"
defaultIntervalsFile = "/home/gatk/references/Sars_cov_2.ASM985889v3.dna_sm.toplevel.wholeGenome.bed"


def runDepthOfCoverage(inputFilePath:str, outputFolder:str=defaultOutputFolder, referenceSequence:str=None, intervalsFile:str=None):
    if not os.path.isfile(inputFilePath):
        raise FileNotFoundError("Unable to find input file base quality score recal at %s" % inputFilePath)
    if not referenceSequence:
        referenceSequence = defaultRefSeq
    if not os.path.isfile(referenceSequence):
        raise FileNotFoundError("Unable to find reference sequence at %s" %referenceSequence)
    if not intervalsFile:
        intervalsFile = defaultIntervalsFile
    if not os.path.isfile(intervalsFile):
        raise FileNotFoundError("Unable to find intervals file at %s" %intervalsFile)
    inputFileName = os.path.split(inputFilePath)[1]
    if not os.path.isdir(outputFolder):
        os.mkdir(outputFolder)
    outputFileNameBase = os.path.join(outputFolder, inputFileName.split(".")[0])
    depthOfCoverageCommand = "%s DepthOfCoverage --input %s --output %s --reference %s --intervals %s" %(gatkExecutable, inputFilePath, outputFileNameBase, referenceSequence, intervalsFile)
    print("RUN: %s" %depthOfCoverageCommand)
    exitStatus = os.system(depthOfCoverageCommand)
    if exitStatus != 0:
        raise RuntimeError("Depth of Coverage command failed with non-zero exit status of %s" % exitStatus)
    return outputFileNameBase
