# advancedSE-Project

![Commit](http://18.218.235.18/static/badges/commit-badge.svg)
![Coverage](http://18.218.235.18/static/badges/coverage-badge.svg)

Group project for Professor Kaiser's advanced software engineering course.

Collaborators:
* Junyang Jin (UNI: jj3132)
* Elmira Aliyeva (UNI: ea2970)
* Ho Sanlok Lee (UNI: hl3436)
* Xihao Luo (UNI: xl3082)


## API Specification

http://18.218.235.18/static/index.html

## Server
```sh
$ curl 18.218.235.18/health
{"commit_id":"xxxxxxx","status":"UP"}
```


## Install and Run Locally

### Prerequisites

Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/). Confirm both Docker and Docker-compose are installed by:
```sh
$ docker --version
Docker version xx.xx.x, build xxxxxxx

$ docker-compose --version
docker-compose version x.xx.x, build xxxxxxxx
```

### Start the API Server

Clone this repository and inside the repository's root directory:
```sh
# Production mode
$ docker-compose -f docker-compose.prod.yml up

# Or, development mode
$ docker-compose -f docker-compose.dev.yml up --build
```

The default port number is 80 for production and 3000 for development mode. Confirm that the server is running:
```sh
# Production mode
$ curl localhost/health
{"status":"UP"}

# Development mode
$ curl localhost:3000/health
{"status":"UP"}
```


## (Optional) Visual Studio Code Environment for Developers

https://code.visualstudio.com/docs/remote/containers#_quick-start-open-an-existing-folder-in-a-container

1. Open `/app` as the root directory in VS Code.

2. Open Command Palette (`F1` key) and run "Remote-Containers: Reopen in Container".

3. If prompted, select the one that says "From 'Dockerfile'".

4. (Optional) To enable IntelliSense and other debugging features, install Python VSCode extension in Dev container and set interpreter path to `/usr/local/bin/python`.

5. To run `flake8`:
```sh
$ flake8
```

6. To run `PyUnit` and `coverage`:
```sh
$ coverage run -m unittest discover test
$ coverage report --omit "test*"
```

### Docker Commands

Shutdown server and clear containers
```sh
$ docker-compose -f docker-compose.dev.yml down
```

Clean up all dangling images, containers, networks, etc.
```sh
$ docker system prune
```

### Adding new Python library
1. Add module to `/app/requirements.txt`
2. Rebuild VS Code container

    a. Open Command Palette (`F1` key) and run "Remote-Containers: Rebuild Container".

3. Rebuild dev server

    a. Close dev server

    b. Clean up Docker (see abov)

    c. Restart the API Server


## References

- PEP 8 Style guide: https://www.python.org/dev/peps/pep-0008/
- gitmoji: https://gitmoji.dev/
