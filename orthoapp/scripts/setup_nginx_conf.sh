if [ -z "$ORTHOAPP_HOME" ] || [ ! -d "$ORTHOAPP_HOME" ]; then
    echo "Error: Need to set ORTHOAPP_HOME to valid directory. Something like:"
    echo "  export ORTHOAPP_HOME="$(dirname "$PWD")""
    exit 1
fi

sudo ln -f -s $TECHBROKER_HOME/conf/nginx.conf /etc/nginx/sites-enabled/techbroker
