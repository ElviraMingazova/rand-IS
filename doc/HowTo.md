# Random dataset generation instruction
## RM 0

1. Open the Terminal, change into the working directory of choice using  
`cd <path to directory>`  
2. Clone the git repository rand-IS using the following command:  
`git clone https://github.com/ElviraMingazova/rand-IS.git`
and change into the working directory  
`cd rand-IS/`
4. Type in `source bin/activate` to activate the virtual environment in that directory.
3. Create a generalized genome dimension file in the directory rand-IS/data/textfiles/ a textfile that contains two tab (or space) separated columns.
In the first column the names of the chromosomes in the format chr\__ (instead of __ is the number or X/Y in case of the human genome for example). You will find a couple of examples in the folder rand-IS/data/textfiles/.
        ___
        chr1	248956422  
        chr2	242193529  
        chr4	190214555  
        ...  
        chrY  57227415
        ___
The chromosome sizes can be downloaded from the database of the University of California, Santa Cruz (UCSC).
    - To do it manually tap this link http://hgdownload.cse.ucsc.edu/downloads.html, find the needed organism and search for the file chrom.sizes or chromInfo in one of the databases. You can also use directly the following link:  http://genome.ucsc.edu/cgi-bin/hgTracks?db=dm3&chromInfoPage=
    Just swap the db=xx for another genome.
    - Alternatively, you can use the tool fetchChromSizes, that is already in the rand-IS/bin repository.  
    Usage: `fetchChromSizes <db> > <db>.chrom.sizes`  
    This tool is used to fetch chrom.sizes information from UCSC for the given <db>.
    <db> - name of UCSC database, e.g.: hg38, hg18, mm9, etc ...  
    Example: `fetchChromSizes mm10 > ../data/textfiles/mm10.chrom.sizes.txt`  
    This data is available at the URL:
    `http://hgdownload.cse.ucsc.edu/goldenPath/<db>/bigZips/<db>.chrom.sizes`.  
    Don't forget to edit the downloaded file that there is only information described above and move it to the rand-IS/data/textfiles/ directory

4. To generate a random dataset of the IS type in the terminal:  
`python3 scripts/getRegionW2_weighted.py -n_ -r_ -d_ -i "data/textfiles/_.txt" -o "results/_.txt"`  
Instead of "_" you have to type in the correct value for the parameters.  
Explanation of the parameters:
  * n - Number of IS you want to generate
  * r - Range-value: defines an interval where the IS is located
  * d - Delta-value: expands the range with the value provided by user
  * i - Input-file .txt with names of chromosomes and their lengths in bp organized into two columns and separated by \t (tab or space)
  * o - Output-file where the random integration sites will be saved

## RM 1

**Dependencies**
- GEM library tools
- wig2bed from the Bedops package  


1. Choose and download the genome of choice in the fasta format into the rand-IS/data/genomes directory. Sometimes genomes are only available in twoBit format, then convert it to fasta using `twoBitToFa` tool. The genomes are available for download from here: http://hgdownload.cse.ucsc.edu/downloads.html.  
For example we will do it with the chrY sequence.  
`cd rand-IS/genomes`  
`wget http://hgdownload.cse.ucsc.edu/goldenPath/hg38/chromosomes/chrY.fa.gz`  
`gunzip chrY.fa.gz`
