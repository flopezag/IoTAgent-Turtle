# IoTAgent-Turtle
IoT Agent for the RDF Turtle 1.1 for statistical data representation

<div id="top"></div>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Apache2.0 License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/flopezag/IoTAgent-Turtle">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">project_title</h3>

  <p align="center">
    project_description
    <br />
    <a href="https://github.com/flopezag/IoTAgent-Turtle"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/flopezag/IoTAgent-Turtle">View Demo</a>
    ·
    <a href="https://github.com/flopezag/IoTAgent-Turtle/issues">Report Bug</a>
    ·
    <a href="https://github.com/flopezag/IoTAgent-Turtle/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

iaea iacta iae..

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* ...

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

...

### Prerequisites

The following software must be installed:

- Python 3.9
- pip
- virtualenv

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

The recommended installation method is using a virtualenv. Actually, the installation 
process is only about the python dependencies. By default, the service configuration
follow the description of the [local configuration file](./common/config.json). You 
have to modify the `broker` attribute to specify any other location of the FIWARE Context
Broker LD.

1. Clone the repo
   ```bash
   git clone https://github.com/flopezag/IoTAgent-Turtle.git
   ```
2. Define the configuration file: `./common/config.json`
3. Create the virtualenv
   ```bash
   virtualenv -ppython3.9 .env
   ```
4. Activate the python environment
   ```bash
   source .env/bin/activate
   ```
5. Install the requirements 
   ```bash
   pip install -r requirements.txt
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/flopezag/IoTAgent-Turtle/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Fernando López - [@twitter_handle](https://twitter.com/twitter_handle) - fernando.lopez@fiware.org

Project Link: [https://github.com/flopezag/IoTAgent-Turtle](https://github.com/flopezag/IoTAgent-Turtle)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the Apache2.0 License. See `LICENSE` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/flopezag/IoTAgent-Turtle.svg?style=for-the-badge
[contributors-url]: https://github.com/flopezag/IoTAgent-Turtle/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/flopezag/IoTAgent-Turtle.svg?style=for-the-badge
[forks-url]: https://github.com/flopezag/IoTAgent-Turtle/network/members
[stars-shield]: https://img.shields.io/github/stars/flopezag/IoTAgent-Turtle.svg?style=for-the-badge
[stars-url]: https://github.com/flopezag/IoTAgent-Turtle/stargazers
[issues-shield]: https://img.shields.io/github/issues/flopezag/IoTAgent-Turtle.svg?style=for-the-badge
[issues-url]: https://github.com/flopezag/IoTAgent-Turtle/issues
[license-shield]: https://img.shields.io/github/license/flopezag/IoTAgent-Turtle.svg?style=for-the-badge
[license-url]: https://github.com/flopezag/IoTAgent-Turtle/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username












Tutorial: http://blog.erezsh.com/create-a-stand-alone-lalr1-parser-in-python/

Generate parser:
python -m lark.tools.standalone json.g > json_parser.py

JSON Generator: https://www.json-generator.com

lexer=basic
python kk1.py generated.json > /dev/null  118.79s user 2.09s system 98% cpu 2:02.59 total

parser='lalr'
python kk1.py generated.json > /dev/null  17.42s user 0.33s system 94% cpu 18.774 total

tree-less
python kk1.py generated.json > /dev/null  8.94s user 0.13s system 97% cpu 9.324 total

using  pypy



IDE https://www.lark-parser.org/ide/

turtle EBNF: https://dajobe.org/2004/01/turtle/2007-09-11/
turtle EBNF LALR(1): https://www.w3.org/TR/turtle/#grammar-production-blankNodePropertyList

https://github.com/open-sdg/sdg-build/tree/1.7.0-dev/sdg/translations

Errors found in the turtle file
- The ConceptSchame (CodeList) of the NUTS has no skos:ConceptScheme
- skos:prefLabel -> puede ser un LanguageMap (different languages) o puede ser una Property (sólo una cadena)

SERVER
Use asyncio + Vibora

from vibora import Vibora, JsonResponse

app = Vibora()

@app.route('/')
async def home():
    return JsonResponse({'hello': 'world'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)


Send data to Orion-LD...

curl -iX POST 'http://localhost:1026/ngsi-ld/v1/entityOperations/create' \                                                                                                                           
-H 'Content-Type: application/json' \                         
-H 'Accept: application/ld+json' \                                                            
--data-raw '...'

http POST http://localhost:1026/ngsi-ld/v1/entityOperations/create Content-Type:application/ld+json Accept:application/ld+json << final.jsonld