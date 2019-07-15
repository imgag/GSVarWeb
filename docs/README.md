GSvarWeb documentation
----------------------

`GSvarWeb` is a bundle of the following four components:

- a website built with [Vue.js](https://vuejs.org/) and hosted on [Netlify](https://netlify.com)
- a RESTfull server generated with [OpenAPI](https://www.openapis.org/) and hosted on our own server at [gsvarapi.imgag.de](https://gsvarapi.imgag.de/v1/ui)
- an installation of [MegSAP](https://github.com/imgag/megSAP/) which is used by the aforementioned RESTfull server
- an authentication service. We use [KeyCloak](https://www.keycloak.org/) because it was free and easy to set up. The service is hosted at our own server

The way the application works is illustrated below:

![user flow](user_flow.svg)

This has some implications:

- the `frontend`, the `api` and `MegSAP` are stateless. They can be deployed anywhere, anytime. 
- since the authentication service relies on `JWT` it could be replaced by e.g [Auth0](https://auth0.com).

### Generating a server

If you want to generate / modify the API, you can use the below command to do this:

```
java -jar openapi-generator-cli-4.0.0-beta3.jar generate -i path/to/imgag/ngs-remote/openapi.yaml -g python-flask -o path/to/imgag/ngs-remote/api
```

Bear in mind that the `.openapiignore` file is used to guard overrides, and that you might have to comment some lines out if you want specific files to be overridden (`controllers`).

### Developing locally with the authentication server

Since we do not want to mess up our production deployment, the realm used by default is the `debug` realm.
If you want to modify the site you will to either add a user to that realm, or change the used realm using the environment variable.
