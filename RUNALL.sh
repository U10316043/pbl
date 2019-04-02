#/bin/bash
nohup ./manage.py runserver_plus --cert server.crt 0.0.0.0:8080 > serverLOG.txt & nohup ./manage.py checkLimitTime > timeUpLog.txt &
