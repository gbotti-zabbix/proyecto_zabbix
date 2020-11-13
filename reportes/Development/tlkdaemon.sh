#! /bin/bash
# Copyright (c) 1996-2012 My Company.
# All rights reserved.
#
# Author: Bob Bobson, 2012
#
# Please send feedback to bob@bob.com
#
# /etc/init.d/testdaemon
#
### BEGIN INIT INFO
# Provides: testdaemon
# Required-Start:
# Should-Start:
# Required-Stop:
# Should-Stop:
# Default-Start:  3 5
# Default-Stop:   0 1 2 6
# Short-Description: Test daemon process
# Description:    Runs up the test daemon process
### END INIT INFO

case "$1" in
  start)
    echo "Start monitoreo y carga inventario tlk"
    # Start the daemon
    python /usr/share/tlkdaemon/tlkdaemon.py start
    ;;
  stop)
    echo "Stop monitoreo y carga inventario tlk"
    # Stop the daemon
    python /usr/share/tlkdaemon/tlkdaemon.py stop
    ;;
  restart)
    echo "Restarting monitoreo y carga inventario tlk"
    python /usr/share/tlkdaemon/tlkdaemon.py restart
    ;;
  *)
    # Refuse to do other stuff
    echo "Usage: /etc/init.d/testdaemon.sh {start|stop|restart}"
    exit 1
    ;;
esac


exit 0

