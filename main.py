import gatkSupport
import os
import json


workingFolderEnv = os.environ.setdefault("WORKINGFOLDER", "/data")
if not os.path.isdir(workingFolderEnv):
    raise NotADirectoryError("Unable to find working directory at %s" %workingFolderEnv)
inputFolderEnv = os.environ.setdefault("INPUTFOLDER", os.path.join(workingFolderEnv, "primerTrimBAM"))
performMarkDupsEnv = os.environ.setdefault("MARKDUPLICATES", "0")
if performMarkDupsEnv.upper() in ["0", "FALSE"]:
    performMarkDupsEnv = False
if not os.path.isdir(inputFolderEnv):
    raise NotADirectoryError("Unable to find input folder at %s" %inputFolderEnv)
expectedVariantsFileEnv = os.environ.setdefault("EXPECTEDVARIANTS", os.path.join(inputFolderEnv, "commonVariants.vcf"))
if not os.path.isfile(expectedVariantsFileEnv):
    expectedVariantsFile = None
referenceGenomeFileEnv = os.environ.setdefault("REFGENOME", os.path.join(inputFolderEnv, "reference.fa"))
if not os.path.isfile(referenceGenomeFileEnv):
    referenceGenomeFileEnv = "/home/gatk/references/Sars_cov_2.ASM985889v3.dna_sm.toplevel.fa.gz"
resortedBAMFolderEnv = os.environ.setdefault("RESORTEDFOLDER", os.path.join(workingFolderEnv, "resortBAM"))
if not os.path.isdir(resortedBAMFolderEnv):
    os.mkdir(resortedBAMFolderEnv)
readGroupedFolderEnv = os.environ.setdefault("READGROUPEDFOLDER", os.path.join(workingFolderEnv, "rgBAM"))
if not os.path.isdir(readGroupedFolderEnv):
    os.mkdir(readGroupedFolderEnv)
if performMarkDupsEnv:
    dedupReadFolderEnv = os.environ.setdefault("DEDUPREADFOLDER", os.path.join(workingFolderEnv, "dedupBAM"))
    if not os.path.isdir(dedupReadFolderEnv):
        os.mkdir(dedupReadFolderEnv)
else:
    dedupReadFolderEnv = None
bqsrReadsFolderEnv = os.environ.setdefault("BQSRREADFOLDER", os.path.join(workingFolderEnv, "bqsrBAM"))
if not os.path.isdir(bqsrReadsFolderEnv):
    os.mkdir(bqsrReadsFolderEnv)
rawVCFFolderEnv = os.environ.setdefault("RAWVCFFOLDER", os.path.join(workingFolderEnv, "rawVCF"))
if not os.path.isdir(rawVCFFolderEnv):
    os.mkdir(rawVCFFolderEnv)
depthOfCoverageFolderEnv = os.environ.setdefault("DEPTHOFCOVERAGEFOLDER", os.path.join(rawVCFFolderEnv, "coverage"))
if not os.path.isdir(depthOfCoverageFolderEnv):
    os.mkdir(depthOfCoverageFolderEnv)
filteredVCFFolderEnv = os.environ.setdefault("FILTEREDVCFFOLDER", os.path.join(workingFolderEnv, "filteredVCF"))
if not os.path.isdir(filteredVCFFolderEnv):
    os.mkdir(filteredVCFFolderEnv)
alignmentArtifactFilterFolderEnv = os.environ.setdefault("ALIGNMENTARTIFACTFILTERFOLDER", os.path.join(workingFolderEnv,"alignmentArtifactFilteredVCF"))
if not os.path.isdir(alignmentArtifactFilterFolderEnv):
    os.mkdir(alignmentArtifactFilterFolderEnv)
readgroupsFileEnv = os.environ.setdefault("READGROUPSFILE", os.path.join(workingFolderEnv, "rawBAM", "readgroups.json"))
if not os.path.isfile(readgroupsFileEnv):
    readgroupsFileEnv = None


def markDuplicates(inputFilePath:str, outputFolder:str=dedupReadFolderEnv):
    outputFilePath = gatkSupport.markDuplicates.runMarkDuplicatesSparkParallel(inputFilePath, outputFolder)
    return outputFilePath


def runBQSR(inputFilePath:str, outputFolder:str=bqsrReadsFolderEnv):
    outputFilePath = gatkSupport.bqsr.runBQSRSparkParallel(inputFilePath, outputFolder)
    return outputFilePath


