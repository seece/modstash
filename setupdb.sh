#!/bin/bash
set -e
USAGE="Usage: $0 database_name"
commandfile="createtables.sql"

if [ "$#" == "0" ]; then
        echo "$USAGE"
        exit 1
fi

dbname=$1
shift
commands=""
#commands+=" CREATE DATABASE $dbname"
set -x
psql --command "\\connect $dbname" --command "\\i $commandfile" 


