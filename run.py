#!/usr/bin/env python3
"""
Created on September 21 2019

@author: Melchior du Lac
@description: Extract the sink from an SBML into RP2 friendly format

"""
import argparse
import tempfile
import os
import logging
import shutil
import docker


def main(input_sbml, output_sbml):
    """Function to call the local docker to run the script

    :param input_sbml: Path to the input SBML file
    :param output_sbml: Path to the output SBML file

    :type input_sbml: str
    :type output_sbml: str

    :rtype: None
    :return: None
    """
    docker_client = docker.from_env()
    image_str = 'brsynth/inchikeymiriam-standalone'
    try:
        image = docker_client.images.get(image_str)
    except docker.errors.ImageNotFound:
        logging.warning('Could not find the image, trying to pull it')
        try:
            docker_client.images.pull(image_str)
            image = docker_client.images.get(image_str)
        except docker.errors.ImageNotFound:
            logging.error('Cannot pull image: '+str(image_str))
            exit(1)
    with tempfile.TemporaryDirectory() as tmpOutputFolder:
        if os.path.exists(input_sbml):
            shutil.copy(input_sbml, tmpOutputFolder+'/input_sbml.dat')
            command = ['/home/tool_inchikeyMIRIAM.py',
                       '-input_sbml',
                       '/home/tmp_output/input_sbml.dat',
                       '-output_sbml',
                       '/home/tmp_output/output_sbml.dat']
            container = docker_client.containers.run(image_str,
                                                     command, 
                                                     detach=True, 
                                                     stderr=True,
                                                     volumes={tmpOutputFolder+'/': {'bind': '/home/tmp_output', 'mode': 'rw'}})
            container.wait()
            err = container.logs(stdout=True, stderr=True)
            err_str = err.decode('utf-8')
            if 'ERROR' in err_str:
                print(err_str)
            elif 'WARNING' in err_str:
                print(err_str)
            if not os.path.exists(tmpOutputFolder+'/output_sbml.dat'):
                print('ERROR: Did not generate an output file')
            else:
                shutil.copy(tmpOutputFolder+'/output_sbml.dat', output_sbml)
            container.remove()
        else:
            logging.error('The input file cannot be found: '+str(input_sbml))
            exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Python wrapper to add InChIkey to MIRIAM annotations')
    parser.add_argument('-input_sbml', type=str)
    parser.add_argument('-output_sbml', type=str)
    params = parser.parse_args()
    main(params.input_sbml, params.output_sbml)
