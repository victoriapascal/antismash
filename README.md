gutSMASH - A new approach to functionally profile the human microbiome for specialized primary metabolic gene clusters
======================================================================================================================

Anaerobic bacteria in the gut are responsible for the synthesis and transformation of diverse molecules involved in host-microbe and microbe-microbe interactions, which ultimately mediate host phenotypes. The pathways for the production of these molecules belong to specialized primary metabolism and the genes encoding them are often physically clustered in the genome, in regions also known as metabolic gene clusters (MGCs).

gutSMASH is a tool that has been developed to systematically evaluate the metabolic potential of these bacteria by predicting both known and novel anaerobic MGCs from the gut microbiome. The gutSMASH detection rules have been validated using a curated dataset presented in our manuscript.

Altogether, this new software provides a comprehensive toolkit to functionally characterize anaerobic bacterial genomes by not only predicting MGCs of known functions but also novel MGCs that may represent good candidates for further experimental characterization.


Development & Funding
---------------------

The development of gutSMASH is a collaboration between the Bioinformatics Department at 
Wageningen University and Research and the Department of Bioengineering at Stanford University. This work has also been possible thanks to technical support provided by Novo Nordisk Foundation Center for Biosustainability.

How to install gutSMASH
-----------------------

To be able to run gutSMASH, different binaries have to be installed, by either using apt-get install:

```
sudo apt-get install -y hmmer2 hmmer diamond-aligner fasttree prodigal ncbi-blast+ muscle glimmerhmm
```

or Homebrew for macOS systems:

```
brew install hmmer2 hmmer diamond fasttree prodigal blast muscle brewsci/science/glimmerhmm
```

Assuming python3 is installated, the python3 dependencies can be installed using pip3 with the following command:

```
pip3 install biopython==1.76 helperlibs==0.1.9 bcbio-gff==0.6.6 pysvg-py3==0.2.2.post3 scikit-learn==0.22.1 matplotlib==3.2.1 pyscss==1.3.7 jinja2==2.11.1
```

gutSMASH uses various databases that you will have to download. The different databases are available from here: https://gutsmash.bioinformatics.nl/download.html.  After downloading, they need to be placed into the correct path as detailed on the download page.

How to run gutSMASH from the command line
-----------------------------------------

After downloading this gutSMASH git repository the user can run the tool from the command line. The ideal input for gutSMASH is an annotated nucleotide file in Genbank format or EMBL format. To run the most simple analysis (detection of MGCs only), the `--minimal` flag has to be included:

```
python3 gutsmash/run_gutsmash.py --minimal gbk_input_file
```

We highly encourage to compare the predicted gene clusters to a database of known and characterized gene clusters using the `--cb-knownclusters` flag. Also, gene cluster genes can be annotated into different functional categories by using the `-enable-genefunctions` option as follows:

```
python3 gutsmash/run_gutsmash.py --minimal --cb-knownclusters --enable-genefunctions gbk_input_file
```

Alternatively, gutSMASH can also use a FASTA file as input. Then, the user has to indicate a gene prediction tool of choice to annotate the genome using the `--genefinding-tool` option. For instance, this can be the `Prodigal` tool:

```
python3 gutsmash/run_gutsmash.py --genefinding-tool prodigal --cb-knownclusters --enable-genefunctions fasta_input_file
```

See other option available by typing:

```
python3 gutsmash/run_gutsmash.py --help
```

Publications
------------

See our [article](https://www.nature.com/articles/s41587-023-01675-1) for more information and to cite gutSMASH.

Users might also want to check the [gutSMASH webserver](https://gutsmash.bioinformatics.nl/) and the corresponding [article](https://academic.oup.com/nar/article/49/W1/W263/6279837)

License
-------

gutSMASH is an open source tool available under the GNU Affero General Public
License version 3.0 or greater. See the [`LICENSE.txt`](LICENSE.txt) file for
details.

Acknowledgements
----------------

Some icons used are courtesy of fontawesome.com
