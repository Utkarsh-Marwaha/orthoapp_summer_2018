if [ -z "$ORTHOAPP_HOME" ] || [ ! -d "$ORTHOAPP_HOME" ]; then
    echo "Error: Need to set ORTHOAPP_HOME to valid directory. Something like:"
    echo "  export ORTHOAPP_HOME="$(dirname "$PWD")""
    exit 1
fi

cd $ORTHOAPP_HOME

sudo systemctl restart nginx
nohup gunicorn -b 127.0.0.1:8000 --workers=3 --access-logfile orthoapp-gunicorn.log --log-level info --name orthoapp orthoapp.wsgi &> /dev/null &
