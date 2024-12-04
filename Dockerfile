FROM broadinstitute/gatk:4.6.1.0

RUN apt update
RUN apt install -y bedops

RUN useradd -ms /bin/bash gatk

WORKDIR /home/gatk

COPY ./references /home/gatk/references

RUN gzip -d /home/gatk/references/Sars_cov_2.ASM985889v3.dna_sm.toplevel.fa.gz
RUN gatk BwaMemIndexImageCreator --input /home/gatk/references/Sars_cov_2.ASM985889v3.dna_sm.toplevel.fa --output /home/gatk/references/Sars_cov_2.ASM985889v3.dna_sm.toplevel.fa.img
RUN bgzip /home/gatk/references/Sars_cov_2.ASM985889v3.dna_sm.toplevel.fa
RUN samtools faidx /home/gatk/references/Sars_cov_2.ASM985889v3.dna_sm.toplevel.fa.gz
RUN gatk CreateSequenceDictionary -R /home/gatk/references/Sars_cov_2.ASM985889v3.dna_sm.toplevel.fa.gz
RUN gatk IndexFeatureFile --input /home/gatk/references/common_SARS-CoV-2_mutations.vcf
RUN vcf2bed < /home/gatk/references/problematic_sites_sarsCov2.vcf > /home/gatk/references/problematic_sites_sarsCov2.bed

COPY ./gatkSupport /home/gatk/gatkSupport

COPY ./*.py /home/gatk

#RUN chown -R gatk /home/gatk

#USER gatk

ENV PYTHONUNBUFFERED=1

CMD python3 /home/gatk/main.py