def runMutect2(inputFilePath:str, outputFolder:str=rawVCFFolderEnv):
    rawVCF, orientationBiasFile, mutectBAMOut = gatkSupport.mutect.runMutect2(inputFilePath, outputFolder)
    return rawVCF, orientationBiasFile, mutectBAMOut


def runDepthOfCoverage(inputFilePath:str, outputFolder:str=depthOfCoverageFolderEnv):
    depthOfCoverageFileBaseName = gatkSupport.coverage.runDepthOfCoverage(inputFilePath, outputFolder)
    return depthOfCoverageFileBaseName


def runOrientationBiasFilter(inputVCF:str, orientationBiasFile:str, outputFolder:str=filteredVCFFolderEnv):
    outputFilePath = gatkSupport.orientationBiasFilter.runOrientationBiasFilter(inputVCF, orientationBiasFile, outputFolder)
    return outputFilePath


def getInputBAMFiles(inputFolder:str=inputFolderEnv):
    inputFolderFilesRaw = os.listdir(inputFolder)
    filteredFileList = []
    for file in inputFolderFilesRaw:
        if file.endswith(".bam"):
            filePath = os.path.join(inputFolder, file)
            if os.path.isfile(filePath):
                filteredFileList.append(filePath)
    return filteredFileList


def getReadGroupTable(readGroupFile:str=readgroupsFileEnv):
    if readGroupFile is None:
        print("Failed to find read groups data file.")
        return None
    readGroupFileHandle = open(readGroupFile, 'r')
    readGroupTable = json.load(readGroupFileHandle)
    readGroupFileHandle.close()
    print("Found read group data:\n%s" %readGroupTable)
    return readGroupTable


def addReadGroupData(inputFilePath:str, outputFolder:str=readGroupedFolderEnv, readGroupTable:dict=getReadGroupTable()):
    outputFilePath = gatkSupport.readGroups.runReadGroupAdd(inputFilePath, outputFolder, readGroupTable)
    return outputFilePath


def resortBAMFile(inputFilePath:str, outputFolder:str=resortedBAMFolderEnv, sortByQname:bool=False):
    outputFilePath = gatkSupport.samtools.samtoolsSort(inputFilePath, outputFolder, sortByQname)
    return outputFilePath


def indexBAMFile(inputFilePath:str):
    outputFilePath = gatkSupport.samtools.samtoolsIndexBAM(inputFilePath)
    return outputFilePath


def filterAlignmentArtifacts(inputVCFPath:str, inputBAMPath:str, outputFolder:str=alignmentArtifactFilterFolderEnv):
    outputFilePath = gatkSupport.filterAlignmentArtifact.runFilterAlignmentArtifact(inputVCFPath, inputBAMPath, outputFolder)
    return outputFilePath

def basicMutectFilterArtifacts(inputVCFPath:str, outputFolder:str=filteredVCFFolderEnv):
    outputFilePath = gatkSupport.filterMutectCalls.runFilterMutectCalls(inputVCFPath, outputFolder)
    return outputFilePath


def main():
    inputFileList = getInputBAMFiles()
    completedVCFs = []
    for file in inputFileList:
        resortedBAM = resortBAMFile(file)
        readGroupedBAM = addReadGroupData(resortedBAM)
        if dedupReadFolderEnv:
            deduplicatedBAM = markDuplicates(readGroupedBAM)
        else:
            deduplicatedBAM = readGroupedBAM
        bqsrBAM = runBQSR(deduplicatedBAM)
        rawVCF, orientationBiasFile, mutectBAMOut = runMutect2(bqsrBAM)
        # depthOfCoverageFileBaseName = runDepthOfCoverage(bqsrBAM)
        # orientationFilteredVCF = runOrientationBiasFilter(rawVCF, orientationBiasFile) # Skipping orientation bias analysis, from the looks of the amplicons, there is not expected to be balance with respect to F2R1 and F1R2 values for variants.
        basicFilteredVCF = basicMutectFilterArtifacts(rawVCF)
        # alignmentArtifactFilteredVCF = filterAlignmentArtifacts(basicFilteredVCF, mutectBAMOut) # Non-performant with high depth reads of amplicon panel
        # completedVCFs.append(alignmentArtifactFilteredVCF)
    return completedVCFs


if __name__ == "__main__":
    completedVCFList = main()

