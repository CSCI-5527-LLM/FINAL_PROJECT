# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 22:54:35 2023
Functions and scripts to extract descriptions of novel species and genera from
HTML files (IJSEM format)

@author: Lucas Zhang
"""

import pandas as pd
import re
import os
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

os.chdir('C:\\Users\\china\\Desktop\\Deep Learning\\Final Proj\\articles_flat')
files = os.listdir()
file_info = ["file_name", "file_size"]
mate_data = ["title", "year", "authors", "doi",
             "page1", "page2", "journal", "volumn", "issue"]

df_success_list = []
df_failure_list = []

# file = "70_7_1_014.html" # more recent format
# file = "71_12_2_001.html" # both gen. nov. and sp. nov.
# file = "65_12_4_019.html" # both gen. nov. and sp. nov.
# file = "53_1_1_001.html" #old-fashioned format, both gen. nov. and sp. nov.
# file = "67_10_5_013.html" # a very special document which is an erratum

# for meta data:
# fields required to be extracted from HTML files
# title, published year, authors, doi, file_size, pages, journal, volumn, issue
# descriptions of novel genera and species

# for descriptions:

# case 1, for more recent papers:
# <div class="clearer">&nbsp;</div></div><div xmlns:xs="http://www.w3.org/2001/XMLSchema" class="articleSection"><div class="articleSection"><div class="sectionDivider"><div class="tl-main-part title"><a name="s2" id="s2">Description of <span class="jp-italic">Bacteroides propionicigenes</span> sp. nov.</a></div><div class="menuButton">Go to section...</div><div class="clearer">&nbsp;</div></div><div class="dropDownMenu"><ul><li><a class="menuLink top-section-link" href="#top-1">TOP</a></li><li><a class="menuLink abstract-section-link" href="#abstract-1">ABSTRACT</a></li><li><a class="menuLink body-section-link" href="#S1-1">Abbreviations</a></li><li><a class="menuLink body-section-link" href="#s1">Full-Text</a></li><li><a class="menuLink body-section-link" href="#s2">Description of <span class="jp-italic">Bacteroides propionicigenes</span> sp. nov.</a></li><li><a class="menuLink ack-section-link" href="#ack1">Funding information</a></li><li><a class="menuLink ack-section-link" href="#ack2">Acknowledgements</a></li><li><a class="menuLink ack-section-link" href="#ack3">Author contributions</a></li><li><a class="menuLink ack-section-link" href="#ack4">Conflicts of interest</a></li><li><a class="menuLink ack-section-link" href="#ack5">Ethical statement</a></li><li><a class="menuLink ref-section-link" href="#references-1">References</a></li></ul></div></div><p><span class="jp-italic">Bacteroides propionicigenes</span> (pro.pi.o.ni.ci'ge.nes. N.L. neut. n. <span class="jp-italic">acidum propionicum</span>, propionic acid; Gr. suff. <span class="jp-italic">-genes</span>, producing; from Gr. v. <span class="jp-italic">gennaô</span>, to produce; N.L. part. adj. <span class="jp-italic">propionicigenes</span>, propionic acid producing).</p>
# <p>Cells are Gram-stain-negative, anaerobic, tolerant to oxygen, non-spore-forming, non-pigmented, non-motile rods, 0.9–1 µm wide and variable in length, mostly 1.7–7.5 µm. Colonies on mGAM agar are non-transparent, white, circular, swollen, neat-edged, with a smooth surface and about 0.5–1 mm in diameter. Growth occurs at temperatures ranging from 20 to 45 °C (optimal at 37 °C), pH levels ranging from pH 5.5 to 8.0 (optimal around pH 7) and with 0–2.5 % NaCl (w/v; optimal growth at 0 % NaCl). The major end products of glucose fermentation are acetic acid, propionic acid and isovaleric acid, while minor products are butyric acid, isobutyric acid and valeric acid. Indole is produced, with no urease activity. Nitrate cannot be reduced and catalase is negative. Strain NSJ-90<sup xmlns:f="http://www.example.org/functions">T</sup> is positive for <span class="jp-italic">β</span>-galactosidase, <span class="jp-italic">α</span>-glucosidase, <span class="jp-italic">α</span>-arabinosidase, phosphatase alkaline, leucyl glycine arylamidase, alanine arylamidase, glutamyl glutamic acid arylamidase, esterase, esterase lipase, acid phosphatase and naphthol-AS-BI-phosphohydrolase, while negative for arginine dihydrolase, <span class="jp-italic">α</span>-galactosidase, <span class="jp-italic">β</span>-galactosidase 6-phosphate, <span class="jp-italic">β-</span>glucosidase, <span class="jp-italic">β</span>-glucuronidase, <span class="jp-italic">N</span>-acetyl-<span class="jp-italic">β</span>-glucosaminidase, glutamic acid decarboxylase, <span class="jp-italic">α</span>-fucosidase, arginine arylamidase, proline arylamidase, phenylalanine arylamidase, leucine arylamidase, pyroglutamic acid arylamidase, tyrosine arylamidase, glycine arylamidase, histidine arylamidase, serine arylamidase, lipase, valine arylamidase, cystine arylamidase, trypsin and chymotrypsin. Acids are produced by fermenting glucose, lactose, sucrose, maltose, xylose, arabinose, mannose, raffinose and rhamnose, but not mannitol, salicin, glycerol, cellobiose, melezitose, sorbitol and trehalose. Utilizes substrates of <span class="jp-small">d</span>-fructose, trehalose, <span class="jp-small">d</span>-galactose, <span class="jp-small">d</span>-galacturonic acid, gentiobiose, <span class="jp-small">d</span>-mannitol, melibiose, palatinose, turanose, <span class="jp-italic">α</span>-ketobutyric acid, pyruvic acid and succinic acid. Utilizes starch, xylan, hyaluronic acid and chondroitin sulphate dextrose. The polar lipids include diphosphatidylglycerol, phosphatidylglycerol, phosphatidylethanolamine, three phospholipids and an unknown polar lipid. The major fatty acids (&gt;10 %) are iso-C<span class="jp-sub">15 : 0</span>, anteiso-C<span class="jp-sub">15 : 0</span> and iso-C<span class="jp-sub">17 : 0</span> 3-OH. Menaquinone-10 is the major respiratory quinone.</p>
# <p>The genomic DNA G+C content is 44.85 mol%. The type strain, NSJ-90<sup xmlns:f="http://www.example.org/functions">T</sup> (=CGMCC 1.17886<sup xmlns:f="http://www.example.org/functions">T</sup> =KCTC 25305<sup xmlns:f="http://www.example.org/functions">T</sup>), was isolated from the faeces of a healthy adult human.</p>
# <div class="clearer">&nbsp;</div></div>
# </div>

# case 2, for papers published earlier:
# <div>
# <span class="tl-lowest-section">Description of <span class="jp-italic">Marinithermus hydrothermalis</span> sp. nov.</span>
# <p><span class="jp-italic">Marinithermus hydrothermalis</span> (hy.dro.ther.ma′lis. N.L. masc. adj. <span class="jp-italic">hydrothermalis</span> pertaining to a hydrothermal vent).</p>
# <p>Cells are Gram-negative, non-motile, straight rods, 7·5–9·4×0·9–1·0 μm, that occur in pairs or are filamentous under optimal conditions. Colonies are whitish and 2·5–3·0 mm in diameter. Aerobic, thermophilic, neutrophilic heterotroph. Growth occurs at temperatures of 50·0–72·5 °C (optimum 67·5 °C), at pH 6·25–7·75 (optimum pH 7·0) and in the presence of 0·5–4·5 % NaCl (optimum 3 % NaCl). Generation time under optimal conditions is about 30 min. Cytochrome oxidase- and catalase-negative. The major cellular fatty acid components are iso-C<span class="jp-sub">15 : 0</span> (40·4 %), iso-C<span class="jp-sub">17 : 0</span> (28·5 %), C<span class="jp-sub">16 : 0</span> (12·9 %), anteiso-C<span class="jp-sub">15 : 0</span> (6·0 %), anteiso-C<span class="jp-sub">17 : 0</span> (5·4 %), iso-C<span class="jp-sub">16 : 0</span> (2·8 %) and iso 3-OH C<span class="jp-sub">11 : 0</span> (1·0 %). The major quinone is menaquinone-8. Growth occurs on complex organic substrates such as yeast extract and tryptone peptone. The DNA base composition of the type strain, strain T1<sup xmlns:f="http://www.example.org/functions">T</sup> (=JCM 11576<sup xmlns:f="http://www.example.org/functions">T</sup> =DSM 14884<sup xmlns:f="http://www.example.org/functions">T</sup>), is 68·6 mol%. Isolated from a deep-sea hydrothermal vent chimney at Suiyo Seamount in the Izu-Bonin Arc, Japan (28°34·287′N, 140°38·663′E; depth 1385 m).</p>
# </div></div>

# case 3, not a appropriate HTML file:
# Some produced an error:
# not enough length

iiii = 0
for file in files:
    if iiii % 100 == 0:
        print(".", end="", flush=True)
    iiii += 1
    try:
        ###############################################
        # file information and soup
        ###############################################
        #num_1, num_2, num_3, num_4 = re.split("_", re.sub("\.html$", "", file))
        file_size = os.path.getsize(file)
        with open(file, 'r', encoding='utf-8') as fp: # parse the HTML 
            soup = BeautifulSoup(fp, "lxml") # this is indeed an HTML parser
        ###############################################
        # article meta data
        ###############################################
        # <meta name="citation_title" content="Erratum: Mesonia maritimus sp. nov., 
        #isolated from seawater of the South Sea of Korea">
        title = soup.find_all("meta", {"name": "citation_title"})
        if len(title) == 1:
            title = title[0]["content"]
        else:
            title = "" 
        #<meta name="citation_year" content="2017">
        year = soup.find_all("meta", {"name": "citation_year"})
        if len(year) == 1:
            year = year[0]["content"]
        else:
            year = "" 
        # <meta name="dc.creator" content="Hye-Ri Sung">
        # creators = soup.find_all('meta', {'name': 'dc.creator'})
        authors = soup.find_all('meta', {'name': 'citation_author'})
        authors = [auth['content'] for auth in authors]
        authors = '||'.join(authors)
        # <meta name="citation_doi" content="10.1099/ijsem.0.002361">
        doi = soup.find_all('meta', {'name': 'citation_doi'})
        if len(doi) == 1:
            doi = doi[0]["content"]
        else:
            doi = "" 
        # <meta name="citation_firstpage" content="4285">
        page1 = soup.find_all('meta', {'name': 'citation_firstpage'})
        if len(page1) == 1:
            page1 = page1[0]["content"]
        else:
            page1 = ""        
        # <meta name="citation_lastpage" content="4286">
        page2 = soup.find_all('meta', {'name': 'citation_lastpage'})
        if len(page2) == 1:
            page2 = page2[0]["content"]
        elif len(page2) == 0:
            page2 = ""
        # <meta name="citation_journal_title" content="International Journal 
        #of Systematic and Evolutionary Microbiology">
        journal = soup.find_all("meta", {"name": "citation_journal_title"})
        if len(journal) == 1:
            journal = journal[0]["content"]
        elif len(journal) == 0:
            journal = ""
        #<meta name="citation_volume" content="67">
        volumn = soup.find_all("meta", {"name": "citation_volume"})
        if len(volumn) == 1:
            volumn = volumn[0]["content"]
        elif len(volumn) == 0:
            volumn = ""
        #<meta name="citation_issue" content="10">
        issue = soup.find_all("meta", {"name": "citation_issue"})
        if len(issue) == 1:
            issue = issue[0]["content"]
        elif len(issue) == 0:
            issue = ""
        ###############################################
        # extract descriptions, format 1, descriptions as article sections (more recent)
        ###############################################
        # html_content = """
        # <div class="clearer">&nbsp;</div></div><div xmlns:xs="http://www.w3.org/2001/XMLSchema" class="articleSection"><div class="articleSection"><div class="sectionDivider"><div class="tl-main-part title"><a name="s7" id="s7">Description of <span class="jp-italic">Mesonia oceanica</span> sp. nov.</a></div><div class="menuButton">Go to section...</div><div class="clearer">&nbsp;</div></div><div class="dropDownMenu"><ul><li><a class="menuLink top-section-link" href="#top-1">TOP</a></li><li><a class="menuLink abstract-section-link" href="#abstract-1">ABSTRACT</a></li><li><a class="menuLink body-section-link" href="#S1-1">Abbreviations</a></li><li><a class="menuLink body-section-link" href="#s1">Full-Text</a></li><li><a class="menuLink body-section-link" href="#s2">Isolation</a></li><li><a class="menuLink body-section-link" href="#s3">16S RNA phylogeny</a></li><li><a class="menuLink body-section-link" href="#s4">Genome features</a></li><li><a class="menuLink body-section-link" href="#s5">Ecology</a></li><li><a class="menuLink body-section-link" href="#s6">Physiology and chemotaxonomy</a></li><li><a class="menuLink body-section-link" href="#s7">Description of <span class="jp-italic">Mesonia oceanica</span> sp. nov.</a></li><li><a class="menuLink ack-section-link" href="#ack1">Funding information</a></li><li><a class="menuLink ack-section-link" href="#ack2">Acknowledgements</a></li><li><a class="menuLink ack-section-link" href="#ack3">Author contributions</a></li><li><a class="menuLink ack-section-link" href="#ack4">Conflicts of interest</a></li><li><a class="menuLink ref-section-link" href="#references-1">References</a></li></ul></div></div><p>
        # <span class="jp-italic">Mesonia oceanica</span> (o.ce.a’ni.ca, N.L. fem. adj. <span class="jp-italic">oceanica</span>, of or pertaining to the ocean).</p>
        # <p>Cells are Gram-reaction-negative, rod-shaped, 0.5–0.6 µm×0.9–1.5 µm and non-motile. Strictly aerobic and chemoorganotrophic; positive for catalase and oxidase. Colonies in Marine Agar medium are regular and yellow pigmented. Flexirubin-type pigments are not produced. Mesophilic, neutrophilic and slightly halophilic, with optima at: 26 °C (range: 4–30 °C; 40 °C negative), pH6–8 (range: 5–8; pH 4 negative; pH 9 and 10, weak) and 2–4 % total salinity (range: 1–15 %; 0.5 and 18 % negative). Requires sodium ions for growth. Nitrate is not reduced to nitrite or N<span class="jp-sub">2</span>. Hydrolyses aesculin, casein, gelatin, Tween 80 (weakly) and DNA (weakly), but not alginate, cellulose (as filter paper) or agar. Indole production from tryptophan, arginine dihydrolase and urease are negative. PNPG test (β-galactosidase) is positive in API 20NE. Assimilates malate, as well as glucose, mannose, maltose, arabinose, mannitol, <span class="jp-italic">N</span>-acetyl <span class="jp-small">d</span>-glucosamine, gluconate and adipate, but not caprate or citrate, on API 20NE. The type strain was unable to grow in minimal medium (Basal Medium) with any of 52 sole carbon and energy sources but grew with yeast extract. The following carbohydrates are metabolised with weak acid production in aerobic API 50CH/E tubes: <span class="jp-small">d</span>-glucose, <span class="jp-small">d</span>-mannose, amygdalin, salicin, cellobiose and maltose. Enzymatic activities displayed on API ZYM are alkaline and acid phosphatases, leucine and valine arylamidases and α- and β-glucosidases. Naphthol-AS-BI-phosphohydrolase, estearase and estearase lipase are weakly positive; lipase, cystine arylamidase, trypsin, α-chymotrypsin, α-galactosidase, β-galactosidase, β-glucuronidase, <span class="jp-italic">N</span>-acetyl-β-glucosaminidase, α-mannosidase and α-fucosidase are negative. Major polar lipids are phosphatidylethanolamine (PE), two unidentified glycolipids, three unidentified aminolipids and three unidentified lipids. Major respiratory quinone is MK6. Major cellular fatty acids include iso-C<span class="jp-sub">15 : 0</span>, iso-C<span class="jp-sub">15 : 0</span> 2-OH [although reported as summed feature 3 (C<span class="jp-sub">16 : 1</span> ω7<span class="jp-italic">c</span>/ω6<span class="jp-italic">c</span>)] and iso-C<span class="jp-sub">17 : 0</span> 3-OH.</p>
        # <p>The type strain is ISS653<sup xmlns:f="http://www.example.org/functions">T</sup> (=CECT 9532<sup xmlns:f="http://www.example.org/functions">T</sup>=LMG 31236<sup xmlns:f="http://www.example.org/functions">T</sup>), which was isolated from surface seawater of the Atlantic Ocean during the <span class="jp-italic">Tara</span> oceans expedition. Strain ISS1889 (=CECT 30008) is an additional strain of the species. The DNA G+C content of the type strain is 34.9 mol% and its genome size is 4.28 Mbp. The GenBank/EMBL/DDBJ accession numbers for the whole genome sequence and 16S rRNA gene sequence of strain ISS653<sup xmlns:f="http://www.example.org/functions">T</sup> are CABVMM01 and MH732189, respectively.</p>
        # <div class="clearer">&nbsp;</div></div>
        # """
        # soup = BeautifulSoup(html_content, "lxml")
        section_tags = soup.find_all('a', {'name': re.compile(r's\d+(-\d+)?'), 
                                           'id': re.compile(r's\d+(-\d+)?')})
        flag = False
        for section_tag in section_tags:
            if fuzz.partial_ratio('description of', section_tag.text.lower()) > 90:
                format_type = 1
                description = ""
                flag = True
                
                description += (section_tag.text.strip() + "\n")
                parent_tag = section_tag.parent.parent.parent
                assert parent_tag["class"][0] == "articleSection", \
                    "case 1, the tag format is wrong in that this is not an articleSection"
                for paragraph_tag in parent_tag.nextSiblingGenerator():
                    if paragraph_tag.name and paragraph_tag.name == "div" and paragraph_tag["class"][0] == "clearer":
                        break # until the next "clearer"
                    else:
                        description += (paragraph_tag.text.strip() + "\n")
                        
                # added to the df_success_list
                # file_info = ["file_name", "file_size"]
                # mate_data = ["title", "year", "authors", "doi",
                #              "page1", "page2", "journal", "volumn", "issue"]
                df_success_list.append(pd.DataFrame(
                    [[file, file_size, title, year, authors, doi, page1, page2,
                      journal, volumn, issue, format_type, description]],
                    columns = file_info + mate_data + ["format_type", "description"]))

        if flag:
            continue # next file
        
        ###############################################
        # extract descriptions, format 2, descriptions as subtitles in discussion (old-fashioned)
        ###############################################
        # html_content = """
        # <div>
        # <span class="tl-lowest-section">Enrichment and purification</span>
        # <p>Enrichment cultures...</p>
        # </div>
        # <div>
        # <span class="tl-lowest-section">Fatty acid, quinone and DNA base composition</span>
        # <p>When the isolate was grown at 67·5 °C, the major cellular fatty acids were iso-C<span class="jp-sub">15 : 0</span> (40·4 %), iso-C<span class="jp-sub">17 : 0</span> (28·5 %), C<span class="jp-sub">16 : 0</span> (12·9 %), anteiso-C<span class="jp-sub">15 : 0</span> (6·0 %), anteiso-C<span class="jp-sub">17 : 0</span> (5·4 %), iso-C<span class="jp-sub">16 : 0</span> (2·8 %) and iso 3-OH C<span class="jp-sub">11 : 0</span> (1·0 %). Menaquinone-8 was the major respiratory quinone. This fatty acid and respiratory quinone composition was similar to those of members of the genus <span class="jp-italic">Thermus</span>, as described previously (<span class="xref"><a href="#R15" data-original-title="" title="">Hensel <span class="jp-italic">et al.</span>, 1986</a></span>; <span class="xref"><a href="#R35" data-original-title="" title="">Prado <span class="jp-italic">et al.</span>, 1988</a></span>). However, the presence of iso 3-OH C<span class="jp-sub">11 : 0</span> in the fatty acid composition of the isolate distinguished it from <span class="jp-italic">Thermus</span> species.</p>
        # <p>The G+C content of the genomic DNA of strain T1<sup xmlns:f="http://www.example.org/functions">T</sup> was 68·6 mol%. This value is very similar to those of members of the genus <span class="jp-italic">Thermus</span> (<span class="xref"><a href="#R10" data-original-title="" title="">Duffield &amp; Cossar, 1995</a></span>).</p>
        # </div>
        # <div>
        # <span class="tl-lowest-section">Description of <span class="jp-italic">Marinithermus</span> gen. nov.</span>
        # <p><span class="jp-italic">Marinithermus</span> (ma.ri.ni.ther′mus. L. adj. <span class="jp-italic">marinus</span> of the sea; Gr. adj. <span class="jp-italic">thermos</span> hot; N.L. n. <span class="jp-italic">Marinithermus</span> an organism living in marine hot places).</p>
        # <p>Rod-shaped bacterium, Gram-negative, with branched chain fatty acids and menaquinone-8. Thermophilic. Growth suited to the pH and salinity of sea water; able to grow at 55–70 °C, pH 6·2–7·7 and 1·0–4·5 % NaCl. Aerobic, heterotrophic, able to utilize organic complex substrates, amino acids, carboxylic acids and sugars. The G+C content is approximately 68 mol%. 16S rDNA sequence comparison locates <span class="jp-italic">Marinithermus</span> in a novel lineage deeply branched prior to the divergence of the genus <span class="jp-italic">Thermus</span>. The type species is <span class="jp-italic">Marinithermus hydrothermalis</span>.</p>
        # </div>
        # """
        # soup = BeautifulSoup(html_content, "lxml")
        section_tags = soup.find_all('span', {'class': "tl-lowest-section"})
        
        flag = False
        for section_tag in section_tags:
            if fuzz.partial_ratio('description of', section_tag.text.lower()) > 90:
                format_type = 2
                description = ""
                flag = True
                
                parent_tag = section_tag.parent
                assert parent_tag.name == "div", \
                    "case 2, the tag format is wrong in that this is not a div"
                description += (parent_tag.text.strip()) # all the content in the <div>

                # added to the df_success_list
                # file_info = ["file_name", "file_size"]
                # mate_data = ["title", "year", "authors", "doi",
                #              "page1", "page2", "journal", "volumn", "issue"]
                df_success_list.append(pd.DataFrame(
                    [[file, file_size, title, year, authors, doi, page1, page2,
                      journal, volumn, issue, format_type, description]],
                    columns = file_info + mate_data + ["format_type", "description"]))

        if flag:
            continue # next file
            
        ###############################################
        # no descriptions
        ###############################################
        assert flag, "no description found!"
        
    except Exception as e:
        # export this file to another pandas dataframe
        # file_info = ["file_name", "file_size"]
        # mate_data = ["title", "year", "authors", "doi",
        #              "page1", "page2", "journal", "volumn", "issue"]
        df_failure_list.append(pd.DataFrame(
            [[file, file_size, title, year, authors, doi, page1, page2,
              journal, volumn, issue, str(e)]], 
            columns = file_info + mate_data + ["error_msg"]))

df_failure = pd.concat(df_failure_list, ignore_index=True)
df_success = pd.concat(df_success_list, ignore_index=True)
df_success.to_csv("df_success.csv", index=False, encoding='utf-8')
df_failure.to_csv("df_failure.csv", index=False, encoding='utf-8')









