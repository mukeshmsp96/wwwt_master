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

# Assignment findings and reccomendations

**Findings**
- Hardcoded secret — `FILE_SECRET` is embedded in [app.py](app.py); this is a critical secret exposure risk.
- Missing header handling — `request.headers['X-Image-Secret']` raises KeyError if the header is absent and may crash the app or leak information when debug is enabled.
- Open-before-auth — the code opens the image file before validating the secret, which can cause unnecessary I/O and disclose information via errors.
- Path traversal risk — `file_name` is used directly in `images/{file_name}.png`; a crafted `file_name` may traverse directories (e.g., `..`) and access unintended files.
- Debug enabled in code — `os.environ['FLASK_DEBUG'] = 'true'` enables debug mode by default and can expose internals.
- No MIME/content-type — GET responses return raw bytes without a `Content-Type` header (should be `image/png`).
- App entry and port mismatch — Dockerfile `EXPOSE 80` vs `app.py` using `APP_PORT` with no default; container port binding may be incorrect.
- Fragile Dockerfile — using `FROM ubuntu` and installing Python/pip manually, no pinned dependency versions, and `COPY images/* images/` may fail if `images/` is empty.
- No `if __name__ == '__main__'` guard — `app.run()` runs on import, preventing safe testing and imports.
- Insufficient error handling — missing files or other errors will raise exceptions; with debug enabled, stack traces may be exposed.
- Unpinned dependency — `requirements.txt` lists `flask` with no version pinning; pinning improves reproducibility.
- Logging sensitive values — current logging prints the provided secret (`logging.info(f'bad file secret! {secret}')`); logs should avoid secrets.
- No authentication/authorization — relying on a single static secret is weak; consider stronger auth mechanisms.
- No rate-limiting or size checks — upload endpoint accepts request data without limits or validation; add size limits and validation.

**Recommendations**
- Move `FILE_SECRET` to an environment variable and avoid logging secrets.
- Access headers with `request.headers.get('X-Image-Secret')` and return a clear 400/401 when missing.
- Validate the secret before performing any file I/O.
- Sanitize `file_name` (allow only safe characters) and construct paths with `os.path.join`, verifying the resolved path is inside the `images/` directory.
- Do not enable Flask debug mode by default; control it via environment/config for local development only.
- Return proper response objects (e.g., `send_from_directory`) with `Content-Type: image/png` and appropriate status codes.
- Provide a sensible default port and guard `app.run(...)` with `if __name__ == '__main__'`.
- Improve the Dockerfile: use an official Python slim image, set `WORKDIR`, copy only needed files, pin dependencies, and ensure `images/` exists.
- Add upload validation and limits (max size, content-type checks) and consider rate-limiting.
- Add small unit tests for endpoints and input validation.
- Quick minimal fixes you can apply now: replace the hardcoded `FILE_SECRET` with `os.environ.get('FILE_SECRET')`, use header `.get()` checks, add the `if __name__ == '__main__'` guard, and use `send_from_directory` for GET responses.
