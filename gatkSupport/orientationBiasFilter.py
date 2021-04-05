import os

gatkExecutable = "/gatk/gatk"
defaultOutputFolder = "/data/filterVC"
defaultRefSeq = "/home/gatk/references/Sars_cov_2.ASM985889v3.dna_sm.toplevel.fa.gz"


def runOrientationBiasFilter(inputFilePath:str, orientationBiasDataFile:str=None, outputFolder:str=defaultOutputFolder, referenceSequence:str=None):
    if not os.path.isfile(inputFilePath):
        raise FileNotFoundError("Unable to find input file base quality score recal at %s" % inputFilePath)
    if not referenceSequence:
        referenceSequence = defaultRefSeq
    if not orientationBiasDataFile:
        orientationBiasDataFile = inputFilePath + ".orientationBias.tar.gz"
    if not os.path.isfile(orientationBiasDataFile):
        raise FileNotFoundError("Unable to find orientation bias data at %s" %orientationBiasDataFile)
    orientationModelFileName = os.path.split(inputFilePath)[1][:-4] + ".orientationModel.tar.gz"
    orientationModelFilePath = os.path.join(outputFolder, orientationModelFileName)
    outputFileName = os.path.split(inputFilePath)[1][:-4] + ".orientationFilter.vcf"
    outputFilePath = os.path.join(outputFolder, outputFileName)
    learnOrientationModelCommand = "%s LearnReadOrientationModel --input %s --output %s" %(gatkExecutable, orientationBiasDataFile, orientationModelFilePath)
    print("RUN: %s" %learnOrientationModelCommand)
    exitStatus = os.system(learnOrientationModelCommand)
    if exitStatus != 0:
        raise RuntimeError("Learn orientation model command failed with non-zero exit status of %s" % exitStatus)
    filterCallsCommand = "%s FilterMutectCalls -V %s --reference %s  --ob-priors %s --output %s" %(gatkExecutable, inputFilePath, referenceSequence, orientationModelFilePath, outputFilePath)
    print("RUN: %s" %filterCallsCommand)
    exitStatus = os.system(filterCallsCommand)
    if exitStatus != 0:
        raise RuntimeError("Filter calls command failed with a non-zero exit status of %s" %exitStatus)
    return outputFilePath