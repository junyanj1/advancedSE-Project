# advancedSE-Project
Group project for Professor Kaiser's advanced software engineering course.

Collaborators:
* Junyang Jin (UNI: jj3132)
* Elmira Aliyeva (UNI: ea2970)
* Ho Sanlok Lee (UNI: hl3436)
* Xihao Luo (UNI: xl3082)


## Install and Run

### Prerequisites

Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/). Confirm Docker and Docker-compose is installed by:
```sh
$ docker --version
Docker version xx.xx.x, build xxxxxxx

$ docker-compose --version
docker-compose version x.xx.x, build xxxxxxxx
```

### Start server in production mode
*IN PROGRESS*

### Start server in dev mode

Clone this repository and inside the repository's root directory:
```sh
$ docker-compose up --build
```

Confirm that the server is running:
```sh
$ curl localhost:3000/health
{"status":"UP"}
```


## (Optional) Visual Studio Code Environment for Developers
1. Open `/app` directory in VS Code.

2. Open Command Palette (`F1` key) and run "Remote-Containers: Reopen in Container".

3. If prompted, select the one that has Dockerfile.

4. (Optional) To enable IntelliSense and other debugging features, install Python VSCode extension in Dev container and set interpreter path to `/usr/local/bin/python`.Cl