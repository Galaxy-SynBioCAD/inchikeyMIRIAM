#!/usr/bin/env python3

import rpSBML
import libsbml
import logging


class inchikeyMIRIAM:
    def __init__(self):
        self.deprecatedCID_cid = {}
        self.chebi_cid = {}
        self.cid_strc = {}


    ## Function to create return the uniform compound ID
    #
    # @param cid String The identifier for a given compounf
    #
    def _checkCIDdeprecated(self, cid):
        try:
            return self.deprecatedCID_cid[cid]
        except KeyError:
            return cid


    def addInChiKey(self, gem_sbml, out_sbml):
        filename = gem_sbml.split('/')[-1].replace('.rpsbml', '').replace('.sbml', '').replace('.xml', '')
        logging.debug(filename)
        rpsbml = rpSBML.rpSBML(filename, path=gem_sbml)
        for spe in rpsbml.model.getListOfSpecies():
            inchikey = None
            miriam_dict = rpsbml.readMIRIAMAnnotation(spe.getAnnotation())
            if 'inchikey' in miriam_dict:
                self.logging.info('The species '+str(spe.id)+' already has an inchikey... skipping')
                continue
            try:
                for mnx in miriam_dict['metanetx']:
                    inchikey = self.cid_strc[self._checkCIDdeprecated(mnx)]['inchikey']
                    if inchikey:
                        rpsbml.addUpdateMIRIAM(spe, 'species', {'inchikey': [inchikey]})
                    else:
                        logging.warning('The inchikey is empty for: '+str(spe.id))
                    continue
            except KeyError:
                try:
                    for chebi in miriam_dict['chebi']:
                        inchikey = self.cid_strc[self._checkCIDdeprecated(self.chebi_cid[chebi])]['inchikey']
                        if inchikey:
                            rpsbml.addUpdateMIRIAM(spe, 'species', {'inchikey': [inchikey]})
                        else:
                            logging.warning('The inchikey is empty for: '+str(spe.id))
                        continue
                except KeyError:
                    logging.warning('Cannot find the inchikey for: '+str(spe.id))
        libsbml.writeSBMLToFile(rpsbml.document, out_sbml)
        return True
