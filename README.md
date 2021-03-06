GSvarWeb
----------
[![Build Status](https://travis-ci.org/imgag/GSvarWeb.svg?branch=master)](https://travis-ci.org/imgag/GSvarWeb)

`GSvarWeb` is a remote API and browser application for [ngs-bits](https://github.com/imgag/ngs-bits).

Currently it is capable of displaying and processing `.GSvar` files

![GSvar table](./screenshots/gsvar-table.png "GSvar table")

## Architecture

`GSvarWeb` consists of server API which is [specified](./openapi.yaml) and implemented with [flask](http://flask.pocoo.org) using [OpenAPI](https://www.openapis.org/). 

Installation instructions can be found in the [API folder](./api/README.md).

The following environment variables can be set during startup:

| Variable        | Meaning                                    | Default |
| --------------- |:------------------------------------------:|:-------:|
| PORT            | Which port the server should listen on     | 8080    |
| DATA            | Where to put uploaded files                | $PWD    |
| NGS_BITS        | Where to find ngs bits binaries            | $PWD    |
| MEGSAP          | Where to find the megSAP directory         | None    |
| PRODUCTION      | Whether or not the server is in production | False   |
| AUTH_DOMAIN     | The domain to authenticate against  | auth.imgag.de  |
| AUTH_REALM      | The authentication realm                   | debug   |
| CORS_ORIGINS    | Comma-seperated list of allowed hosts      | -       |

You can start the server using above variables like so:

```
DATA=$PWD/data NGS_BITS=/some/path/to/ngs-bits/bin python3 -m openapi_server
```

You can find the OpenAPI UI under `/v1/ui` for testing and experiment purposes.

For convenience reasons the server also can serve files from the `dist` folder, allowing it to serve the frontend.

The API works by invoking shell pipelines and the command line interface of `ngs-bits`.

### Frontend

The frontend is a single page application built with [Vue](https://vuejs.org/) and [Vuetify](https://vuetifyjs.com/en/). Build instructions can be found in [frontend folder](./frontend/README.md).

The following environment variables can be set:

| Variable          | Meaning                                                  | Default                  | 
| ----------------- | -------------------------------------------------------- | ------------------------ |
| VUE_APP_API_URL   | Which URL to use for API requests                        | http://localhost:9000/v1 |
| VUE_APP_REALM     | The authorization realm to use                           | debug                    |

You can invoke environment variables like so:

```
VUE_APP_API_URL=http://localhost:9000/v1  npm run build
```

After building the project one can copy the `dist` folder into the `api` directory. When setting `SERVE_DIST`, it will be displayed as the default.

## Deployment in production

Currently `GSvarWeb` has not been tested in a production environment (meaning, it has not been publicly deployed to the WWW).

It is strongly recommended to use standalone [WSGI](https://wsgi.readthedocs.io/en/latest/index.html) containers, [such as gunicorn](http://flask.pocoo.org/docs/1.0/deploying/wsgi-standalone/#gunicorn), additionally behind a proxy.
