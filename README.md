Intended project structure:

<!-- ═	║	╒	╓	╔	╕	╖	╗	╘	╙	╚	╛	╜	╝	╞	╟
╠	╡	╢	╣	╤	╥	╦	╧	╨	╩	╪	╫	╬ -->

```
╚═ agora-app
   ╠═ src
   ║  ╠═ Dockerfile
   ║  ╠═ server.py
   ║  ╠═ utilities
   ║  ╠═ templates
   ║  ╠═ params
   ║  ╠═ tests
   ║  ╠═ static
   ║  ║  ╠═ css
   ║  ║  ╠═ js
   ║  ║  ╚═ img
   ║  ╚═ volumes (GITIGNORE)
   ║     ╠═ db
   ║     ╠═ img
   ║     ╠═ logs
   ║     ╚═ posts
   ╠═ docs
   ╠═ README.md
   ╚═ TODO.md
```

Create a `volumes` folder inside of `src` to house your copy of the database:
```
mkdir src/volumes
```
To add a (empty) database, run the following from inside of `volumes`:
```
sqlite3 agora.db < ../params/agora.schema
```
To build with docker, run the following in the top level of the repository (where the `Dockerfile` is):
```
sudo docker build -t <YOUR_NAME>/agora-app:latest .
```
and to run your image:
```
sudo docker run -p 8080:8080 \
                -v ./src/volumes:/app/volumes \
                -v ./src/templates:/app/templates \
                -v ./src/static:/app/static \
                -e HOST="<THE DOMAIN YOU ARE USING>" \
                -e MAILGUN_KEY="<YOUR MAILGUN KEY>" \
                -e RECAPTCHA_SITEKEY="<YOUR RECAPTCHA SITEKEY>" \
                -e RECAPTCHA_SERVERKEY="<YOUR RECAPTCHA SERVERKEY>" \
                <YOUR_NAME>/agora-app:latest
```
Notes:
* The `-p` parameter essentially links a port on your machine to one of Docker's internal ports. `1234:8080` maps your machine's port `1234` to Docker's port `8080`. For this command to work, you must use Docker's `8080` port.

## Deployment

To deploy the app for yourself, you will need to complete the following steps:

1. Acquire a server from which to serve the app.
1. Install Docker on the server.
1. Acquire a domain name for your server.
1. Set up integration with Mailgun email relay.
    1. Make a Mailgun account.
    1. Add your domain name as an approved domain for your account.
    1. Add SPF and DKIM records through your DNS provider for your domain, as suggested by Mailgun.
    1. Create a new HTTP API key for sending mail, and hold onto it.
1. Set up integration with Google reCaptcha.
    1. Visit the [Google developer's guide for reCaptcha](https://developers.google.com/recaptcha/intro).
    1. Click "get started" and create a score-based captcha.
    1. Add a name for the captcha and enter the domain name of your instance.
    1. Copy both the provided site key and secret key, and hold onto them.
1. Create a SQLite database in `src/volumes/`, using the schema from `src/params/agora.schema`.
1. Build the Docker image on your server.
1. Run the Docker image as shown above, setting the following environment variables:
    1. `HOST` should be your domain.
    1. `MAILGUN_KEY` should be your Mailgun HTTP API key.
    1. `RECAPTCHA_SITEKEY` and `RECAPTCHA_SERVERKEY` should be your respective site and secret keys for reCaptcha.
