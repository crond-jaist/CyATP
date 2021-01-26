
# CyATP: Cybersecurity Awareness Training Platform

CyATP is a web platform for cybersecurity awareness training that
makes use of Natural Language Generation (NLG) techniques to
automatically generate the training content; the serious game approach
is employed for learning purposes. Using this platform, learners can
increase their security awareness knowledge and put it to use in their
daily life. CyATP is being developed by the Cyber Range Organization
and Design ([CROND](https://www.jaist.ac.jp/misc/crond/index-en.html))
NEC-endowed chair at the Japan Advanced Institute of Science and
Technology ([JAIST](https://www.jaist.ac.jp/english/)) in Ishikawa,
Japan.

An overview of the CyATP architecture is provided in the figure
below. Trainees use the web interface to access the **Concept Map**
and **Learn Concepts** pages in order to find out about the security
concepts they want to study. They can also use the **Take Quiz** and
**Crossword Puzzle** pages to test and deepen their knowledge. The
front end of the CyATP platform is developed using Bootstrap and
jQuery, and the back end employs Flask and Neo4j.

<div align=center><img src='https://github.com/blab-private/CyATP/blob/master/static/images/platform_architecture.png'></div>

CyATP already includes some pregenerated awareness training
content. To learn more about this content, and about how to add new
training content to the database, see the [Training Content
Guide](https://github.com/blab-private/CyATP/blob/master/training_content/content_guide.md).


## Prerequisites

As we store some components of the training content into a Neo4j graph
database, the following step must be carried out before using CyATP:

* **Install the Neo4j database platform.** You can download the [Neo4j
    Community Edition](https://neo4j.com/download-center/#community)
    free of charge; we recommend Neo4j v4.0+. (Note that all versions
    of Neo4j require Java to be preinstalled.)

The following optional step can also be performed:

* **Create a virtual Python environment.** You can create an isolated
    Python environment and install packages into this virtual
    environment to avoid conflicts. This can be done using the options
    `venv` for Python 3 or `virtualenv` for Python 2. For example, you
    can run the following commands to create and activate the
    `cyatp-env` virtual environment:

  ```
  $ python3 -m venv cyatp-env
  $ source cyatp-env/bin/activate
  ```


## Setup

To set up CyATP, follow the steps below:

1. **Install the latest version of CyATP.** Use the
[releases](https://github.com/blab-private/CyATP/releases) page to
download the source code archive of the latest version of the training
platform and extract it on your computer.

2. **Install the required Python libraries.** Go to the directory
where CyATP is located and install the required third-party libriaries
by running the following command:

   ```
   $ sudo -H pip install -r requirements.txt
   ```

3. **Set up the Neo4j database.** Follow the next steps in a terminal
     window to install the CyATP training database content into Neo4j:
    1. Enter the directory where Neo4j was installed (e.g.,
    `~/neo4j-community-4.1.1/`).
    2. Stop the Neo4j database service:
       ```
       $ ./bin/neo4j stop
       ```
    3. Copy the file `neo_db/cyatp.db` from the CyATP directory to the
    `bin/` directory in the Neo4j installation:
       ```
       $ cp <CYATP_PATH>/neo_db/cyatp.db <NEO4J_PATH>/bin
       ```
    4. Load the CyATP training database into Neo4j:
       ```
       $ neo4j-admin load --from=cyatp.db --database=neo4j --force
       ```
    5. Restart the Neo4j database service:
       ```
       $ ./bin/neo4j restart
       ```

### Notes

* After installing Neo4j, when you access http://localhost:7474 for
  the first time you will be asked to change the default database
  password. After you do that, make sure to also change the password
  included in file `neo_db/config.py` in the CyATP directory.

* After setting up the Neo4j database with CyATP training data, you
  can access http://localhost:7474 and run the following command to
  retrieve the existing data (the
  [Cypher](https://neo4j.com/developer/cypher/) query language is
  used):

  ```
  MATCH (n) RETURN n
  ```


## Quick Start

In order to start the CyATP web server, use a terminal window to go to
the project directory and execute the following command:

```
$ env FLASK_APP=cyatp.py flask run
```

By default the web interface of CyATP can be accessed only locally at
http://127.0.0.1:5000/. The screenshot below displays the top page,
which provides an overview of CyATP and the functions of each
additional page.

<div align=center><img width='600' src='https://github.com/blab-private/CyATP/blob/master/static/images/cyatp_screenshot.png'></div>

### Configuration

* If you want to change the default port used by CyATP (which is
  `5000`), use the option `-p` when running the program:
  ```
  $ env FLASK_APP=cyatp.py flask run -p <port_number>
  ```

* To make the CyATP server publicly available, use the option
  `--host=0.0.0.0` when running the program:
  ```
  $ env FLASK_APP=cyatp.py flask run --host=0.0.0.0
  ```

* For more details about setting up Flask applications, see this
  [tutorial](https://flask.palletsprojects.com/en/1.1.x/quickstart/). CyATP
  can also be deployed via a cloud service, such as Amazon Web
  Services (AWS), Microsoft Azure or Alibaba Cloud. For details, see
  the documentation on [Flask application
  deployment](https://flask.palletsprojects.com/en/1.1.x/deploying/).


## References

For a research background regarding CyATP, please refer to the
following document:

* Y. Zeng, "Content Generation and Serious Game Implementation for
  Security Awareness Training", Master's thesis, March 2021.

For a list of contributors to this project, check the file
CONTRIBUTORS included with the source code.
