# Cybersecurity Incident Data Analytics

An application to process and serve data from the VERIS community dataset for the purposes of my Cybersecurity Incident Review data visualiser app.

### Development

This project uses a Python venv to keep track of dependencies.

```bash
$ cd ~
$ git clone https://github.com/dqna64/cybersec-analytics-py
```

Activate the venv:

```bash
$ cd ~/cybersec-analytics-py
$ ./env/bin/activate
```

Set necessary environment variables:

```bash
(env) $ export MONGODB_SECREVIEW_CONN_STR=<your_connection_string>
```

### Dependencies

Project dependencies listed in `/requirements.txt`.

- **pymongo 4.0.0** MongoDB client for Python.