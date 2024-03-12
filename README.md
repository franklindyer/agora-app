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
You can run this with Docker Compose. First you need to define a few environment variables in a file called `.env` in the project root. (It should be gitignored, since it will have some sensitive info in it.) The following environment variables must be defined there:

- `AGORA_PORT`: the physical port on your machine to map onto the Docker image's virtual port
- `HOST`: the domain name at which you're serving the app
- `MAILGUN_KEY`: the API key that you're using for Mailgun
- `RECAPTCHA_SITEKEY`: your reCaptcha site key
- `RECAPTCHA_SERVERKEY`: your reCaptcha server key
- `DEV_EMAILS`: a comma-separated list of emails of people you would like to receive bug report emails for the Agora instance

Then, just run `docker compose up`!

