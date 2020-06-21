#!/usr/bin/env python3
import sys

sys.path.insert(0, '/home/')
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
    inchikeymiriam.deprecatedCID_cid = rpcache.getDeprecatedCID()
    inchikeymiriam.cid_strc = rpcache.getCIDstrc()
    inchikeymiriam.chebi_cid = rpcache.getChebiCID()
    inchikeymiriam.addInChiKey(gem_sbml, out_sbml)
