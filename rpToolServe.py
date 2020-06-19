#!/usr/bin/env python3

import rpTool
import logging
import rpCache

logging.basicConfig(
    level=logging.DEBUG,
    #level=logging.WARNING,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
)

def main(gem_sbml,
         out_sbml):
    rpcache = rpCache.rpCache()
    inchikeymiriam = rpTool.inchikeyMIRIAM()
    inchikeymiriam.deprecatedCID_cid = rpcache.deprecatedCID_cid
    inchikeymiriam.cid_strc = rpcache.cid_strc
    inchikeymiriam.chebi_cid = rpcache.chebi_cid
    inchikeymiriam.addInChiKey(gem_sbml, out_sbml)
