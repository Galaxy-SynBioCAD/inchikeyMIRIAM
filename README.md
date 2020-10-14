# inchikeyMIRIAM

Project that uses the rpCache to parse an SBML file to find all the chemical species, and try to recover the inchikey and add it to the MIRIAM annotation.

## Getting Started

The docker needs to be built locally where the other dockers are to be built 

### Prerequisites

[rpCache](https://github.com/Galaxy-SynBioCAD/rpCache)
[rpSBML](https://github.com/Galaxy-SynBioCAD/rpBase)

### Installing

Build the docker image:

```
docker build -t brsynth/inchikeymiriam-standalone:v2 .
```

## Running the tests

TODO

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Galaxy](https://galaxyproject.org) - The Galaxy project

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

TODO

## Authors

* **Melchior du Lac** 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thomas Duigou
* Joan Hérisson
