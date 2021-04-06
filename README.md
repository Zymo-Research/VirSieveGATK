# VirSieve GATK

## Summary

This container is part of the Environmental Viral Detection pipeline and covers variant analysis and filtering with GATK.  This operation requires processed BAM files from previous steps as well as a reference genome.  The reference genome is built in to the container for ease of use and consistency.

**SECURITY CONCERN**: This pipeline is currently using os.system to run commands and sanitization was causing runs to fail. If running files from untrusted sources, please be sure to sanitize file names to prevent potential command injections into the container.

### File naming and structure
Like other containers in the VirSieve Pipeline, this container is expected to run within a working folder.  Within that folder the expected input folder for this container is called **primerTrimBAM**.  Depending on the nature of the pipeline being run (especially if primer trim is not appropriate), you may need to use a different input folder, which can be passed via environment variable.  Please see below for environment variables relevant to this container.  As GATK is a sophisticated system with several different analytical steps, there will be multiple outputs and output folders from this process.  The key outputs will be the raw VCF files with an additional folder beside them containing the local reassembly BAM files carried out by mutect2 around mutations.  In addition to this, there will be a folder of VCF files that are filtered for potential orientation biases and other potential issues.  Finally, there will be a folder containing mutations that are analyzed for potentially being due to alignment artifacts.  This filter is very stringent (sometimes too stringent) and some valid mutation calls may not pass it (but these will still be visible in the final output).

### Running the container
To run this container (presumed to be named _virsievegatk_ here), simply use the following command:
```bash
docker container run --rm -v /path/to/working/folder:/data virsievegatk
```

### Setting non-default options
Some options can be set to non-default values by passing them into the container as environmental variables using the standard Docker commandline technique for setting environmental variables as follows:

| Variable        | Type           | Default  | Description |
| --------------- |:--------------:|:--------:|-------------|
WORKINGFOLDER | string | /data | Working folder name within the container
INPUTFOLDER | string | /$WORKINGFOLDER/primerTrimBAM | The name of the incoming sequence folder within the working folder
MARKDUPLICATES | boolean | FALSE | If a value is given here (usually just set it to 1), duplicates will be marked.  Identifying duplicates if using amplicon sequencing is generally not advised unless a UMI is somehow incorporated.
EXPECTEDVARIANTS | string | /$WORKINGFOLDER/$INPUTFOLDER/commonVariants.vcf | A VCF containing expected, common viral variants. If no file is found at this location, the container will default to its internal reference.
REFGENOME | string | /$WORKINGFOLDER/$INPUTFOLDER/reference.fa | Reference genome for the sample.  If no file is present, the internal default will be used.  If a file is provided, it should be prepared for GATK by indexing, dictionary genreation, and other processing required by GATK.
RESORTEDFOLDER | string | /$WORKINGFOLDER/resortBAM | Folder for storing the resorted BAM file.  Can be stored in an unmounted folder to have it disappear when the container is complete.
READGROUPEDFOLDER | string | /$WORKINGFOLDER/rgBAM | Folder for BAM files that have their readgroups added.  This is required for certain GATK functions.
DEDUPREADFOLDER | string | /$WORKINGFOLDER/dedupBAM | Folder for BAM files that have their duplicate reads marked.  This step may be skipped by leaving the MARKDUPLICATES environment variable as FALSE in which case this value is irrelevant.
BQSRREADFOLDER | string | /$WORKINGFOLDER/bqsrBAM | Folder for BAM files that have their base quality scores recalibrated.
RAWVCFFOLDER | string | /$WORKINGFOLDER/rawVCF | Folder for VCF files from mutect2 that have not been filtered.  This folder will also house the new BAM files generated during the local reassemblies around mutations.
FILTEREDVCFFOLDER | string | /$WORKINGFOLDER/filteredVCF | Folder for VCF files containing filtering details from orientation bias and other filters
ALIGNMENTARTIFACTFILTERFOLDER | string | /$WORKINGFOLDER/alignmentArtifactFilteredVCF | Folder for VCF files that have been filtered for variants caused by likely alignment artifacts
READGROUPSFILE | string | /$WORKINGFOLDER/rawBAM/readgroups.json | JSON formatted file describing the read groups to be assigned to each BAM file.  Container will use its best guess if no file is available.


## Contributing

We welcome and encourage contributions to this project from the microbiomics community and will happily accept and acknowledge input (and possibly provide some free kits as a thank you).  We aim to provide a positive and inclusive environment for contributors that is free of any harassment or excessively harsh criticism. Our Golden Rule: *Treat others as you would like to be treated*.

## Versioning

We use a modification of [Semantic Versioning](https://semvar.org) to identify our releases.

Release identifiers will be *major.minor.patch*

Major release: Newly required parameter or other change that is not entirely backwards compatible
Minor release: New optional parameter
Patch release: No changes to parameters

## Authors

- **Michael M. Weinstein** - *Project Lead, Programming and Design* - [michael-weinstein](https://github.com/michael-weinstein)


See also the list of [contributors](https://github.com/Zymo-Research/figaro/contributors) who participated in this project.

## License

This project is licensed under the GNU GPLv3 License - see the [LICENSE](LICENSE) file for details.
This license restricts the usage of this application for non-open sourced systems. Please contact the authors for questions related to relicensing of this software in non-open sourced systems.

## Acknowledgments

We would like to thank the following, without whom this would not have happened:
* The Python Foundation
* The staff at Zymo Research
* The scientific and public health COVID response community
* Our customers


