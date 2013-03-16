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
#commands+="CREATE DATABASE $dbname"
commands+=" \connect $dbname"
commands+=" \set echo ALL"
commands+=" \i $commandfile"

echo psql --command \"$commands\"

