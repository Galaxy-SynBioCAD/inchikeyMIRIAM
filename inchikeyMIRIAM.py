#!/usr/bin/env python3

import rpSBML
import libsbml
import logging
import rpCache

self.logger.basicConfig(
    #level=self.logger.DEBUG,
    #level=self.logger.WARNING,
    level=self.logger.ERROR,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
)


class inchikeyMIRIAM:
    """This class holds the cache information used by the scripts
    """
    def __init__(self):
        """Constructor for the inchikeyMIRIAM class
        """
        self.deprecatedCID_cid = {}
        self.chebi_cid = {}
        self.cid_strc = {}
        self.logger = logging.getLogger(__name__)


    def _checkCIDdeprecated(self, cid):
        """Function to create return the uniform compound ID

        :param cid: The compound id

        :type cid: str
    
        :rtype: str
        :return: A valid compound id
        """
        try:
            return self.deprecatedCID_cid[cid]
        except KeyError:
            return cid


    def addInChiKey(self, input_sbml, output_sbml):
        """Check the MIRIAM annotation for MetaNetX or CHEBI id's and try to recover the inchikey from cache and add it to MIRIAM

        :param input_sbml: SBML file input
        :param output_sbml: Output SBML file

        :type input_sbml: str
        :type output_sbml: str
    
        :rtype: bool
        :return: Success or failure of the function
        """
        filename = input_sbml.split('/')[-1].replace('.rpsbml', '').replace('.sbml', '').replace('.xml', '')
        self.logger.debug(filename)
        rpsbml = rpSBML.rpSBML(filename, path=input_sbml)
        for spe in rpsbml.model.getListOfSpecies():
            inchikey = None
            miriam_dict = rpsbml.readMIRIAMAnnotation(spe.getAnnotation())
            if 'inchikey' in miriam_dict:
                self.logger.info('The species '+str(spe.id)+' already has an inchikey... skipping')
                continue
            try:
                for mnx in miriam_dict['metanetx']:
                    inchikey = self.cid_strc[self._checkCIDdeprecated(mnx)]['inchikey']
                    if inchikey:
                        rpsbml.addUpdateMIRIAM(spe, 'species', {'inchikey': [inchikey]})
                    else:
                        self.logger.warning('The inchikey is empty for: '+str(spe.id))
                    continue
            except KeyError:
                try:
                    for chebi in miriam_dict['chebi']:
                        inchikey = self.cid_strc[self._checkCIDdeprecated(self.chebi_cid[chebi])]['inchikey']
                        if inchikey:
                            rpsbml.addUpdateMIRIAM(spe, 'species', {'inchikey': [inchikey]})
                        else:
                            self.logger.warning('The inchikey is empty for: '+str(spe.id))
                        continue
                except KeyError:
                    self.logger.warning('Cannot find the inchikey for: '+str(spe.id))
        libsbml.writeSBMLToFile(rpsbml.document, output_sbml)
        return True

def main(input_sbml, output_sbml):
    """Main function that creates a inchikeyMIRIAM object and runs it

    :param input_sbml: SBML file input
    :param output_sbml: Output SBML file

    :type input_sbml: str
    :type output_sbml: str

    :rtype: None
    :return: None
    """
    rpcache = rpCache.rpCache()
    inchikeymiriam = inchikeyMIRIAM()
    inchikeymiriam.deprecatedCID_cid = rpcache.getDeprecatedCID()
    inchikeymiriam.cid_strc = rpcache.getCIDstrc()
    inchikeymiriam.chebi_cid = rpcache.getChebiCID()
    inchikeymiriam.addInChiKey(input_sbml, output_sbml)

