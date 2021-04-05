import os

gatkExecutable = "/gatk/gatk"
defaultOutputFolder = "/data/bqsrBAM"
defaultRefSeq = "/home/gatk/references/Sars_cov_2.ASM985889v3.dna_sm.toplevel.fa.gz"
defaultCommonMutations = "/home/gatk/references/common_SARS-CoV-2_mutations.vcf"


def runBQSRSparkParallel(inputFilePath:str, outputFolder:str=defaultOutputFolder, referenceSequence:str=None, commonMutations:str=None):
    if not os.path.isfile(inputFilePath):
        raise FileNotFoundError("Unable to find input file base quality score recal at %s" % inputFilePath)
    if not referenceSequence:
        referenceSequence = defaultRefSeq
    if not commonMutations:
        commonMutations = defaultCommonMutations
    if not os.path.isfile(referenceSequence):
        raise FileNotFoundError("Unable to find reference sequence at %s" %referenceSequence)
    if not os.path.isfile(commonMutations):
        raise FileNotFoundError("Unable to find known mutations file at %s" % commonMutations)
    outputFileName = os.path.split(inputFilePath)[1][:-4] + ".bqsr.bam"
    outputFilePath = os.path.join(outputFolder, outputFileName)
    bqsrCommand = "%s BQSRPipelineSpark --spark-master local[*] --input %s --output %s --reference %s --known-sites %s" %(gatkExecutable, inputFilePath, outputFilePath, referenceSequence, commonMutations)
    print("RUN: %s" %bqsrCommand)
    exitStatus = os.system(bqsrCommand)
    if exitStatus != 0:
        raise RuntimeError("BQSR command failed with non-zero exit status of %s" % exitStatus)
    return outputFilePath