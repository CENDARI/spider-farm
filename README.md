# Installation

1. First create a virtual environment by running `virtualenv ENV_NAME`, e.g. `virtualenv webscraping-test` 
This will create a directory ENV_NAME where all the dependencies will be installed. 
2. Activate the environment by running `source ENV_NAME/bin/activate` (You can deactivate the environment by running `deactivate`.) If `pip --version` shows something less than 6.0.0, please update pip by running `pip install -U pip`
3. Clone all aipberoun repositories by running `git clone REPOSITORY_URL` for each REPOSITORY_URL described in section [Source code](#source-code) below.
4. Install Portia according to its [documentation](https://github.com/scrapinghub/portia) by running 

  ```
  pip install -r requirements.txt
  pip install -e ./slybot
  ```
inside its directory.
5. Install scrapyd by running `pip install -e SCRAPYD_DIR`
6. Install scrapy by running `pip install -e SCRAPY_DIR` and checkout the branch `aip`

*Please note that it is important to install scrapy last, since otherwise the services will use version of scrapy they pull via their requirements. You can test which scrapy is going to be run by `which scrapy`.*

# Running

The service contains two independent parts: Portia and scrapyd.

*Portia* is a webapplication for creating scraping spiders. One annotates graphically which parts of a webpage is mapped to which `field`. The resulting spider then crawls the website according to rules, which are also configurable within Portia, and outputs scraped data in form field_name --> scraped data. Portia spiders are in particular scrapy spiders and so their output can be either json, xml or csv. See the [Scrapy documentation](http://doc.scrapy.org/en/latest/topics/feed-exports.html) for details.

*Scrapyd* is a service for running and monitoring spiders which we've extended according to the CENDARI specification. You can write your own scrapy spiders and deploy them. See spider-farm repository and the official [Scrapy documentation](http://doc.scrapy.org/en/latest/topics/spiders.html).

## Portia

Run `twistd -n slyd` in the PORTIA_DIR/slyd directory. This will open Portia webapplication at the port 9001. Use it by entering `http://URL:9001/static/index.html` in the browser. There is a detailed explanation of this application on its website [scrapinghub/portia](https://github.com/scrapinghub/portia)

Once you create a project it is stored in PORTIA_DIR/slyd/data/projects/ You can deploy these projects/spiders to a scrapyd service by running `scrapyd-deploy` inside a project's directory. The deployment and its configuration works the same as for handwritten spiders, see below.

## Scrapyd

One can configure scrapyd to run as a daemon but for testing purposes it is easier to just create an empty directory and run `scrapyd` inside it. Scrapyd service will then store all deployed spiders and all data they scrape as well as logs in that directory. Scrapyd logs everything to the console so one can monitor what's happening without checking the log files. By default it runs on port 6800.  

You can control scrapyd service by its API for details see [its documentation](http://scrapyd.readthedocs.org/en/latest/api.html). We've added one more API `scrape.json` which takes just one parameter `urls` which is a new-line  separated list of urls to be scraped. *If you leave spaces between urls the Portia spiders won't work!* To test passing of multiple urls in bash you can use the following syntax `$'url1\nurl2\nurl3'`, e.g. run `curl http://localhost:6800/schedule.json -d project=demo-portia -d spider=mirabile -d start_urls=$'http://www.mirabileweb.it/title/divisio-textus-summae-contra-gentiles-thomae-de-aq-title/129674\nhttp://www.mirabileweb.it/title/acta-capitulorum-generalium-ordinis-praedicatorum--title/18402'`

Mapping url --> spider is done in SCRAPYD_DIR/scrapyd/mapping.conf that contains at least one pair `url regexp : spider-name` for each project. So for example we can create several spiders inside of mirabile project and configure via regexps which spider is going to be run for which type of url.

For deploying new spiders to scrapyd service we  refer to the [official documentation](http://scrapyd.readthedocs.org/en/latest/deploy.html). Configuration for the upload is in the file scrapy.cfg inside the project's directory. See http://scrapyd.readthedocs.org/en/latest/config.html for details.

# Source code

scrapy.git 
  - contains scrapy framework with changes that allow for passing of arbitrary starting urls to spiders

scrapyd.git 
  - contains scrapyd webservice for deployment, running and monitoring of spiders

portia.git 
  - contains a snapshot of the Portia webscraper with a fix that makes it possible to deploy Portia based spiders to scrapyd service

spider-farm.git 
  - contains our own repository for hand-made spiders. 

Our aim was to introduce minimal necessary changes to upstream repositories in order to ease maintainability burden. 

The biggest changes are in scrapyd service, where we have added  interface scrape.json that takes just one parameter `urls` (which is a list of urls to be scraped)  and then for each url it starts a spider job that can be monitored via [scrapyd interface](http://scrapyd.readthedocs.org/en/latest/api.html). The project name and spider names have to match the project name and spider names deployed in the scrapyd service.

Our change to scrapy.git is just a small patch that allows passing starting url to spiders. We've discovered that Portia is not compatible with scrapy/master and so we've based another branch on scrapy/0.25.1. This is the primary branch for our development.

~~In portia.git we've just added a small bugfix that will be hopefully integrated into the official repository.~~ The bugfix is already upstream, but we keep our own fork of Portia in case we decide to change its spider template or handling of multiple urls.
