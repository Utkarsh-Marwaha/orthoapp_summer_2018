if [ -z "$ORTHOAPP_HOME" ] || [ ! -d "$ORTHOAPP_HOME" ]; then
    echo "Error: Need to set ORTHOAPP_HOME to valid directory. Something like:"
    echo "  export ORTHOAPP_HOME="$(dirname "$PWD")""
    exit 1
fi

cd $ORTHOAPP_HOME

sql_script="scripts/create_user.sql"

echo "DROP ROLE ortho_admin;" > $sql_script
echo "CREATE USER ortho_admin WITH PASSWORD '$ORTHOAPP_PASSWORD';" >> $sql_script
echo "ALTER ROLE ortho_admin SET client_encoding TO 'utf8';" >> $sql_script
echo "ALTER ROLE ortho_admin SET default_transaction_isolation TO 'read committed';" >> $sql_script
echo "ALTER ROLE ortho_admin SET timezone TO 'UTC';" >> $sql_script

sudo -u postgres psql < $sql_script

rm $sql_script
