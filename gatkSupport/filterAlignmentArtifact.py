import os

gatkExecutable = "/gatk/gatk"
defaultOutputFolder = "/data/alignmentArtifactFilteredVCF"
defaultRefSeq = "/home/gatk/references/Sars_cov_2.ASM985889v3.dna_sm.toplevel.fa.gz"
defaultBWAMemIndexImage = "/home/gatk/references/Sars_cov_2.ASM985889v3.dna_sm.toplevel.fa.img"


def runFilterAlignmentArtifact(inputVCFPath:str, inputBAMPath:str, outputFolder:str=defaultOutputFolder, referenceSequence:str=None, bwaMemIndexImage:str=None):
    if not os.path.isfile(inputVCFPath):
        raise FileNotFoundError("Unable to find input file base quality score recal at %s" % inputVCFPath)
    if not os.path.isfile(inputBAMPath):
        raise FileNotFoundError("Unable to find GATK BAM output file at %s" %inputBAMPath)
    if not referenceSequence:
        referenceSequence = defaultRefSeq
    if not bwaMemIndexImage:
        bwaMemIndexImage = defaultBWAMemIndexImage
    if not os.path.isfile(bwaMemIndexImage):
        raise FileNotFoundError("Unable to find orientation bias data at %s" %bwaMemIndexImage)
    outputFileName = os.path.split(inputVCFPath)[1][:-4] + ".alignmentArtifactFilter.vcf"
    outputFilePath = os.path.join(outputFolder, outputFileName)
    alignmentArtifactFilterCommand = "%s FilterAlignmentArtifacts --reference %s --variant %s --input %s --bwa-mem-index-image %s --output %s" % (gatkExecutable, referenceSequence, inputVCFPath, inputBAMPath, bwaMemIndexImage, outputFilePath)
    print("RUN: %s" %alignmentArtifactFilterCommand)
    exitStatus = os.system(alignmentArtifactFilterCommand)
    if exitStatus != 0:
        # raise RuntimeError("Filter alignment artifact command failed with non-zero exit status of %s" % exitStatus)
        # NOT CRASHING OUT ON THIS ONE BECAUSE THERE APPEARS TO BE A REPRODUCIBLE SEGFAULT IN THE GATK FUNCTIONALITY HERE
        if os.path.isfile(outputFilePath):
            os.remove(outputFilePath)
        print("Filter alignment artifact command failed with non-zero exit status of %s" %exitStatus)
        print("This may be due to a known segfault in the GATK function, please see above to see if that was the case.  If not, please file a bug report.")
    return outputFilePath