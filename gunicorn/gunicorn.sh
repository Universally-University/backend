#! /bin/bash
### BEGIN INIT INFO
# Provides:          gunicorn
# Required-Start:    nginx
# Required-Stop:     
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: The main django process
# Description:       The gunicorn process that receives HTTP requests
#                    from nginx
# Location: /etc/init.d/gunicorn
#
### END INIT INFO
#
# Author:       Zack Hankin <admin@hankin.io>
#

if [ -e "/etc/default/gunicorn" ]
then
    . /etc/default/gunicorn
fi

export APPNAME=${APPNAME:-django_react_stack}
export PROJECTPATH=${PROJECTPATH:-/home/www-data/app}
export USER=${USER:-www-data}
export APPMODULE=${APPMODULE:-${APPNAME}.wsgi}
export PYTHONPATH=${PYTHONPATH:-${PROJECTPATH}/.venv/bin}
export DESC=${DESC:-gunicorn}
export NAME=${NAME:-gunicorn}
export CONFFILE=${CONFFILE:-/etc/gunicorn/gunicorn.conf.py}
export DAEMON=${DAEMON:-${PYTHONPATH}/gunicorn}
export PIDFILE=${PIDFILE:-/var/run/gunicorn.pid}
export SLEEPSEC=${SLEEPSEC:-1}
export UPGRADEWAITLOOPS=${UPGRADEWAITLOOPS:-5}
export CHECKSLEEP=${CHECKSLEEP:-3}

. /lib/lsb/init-functions
. /lib/init/vars.sh

DAEMON_ARGS="-c $CONFFILE --pythonpath $PYTHONPATH $APPMODULE"

case "$1" in
  start)
        log_daemon_msg "Starting $NAME daemon" "$APPNAME"
        start-stop-daemon --start --quiet --chdir $PROJECTPATH --pidfile $PIDFILE --exec $DAEMON -- $DAEMON_ARGS
        log_end_msg $?
    ;;
  stop)
        log_daemon_msg "Stopping $NAME daemon" "$APPNAME"
        killproc -p $PIDFILE $DAEMON
        log_end_msg $?
    ;;
  force-reload|restart|reload)
    $0 stop
    $0 start
    ;;
  status)
    status_of_proc -p $PIDFILE "$DAEMON" "$NAME" && exit 0 || exit $?
    ;;
  *)
    echo "Usage: /etc/init.d/$APPNAME {start|stop|restart|reload|force-reload|status}" >&2
    exit 1
    ;;
esac
