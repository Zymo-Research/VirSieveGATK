import os

gatkExecutable = "/gatk/gatk"
defaultOutputFolder = "/data/rawVC"
defaultRefSeq = "/home/gatk/references/Sars_cov_2.ASM985889v3.dna_sm.toplevel.fa.gz"


def runMutect2(inputFilePath:str, outputFolder:str=defaultOutputFolder, referenceSequence:str=None):
    if not os.path.isfile(inputFilePath):
        raise FileNotFoundError("Unable to find input file base quality score recal at %s" % inputFilePath)
    if not referenceSequence:
        referenceSequence = defaultRefSeq
    if not os.path.isfile(referenceSequence):
        raise FileNotFoundError("Unable to find reference sequence at %s" %referenceSequence)
    inputFileName = os.path.split(inputFilePath)[1]
    outputFileName = inputFileName.split(".")[0] + ".vcf"
    orientationBiasFileName = outputFileName + ".orientationBias.tar.gz"
    mutectAssemblyBAMFolder = os.path.join(outputFolder, "mutectBAM")
    if not os.path.isdir(mutectAssemblyBAMFolder):
        os.mkdir(mutectAssemblyBAMFolder)
    mutectAssemblyBAMName = outputFileName[:-4] + ".mutect2.bam"
    mutectAssemblyBAMPath = os.path.join(mutectAssemblyBAMFolder, mutectAssemblyBAMName)
    outputFilePath = os.path.join(outputFolder, outputFileName)
    orientationBiasFilePath = os.path.join(outputFolder, orientationBiasFileName)
    mutectCommand = "%s Mutect2 --input %s --output %s --reference %s --f1r2-tar-gz %s --bam-output %s --create-output-bam-index" %(gatkExecutable, inputFilePath, outputFilePath, referenceSequence, orientationBiasFilePath, mutectAssemblyBAMPath)
    print("RUN: %s" %mutectCommand)
    exitStatus = os.system(mutectCommand)
    if exitStatus != 0:
        raise RuntimeError("Mutect2 command failed with non-zero exit status of %s" % exitStatus)
    return outputFilePath, orientationBiasFilePath, mutectAssemblyBAMPath