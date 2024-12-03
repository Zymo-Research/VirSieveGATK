import os

gatkExecutable = "/gatk/gatk"
defaultOutputFolder = "/data/basicFilteredVCF"
defaultRefSeq = "/home/gatk/references/Sars_cov_2.ASM985889v3.dna_sm.toplevel.fa.gz"
defaultBWAMemIndexImage = "/home/gatk/references/Sars_cov_2.ASM985889v3.dna_sm.toplevel.fa.img"


def runFilterMutectCalls(inputVCFPath:str, outputFolder:str=defaultOutputFolder, referenceSequence:str=None):
    if not os.path.isfile(inputVCFPath):
        raise FileNotFoundError("Unable to find input file base quality score recal at %s" % inputVCFPath)
    if not referenceSequence:
        referenceSequence = defaultRefSeq
    outputFileName = os.path.split(inputVCFPath)[1][:-4] + ".basicFilter.vcf"
    outputFilePath = os.path.join(outputFolder, outputFileName)
    basicMutectFilterCommand = "%s FilterMutectCalls --reference %s --mitochondria-mode true --variant %s --output %s" % (gatkExecutable, referenceSequence, inputVCFPath, outputFilePath)
    print("RUN: %s" %basicMutectFilterCommand)
    exitStatus = os.system(basicMutectFilterCommand)
    if exitStatus != 0:
        raise RuntimeError("Basic mutect filtering command failed with non-zero exit status of %s" % exitStatus)
    return outputFilePath