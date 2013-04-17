# modstash

modstash is a website for sharing tracked module music. 
It's written with Python 3 using CherryPy and Mako. It uses PostgreSQL as an persistence layer.

## Setting up
You can set up the PostgreSQL database with psql using the SQL from `createtables.sql`.

You also need to setup the environment configuration by creating an `environment.conf` file to the `src/` directory. See `environment.conf.sample` for details.

It's also possible to overwrite the database settings by editing the `src/.env` file.

## Tests

You can run tests with
        `foreman tests.Procfile`

or without environment variables you can use just python
        `python tests.py`
		