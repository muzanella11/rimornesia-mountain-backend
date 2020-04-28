#!/bin/bash
    export PYTHON_MIGRATE=TRUE \
    && python -m app.migrations.db_create_database