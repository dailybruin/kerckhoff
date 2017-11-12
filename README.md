![kerckhoff logo](https://user-images.githubusercontent.com/1896936/28765492-cb46e55c-757f-11e7-996c-e53a95eba862.png)

# Kerckhoff
Kerckhoff is a static-site management and deployment solution used by the Daily Bruin, UCLA's student run daily newspaper.

This project is currently under active development.

## Features/Roadmap
You can find the spec [here](https://docs.google.com/a/media.ucla.edu/document/d/1ejb3iIyqSo2M6-fKhweAkp6MdS63gPsNmQje8iEUggc/edit?usp=sharing). `@media.ucla.edu` email required.

## Setting up the Dev environment
We are using [Docker](https://docs.docker.com/) and [Docker-Compose](https://docs.docker.com/compose/) for deployment and development. Feel free to read up more on Docker if you're interested in the details of how it works, or reach out to us on Slack.

0. Install Docker from the official website. Follow the instructions for your specific platform.

1. `git clone https://github.com/daily-bruin/kerckhoff.git` - to clone the repository.
   NOTE(Windows users): Run the following 2 commands before git cloning the repo
   		`git config --global core.eol lf
		 git config --global core.autocrlf input`

2. create a .env file with the following contents:
   `DATABASE_URL=postgres://postgres@db:5432/postgres
    DEBUG=on
    SECRET_KEY=kerchkoff-secrets`.

3. `docker-compose up` - this builds/pulls and configures the Docker images for the Django server, the Postgres database and Redis automatically based on the configuration in `docker-compose.yml`. 

4. The site should now be running on `localhost:5000`, and  the server will automatically restart after any edits you make to Python and JS source files. Refresh the page to see them! (To come: livereload)

## How do I contribute?
1. Set up the Dev environment properly.

2. Look for an open issue (could be a feature or a bugfix) or create one of your own (so we know you're working on a new thing!)

3. `git checkout -b feature/<my-awesome-feature>`

4. Write some badass code.

5. `git add <files I want to update>` or `git add .` (This adds all the files in the current directory - be careful!)

6. `git commit -m <a commit message explaining what you did>`

7. `git push` - this will usually fail for a brand new feature branch, just follow the instructions on your terminal to resolve it

8. Create a pull request (request to merge your branch into the master branch) using the button on Github!

9. Remeber to migrate and createsuperuser

! Important ! - Don't commit secret keys or any sort of sensitive information into git! Always do a `git status` to double check if you're not sure.

