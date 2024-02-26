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
                -e DEV_EMAILS="<LIST OF DEVELOPER EMAILS>"
                <YOUR_NAME>/agora-app:latest
```
Notes:
* The `-p` parameter essentially links a port on your machine to one of Docker's internal ports. `1234:8080` maps your machine's port `1234` to Docker's port `8080`. For this command to work, you must use Docker's `8080` port.

