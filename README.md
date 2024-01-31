Intended project structure:

<!-- ═	║	╒	╓	╔	╕	╖	╗	╘	╙	╚	╛	╜	╝	╞	╟
╠	╡	╢	╣	╤	╥	╦	╧	╨	╩	╪	╫	╬ -->

```
╚═ agora-app
   ╠═ src
   ║  ╠═ Dockerfile
   ║  ╠═ server.py
   ║  ╠═ utilities
   ║  ╠═ js
   ║  ╠═ css
   ║  ╠═ templates
   ║  ╠═ params
   ║  ╠═ tests
   ║  ╚═ volumes (GITIGNORE)
   ║     ╠═ db
   ║     ╠═ img
   ║     ╚═ posts
   ╠═ docs
   ╠═ README.md
   ╚═ TODO.md
```

To add a (empty) database, run the following from inside of `volumes`:
```
sqlite3 agora.db < ../params/agora.schema
```
To build with docker:
```
sudo docker build -t <YOUR_NAME>/agora-app:latest .
```
and to run your image:
```
sudo sudo docker run -p 8080:8080 \ 
                     -v ./src/volumes:/app/volumes \
                     -v ./src/templates:/app/templates \
                     frpzzd/agora-app:latest
```
