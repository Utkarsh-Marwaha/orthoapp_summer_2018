if [ -z "$ORTHOAPP_HOME" ] || [ ! -d "$ORTHOAPP_HOME" ]; then
    echo "Error: Need to set ORTHOAPP_HOME to valid directory. Something like:"
    echo "  export ORTHOAPP_HOME="$(dirname "$PWD")""
    exit 1
fi

cd $ORTHOAPP_HOME

sql_script="scripts/create_database.sql"

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

echo "DROP DATABASE orthoapp;" > $sql_script
echo "CREATE DATABASE orthoapp OWNER ortho_admin;" >> $sql_script
echo "GRANT ALL PRIVILEGES ON DATABASE orthoapp TO ortho_admin;" >> $sql_script

sudo -u postgres psql < $sql_script

rm $sql_script

echo Create and run migrations ...
python3 manage.py makemigrations
python3 manage.py migrate

echo Create admin account ...
python3 manage.py createsuperuser
