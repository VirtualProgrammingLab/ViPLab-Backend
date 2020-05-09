# ViPLab-Backend
Virtual Programming Laboratory Backend

To run the ViPLab backend on your system you need:

* python3.x
* python-qpid-proton
* python-magic
* url64
* docker (and docker-py)

You can configure backend behavior by copying ```config.sample.ini``` 
to ```config.ini``` and change the variables.

Start the backend with:

```python3 backend.py```

Press ```Ctrl+C``` to stop the backend.

## Known issues / missing features

* no status messages what backend is doing (downloading container, starting, etc.)
* files are only send when the container is finished (no intermediate files)
* only *Container*-environment is working (c-environment will follow)
* web resource for image has not been tested (only published files would work)
* no error-handling