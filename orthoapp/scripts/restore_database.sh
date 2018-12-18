if [ -z "$ORTHOAPP_HOME" ] || [ ! -d "$ORTHOAPP_HOME" ]; then
    echo "Error: Need to set ORTHOAPP_HOME to valid directory. Something like:"
    echo "  export ORTHOAPP_HOME="$(dirname "$PWD")""
    exit 1
fi

cd $ORTHOAPP_HOME

NAME=$1
tar xvzf backups/$NAME.tgz
sudo -u postgres psql orthoapp < backups/$NAME.sql
