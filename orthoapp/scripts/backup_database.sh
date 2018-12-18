if [ -z "$ORTHOAPP_HOME" ] || [ ! -d "$ORTHOAPP_HOME" ]; then
    echo "Error: Need to set ORTHOAPP_HOME to valid directory. Something like:"
    echo "  export ORTHOAPP_HOME="$(dirname "$PWD")""
    exit 1
fi

cd $ORTHOAPP_HOME

NAME=techbroker-backup-`date '+%Y-%m-%d-%H-%M-%S'`$1
tar cvzf backups/$NAME.tgz media
pg_dump orthoapp > backups/$NAME.sql

echo backup complete to: backups/$NAME
