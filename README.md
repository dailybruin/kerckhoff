[logo]: https://user-images.githubusercontent.com/1896936/28765492-cb46e55c-757f-11e7-996c-e53a95eba862.png "Kerckhoff Logo"
[spec link]: https://docs.google.com/a/media.ucla.edu/document/d/1ejb3iIyqSo2M6-fKhweAkp6MdS63gPsNmQje8iEUggc/edit?usp=sharing "Kerckhoff Specification Link"
[docker link]: https://www.docker.com/ "Docker Homepage"
[docker doc link]: https://docs.docker.com/ "Docker Documentation"
[docker compose doc link]: https://docs.docker.com/compose/ "Docker Documentation: Compose"

![kerckhoff logo][logo]

# Kerckhoff

[![Dependencies](https://david-dm.org/daily-bruin/kerckhoff/status.svg?style=flat)](https://david-dm.org/daily-bruin/kerckhoff)
[![Dev dependencies](https://david-dm.org/daily-bruin/kerckhoff/dev-status.svg?style=flat)](https://david-dm.org/daily-bruin/kerckhoff?type=dev)

Kerckhoff is a static-site management and deployment solution used by the Daily
Bruin, UCLA's student run daily newspaper.

This project is currently under active development.

## Features/Roadmap

You can find the spec [here][spec link]. An `@media.ucla.edu` email is required.

## Setting Up the Development Environment

We are using [Docker][docker doc link] and
[Docker-Compose][docker compose doc link] for deployment and development. Feel
free to read up more on Docker if you're interested in the details of how it
works, or reach out to us on Slack.

1.  Install Docker from the official website. Follow the instructions for your
    specific platform.

2.  Use `git clone https://github.com/daily-bruin/kerckhoff.git` to clone the
    repository.

    * **Note**: If you're using Windows, run the following two commands before
      cloning the repository:
    * `git config --global core.eol lf`
    * `git config --global core.autocrlf input`

3.  Create a .env file in your repository folder (acquire content from Internal Tools)

    * **Note**: You need values for `AWS_ACCESS_KEY_ID`,
      `AWS_SECRET_ACCESS_KEY`, and `REPOSITORY_FOLDER_ID`, but if you aren't in
      Daily Bruin, you can't use ours ;). If you are,
      [click here](https://dailybruin.slack.com/archives/C7RT6B4FP/p1527528167000076)!

4.  Run ```docker-compose up --build``` which will create all containers you need

5. Run ```docker-compose run web ./kerckhoff/manage.py makemigrations``` and then ```docker-compose run web ./kerckhoff/manage.py migrate``` in a separate terminal.

6.  Let's do some server side stuff. You should create an admin user to log in.
    Create a superuser using `docker-compose run web ./kerckhoff/manage.py createsuperuser`
    Remember your admin username and password!

7.  Now you will want to set up login for your Kerckhoff instance. Create or get a
    Google OAuth client id and secret, and visit `localhost:5000/admin/`. Login with your newly
    created admin account, and create a new Social Application (under Social Accounts).
    Select Google as provider. Set name to Google, fill in the Client ID and secret key and
    move the site (example.com) to the right. (help!). You can find the Client ID and the secret
    key [here](https://dailybruin.slack.com/archives/C7RT6B4FP/p1526580559000282)
    Now you can log out, and log in with the usual flow by visiting `localhost:5000/manage`

## How to Contribute

1.  [Set up the development environment properly.](#setting-up-the-development-environment)

2.  Look for an open issue (could be a feature or a bugfix) or create one of
    your own (so we know you're working on a new thing!)

3.  Create a branch with `git checkout -b feature/<my-awesome-feature>` for a
    feature or `git checkout -b fix/<my-cool-fix>` for a fix.

4.  Write some badass code.

5.  Stage your files with `git add <files I want to update>` or `git add .`.
    (The latter adds all the files in the current directory, so **be careful!**)

6.  Commit your changes with
    `git commit -m <a commit message explaining what you did>`.

    * **Important**: Don't commit secret keys or any sort of sensitive
      information into git! Always use `git status` to double check if you're
      not sure.

7.  Push your commits with `git push`. The push will usually fail for a brand
    new feature branch. Just follow the instructions on your terminal to resolve
    it.

8.  Create a pull request (request to merge your branch into the master branch)
    using the button on Github!

Remeber to `migrate` and `createsuperuser`!
