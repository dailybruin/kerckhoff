[logo]: https://user-images.githubusercontent.com/1896936/28765492-cb46e55c-757f-11e7-996c-e53a95eba862.png  "Kerckhoff Logo"

[spec link]: https://docs.google.com/a/media.ucla.edu/document/d/1ejb3iIyqSo2M6-fKhweAkp6MdS63gPsNmQje8iEUggc/edit?usp=sharing "Kerckhoff Specification Link"

[docker link]: https://www.docker.com/ "Docker Homepage"

[docker doc link]: https://docs.docker.com/ "Docker Documentation"

[docker compose doc link]: https://docs.docker.com/compose/ "Docker Documentation: Compose"

![kerckhoff logo][logo]

# Kerckhoff

Kerckhoff is a static-site management and deployment solution used by the Daily Bruin, UCLA's student run daily newspaper.

This project is currently under active development.

## Features/Roadmap

You can find the spec [here][spec link]. An `@media.ucla.edu` email is required.

## Setting Up the Development Environment

We are using [Docker][docker doc link] and [Docker-Compose][docker compose doc link] for deployment and development. Feel free to read up more on Docker if you're interested in the details of how it works, or reach out to us on Slack.

1. Install Docker from the official website. Follow the instructions for your specific platform.

2. Use `git clone https://github.com/daily-bruin/kerckhoff.git` to clone the repository.
    * **Note**: If you're using Windows, run the following two commands before cloning the repository:
    * `git config --global core.eol lf`
    * `git config --global core.autocrlf input`

3. Create a .env file in your repository folder with the following contents:
    ``` .env
    DATABASE_URL=postgres://postgres@db:5432/postgres
    SITE_HOST=localhost
    DEBUG=True
    SECRET_KEY=kerchkoff-secrets
    S3_SITE_UPLOAD_BUCKET=dev.kerckhoff.dailybruin.com
    S3_ASSETS_UPLOAD_BUCKET=assets.dailybruin.com
    AWS_ACCESS_KEY_ID=<your key here>
    AWS_SECRET_ACCESS_KEY=<your secret key here>
    REPOSITORY_FOLDER_ID=<your id here>
    LIVE_PUSH_SERVER=google.com
    DJANGO_SETTINGS_MODULE=kerckhoff.settings
    ```
    * **Note**: You need values for `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `REPOSITORY_FOLDER_ID`, but you can't use ours ;).

4. Use `docker-compose up` to build/pull and configure the Docker images for the Django server, the Postgres database and Redis automatically based on the configuration in `docker-compose.yml`.

5. The site should now be running on `localhost:5000`, and  the server will automatically restart after any edits you make to Python and JS source files. Refresh the page to see them! (WIP: livereload)

## How to Contribute

1. [Set up the development environment properly.](#setting-up-the-development-environment)

2. Look for an open issue (could be a feature or a bugfix) or create one of your own (so we know you're working on a new thing!)

3. Create a branch with `git checkout -b feature/<my-awesome-feature>` for a feature or `git checkout -b fix/<my-cool-fix>` for a fix.

4. Write some badass code.

5. Stage your files with `git add <files I want to update>` or `git add .`. (The latter adds all the files in the current directory, so __be careful!__)

6. Commit your changes with `git commit -m <a commit message explaining what you did>`.
    * **Important**: Don't commit secret keys or any sort of sensitive information into git! Always use `git status` to double check if you're not sure.

7. Push your commits with `git push`. The push will usually fail for a brand new feature branch. Just follow the instructions on your terminal to resolve it.

8. Create a pull request (request to merge your branch into the master branch) using the button on Github!

Remeber to `migrate` and `createsuperuser`!
