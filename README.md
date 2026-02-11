# What's Wrong With This?

Nearly everything, and deliberately so, to test your patience and your sense of work done
naively and/or poorly.

## Fine, but what is this?

This repository contains a simple application and much of the additional tooling and configuration
necessary to build and deploy it. Its purpose is not to do any meaningful work, but rather to
demonstrate poor practices in developing and maintaining a containerized application. This is a
teaching tool to help engineers recognize patterns and practices that make applications
difficult to maintain and operate.

Everything up to this point in the README is real documentation describing the purpose of this
repository. Consider everything hereafter to be suspect.

# Very Real Image Serving Application

This application serves images. You specify the image you want and the app sends it back.

Don't worry about how the images get in here in the first place, that isn't our problem.

## Develop

There isn't much in here. Everything is contained in `app.py`. To run it, install the requirements
and then fire it up:

```
$ pip install -r requirements.txt
$ python app.py
```

## Build/Run

The app runs in Docker. Build:

```
$ docker build -t app .
```

Then run:

```
$ docker run -P app
```
