'''
Created on Dec 7, 2020

@author: braistedjc
'''
import sys, os
from rampEntity.Molecule import Molecule
from MetabolomicsData import MetabolomicsData
import zipfile
import gzip
import shutil
import re

from ftplib import FTP

class ChemWrangler(object):
    '''
    The ChemWrangler class has production and utility methods for working with molecular information
    associated with RaMP Metabolites.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.chemLibDict = dict()


    """
    Fetch compound properties
    """    
    def fetchCompoundPropertiesFiles(self):
        
        print(os.getcwd())
        
        metData = MetabolomicsData()
        dir = "../../misc/data/chemprops/"
        url = "https://hmdb.ca/system/downloads/current/structures.zip"
        remoteFile = "structures.zip"
                
        metData.download_files(url, dir+remoteFile)
        
        
        with zipfile.ZipFile(dir+remoteFile,"r") as zip_ref:
            zip_ref.extractall(dir)
                 
        dir = "../../misc/data/chemprops/"
        url = "ftp://ftp.ebi.ac.uk/pub/databases/chebi/SDF/ChEBI_complete.sdf.gz"
        remoteFile = "ChEBI_complete.sdf.gz"
        extractFile = "ChEBI_complete.sdf"
                 
        metData.download_files(url, dir+remoteFile)
        
        with gzip.open(dir+remoteFile, 'rb') as f_in:
            with open(dir+extractFile, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        
    def readHMDBSDF(self, source, filePath):
        """
        Utility method to read HMDB SDF file for specific data types to populate Molecule objects.
        """
        i = 0
        sdfDB = open(filePath, 'r+', encoding="utf-8")
        molDict = dict()
        
        mol = Molecule()
        mol.source = source
            
        while True:
            line = sdfDB.readline()

            if len(line) == 0:
                print("line is none...")
                break
            
            line = line.strip()            
            if line == '$$$$':
                i = i + 1
               # print("processing structure " + str(i))
                molDict[mol.id] = mol
                mol = Molecule()
                mol.source = source
            if line == '> <DATABASE_ID>':
                mol.id = "hmdb:" + sdfDB.readline().strip()
            if line == '> <SMILES>':
                mol.smiles = sdfDB.readline().strip()
            if line == '> <INCHI_KEY>':
                mol.inchiKey = sdfDB.readline().strip()
                mol.inchiKeyPrefix = mol.inchiKey.split("-")[0]                
            if line == '> <INCHI_IDENTIFIER>':
                mol.inchi = sdfDB.readline().strip()                                          
            if line == '> <MOLECULAR_WEIGHT>':
                mol.mw = sdfDB.readline().strip()
            if line == '> <EXACT_MASS>':
                mol.monoisotopicMass = sdfDB.readline().strip()
            if line == '> <GENERIC_NAME>':
                mol.name = sdfDB.readline().strip()
            if line == '> <FORMULA>':
                mol.formula = sdfDB.readline().strip()

        self.chemLibDict[source] = molDict
       
        
    def readChebiSDF(self, source, filePath):
        """
        Utility method to read Chebi SDF file for specific data types to populate Molecule objects.
        """        
        print(sys.getdefaultencoding())
        print("ChEBI SDF")

        i = 0
        sdfDB = open(filePath, 'r+', encoding="utf-8")
        molDict = dict()
        mol = Molecule()
        mol.source = source
        
        while True:
            line = sdfDB.readline()

            if len(line) == 0:
                print("line is none...")
                break

            line = line.strip()            
            if line == '$$$$':
                i = i + 1
               # print("processing structure " + str(i))
                molDict[mol.id] = mol
                mol = Molecule()
                mol.source = source
            if line == '> <ChEBI ID>':
                mol.id = sdfDB.readline().strip()
                mol.id = mol.id.replace("CHEBI", "chebi")
            if line == '> <SMILES>':
                mol.smiles = sdfDB.readline().strip()
            if line == '> <InChIKey>':
                mol.inchiKey = sdfDB.readline().strip()
                mol.inchiKeyPrefix = mol.inchiKey.split("-")[0]                
            if line == '> <InChI>':
                mol.inchi = sdfDB.readline().strip()                                      
            if line == '> <MASS>':
                mol.mw = sdfDB.readline().strip()
            if line == '> <Monoisotopic Mass>':
                mol.monoisotopicMass = sdfDB.readline().strip()
            if line == '> <ChEBI Name>':
                mol.name = sdfDB.readline().strip()
            if line == '> <Formulae>':
                mol.formula = sdfDB.readline().strip()

        self.chemLibDict[source] = molDict


    def readKEGGCompound(self, source, filePath):
        """
        Utility method to read KEGG 2021 Compound file for specific data types to populate Molecule objects.
        """
        i = 0
        sdfDB = open(filePath, 'r+', encoding="utf-8")
        molDict = dict()
        mol = Molecule()
        mol.source = source
            
        linekey = ""
        while True:
            line = sdfDB.readline()

            lineToks = re.split("\s{1,}", line)
            if(len(lineToks) > 1):
                linekey = lineToks[0]
                # print(linekey + ".... linekey")

            if len(line) == 0:
                print("line is none...")
                break

            line = line.strip()            
            if line == '///':
                i = i + 1
                # print("processing structure " + str(i))
                molDict[mol.id] = mol
                mol = Molecule()
                mol.source = source
            if linekey == 'ENTRY':
                mol.id = "kegg:"+lineToks[1].strip()                           
            if linekey == 'MOL_WEIGHT':
                mol.mw = lineToks[1].strip()
            if linekey == 'EXACT_MASS':
                mol.monoisotopicMass = lineToks[1].strip()
            if linekey == 'NAME':
                mol.name = lineToks[1].strip()
                mol.name = mol.name[:-1]
            if linekey == 'FORMULA':
                mol.formula = lineToks[1].strip()

        # add to to full dictionary
        self.chemLibDict[source] = molDict


    def readLipidMapsSDF(self, source, filePath):
        """
        Utility method to read Chebi SDF file for specific data types to populate Molecule objects.
        """        
        print(sys.getdefaultencoding())
        print("Lipidmaps SDF")

        i = 0
        sdfDB = open(filePath, 'r+', encoding="utf-8")
        molDict = dict()
        mol = Molecule()
        mol.source = source
        
        while True:
            line = sdfDB.readline()

            if len(line) == 0:
                print("line is none...")
                break

            line = line.strip()            
            if line == '$$$$':
                i = i + 1
               # print("processing structure " + str(i))
                molDict[mol.id] = mol
                mol = Molecule()
                mol.source = source
            if line == '> <LM_ID>':
                mol.id = sdfDB.readline().strip()
                mol.id = "LIPIDMAPS:" + mol.id 
            if line == '> <SMILES>':
                mol.smiles = sdfDB.readline().strip()
            if line == '> <INCHI_KEY>':
                mol.inchiKey = sdfDB.readline().strip()
                mol.inchiKeyPrefix = mol.inchiKey.split("-")[0]                
            if line == '> <INCHI>':
                mol.inchi = sdfDB.readline().strip()                                      
            if line == '> <MASS>':
                mol.mw = sdfDB.readline().strip()
            if line == '> <EXACT_MASS>':
                mol.monoisotopicMass = sdfDB.readline().strip()
            if line == '> <NAME>':
                mol.name = sdfDB.readline().strip()
            if line == '> <FORMULA>':
                mol.formula = sdfDB.readline().strip()

        self.chemLibDict[source] = molDict
        print("Finished Lipidmaps chemprops: size="+str(len(molDict)))

            
    def readPubchemTabIdMiInchikey(self, source, file):
        """
        Utility method to read a small subset of pubchem to evaluate harmonization
        This includes pubchem id, inchikey, monoisotopic mass and formula (12/2021)
        """
        sdfDB = open(file, 'r+', encoding="utf-8")
        
        molDict = dict()
        mol = Molecule()
        mol.source = source
        
        while True:
            line = sdfDB.readline()

            if line is None or len(line) == 0:
                break
            
            mol = Molecule()
            mol.source = source
        
            lineToks = line.split("\t")
            mol.id = lineToks[0].strip()
            mol.monoisotopicMass = lineToks[1].strip()
            mol.inchiKey = lineToks[2].strip()
            mol.inchiKeyPrefix = mol.inchiKey.split("-")[0]
        
            molDict[mol.id] = mol
            
        sdfDB.close()
        
        self.chemLibDict[source] = molDict



    def readSDF(self, source, file):
        """
        Reads SDF for specified data source and file
        """
        if source == 'hmdb':
            self.readHMDBSDF(source, file)
        if source == 'chebi':
            self.readChebiSDF(source, file)
        if source == 'kegg':
            self.readKEGGCompound(source, file)
        if source == 'pubchem':
            self.readPubchemTabIdMiInchikey(source, file)
        if source == 'lipidmaps':
            self.readLipidMapsSDF(source, file)          
            

    def loadRampChemRecords(self, sources):
        """
        Populates the chemical record list for the list of passed sources.
        """
        for source in sources:
            if source == 'hmdb':
                file = "../../misc/data/chemprops/structures.sdf"
                self.readSDF('hmdb', file)
            if source == 'chebi':
                file = "../../misc/data/chemprops/ChEBI_complete.sdf"
                self.readSDF('chebi', file)
            if source == 'kegg':
                file = "../../misc/data/chemprops/kegg_compound"
                self.readSDF('kegg', file)
            if source == 'pubchem':
                file = "../../misc/data/chemprops/pubchem_id_mi_inchikey_issue_set.txt"
                self.readSDF('pubchem', file) 
            if source == 'lipidmaps':
                file = "../../misc/data/chemprops/lipid_maps/structures.sdf" 
                self.readSDF("lipidmaps", file)      
           
           
         
    def getChemSourceRecords(self):
        """
        Returns the chemical library dictionary. Molecule objects associated with input data sources.
        """
        return self.chemLibDict
       

                               
    def evaluateMolecularCollisions(self, source):
        '''
        This is a utility method developed to report on constituative isomers
        This simply reviews compuonds from a source, collecting inchikey prefixes that map to compound formula keys.
        The constructed has will have formula keys and a collection of inchikey prefixes. 
        A second hash holds collections of source ids for each formula.
        A file is output that reports on each distinct formula that has a least one pair of isomers.
        '''        
        sources = list()
        sources.append(source)
        self.loadRampChemRecords(sources)
        
        # two ways to evaluate Mi collisions
        # first look for the same formula, different inchi prefix
        # these are the constituent isomers
        
        # build has hash of formula to a list of inchi prefixes
        chemList = list()
        formulaToInchiPrefixListDict = dict()
        formulaToIdDict = dict()
        distinctInchiPrefixList = list()

        currList = None
                
        chemList = self.chemLibDict[source]
        compCount = 0
        for key in chemList:
            mol = chemList.get(key)
            compCount = compCount + 1
            if mol.inchiKeyPrefix is not None and mol.formula is not None:
                
                if(compCount % 10000 == 0):
                    print(mol.formula)
                    
                currList = formulaToInchiPrefixListDict.get(mol.formula, None)
                if currList is not None:
                    if mol.inchiKeyPrefix not in currList:
                        currList.append(mol.inchiKeyPrefix)
                        if mol.inchiKeyPrefix not in distinctInchiPrefixList:
                            distinctInchiPrefixList.append(mol.inchiKeyPrefix)
                else:
                    currList = list()
                    currList.append(mol.inchiKeyPrefix)
                    formulaToInchiPrefixListDict[mol.formula] = currList
            
            currList = formulaToIdDict.get(mol.formula, None)
            if currList is not None:
                if mol.id not in currList:
                    currList.append(mol.id)
            else:
                currList = list()
                currList.append(mol.id)
                formulaToIdDict[mol.formula] = currList
                                      
        file  = open("../../misc/data/chemprops/constituativeIsomerList.txt", "w+", encoding='utf-8')
         
        for key in formulaToInchiPrefixListDict:
            if len(formulaToInchiPrefixListDict[key]) > 1:
                s = key + "\t" + str(len(formulaToInchiPrefixListDict[key])) + "\t" 
                for inchiPre in formulaToInchiPrefixListDict[key]:
                    s = s + inchiPre + ", "
                s = s[:-2]
                s = s + "\t"
                for id in formulaToIdDict[key]:
                    s = s + id + ", "
                s = s[:-2]
                s = s + "\n"
                file.write(s)
          
        file.close()


    def testDownloadKeggFile(self):
        ftpUrl = "ftp.kegg.net"
        user = "BJ2383"
        pw = "Nc@tskegg2**"
        remPath = "kegg/ligand"
        file = "README.ligand"
        localPath = "C:/Tools/"
        
        ftp = FTP(ftpUrl)
        ftp.login(user,pw)
        ftp.cwd(remPath)
        with open(localPath+file, 'wb') as testReadme:
            ftp.retrbinary("RETR "+file, testReadme.write)
        ftp.quit()
        testReadme.close()
            
        
cw = ChemWrangler()
cw.loadRampChemRecords(["hmdb","chebi","lipidmaps"])
        