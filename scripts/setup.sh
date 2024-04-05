#!/usr/bin/env bash
# Bruk dette skriptet for fyrstegongsoppsett

check_log="Støtte på ein feil, sjekk setup.log for info."
log_path=`pwd`/log-setup.log

echo "Aktiverer venv..."
python3 -m venv ./venv && \
  source venv/bin/activate && \
  pip3 install -r requirements.txt > $log_path
if [[ $? == 0 ]]
then
  rm $log_path
  echo "Installerte requirements."
else
  echo $check_log
  exit 1
fi

#if [[ ! -f "../../configs/travel-planner.json" ]]
#then
#  echo "Hugs å laste opp config-fila til ../configs/travel-planner.json "
#  exit 1
#else
#  echo "Config-fil oppdaga."
#fi

echo "Lastar inn data frå databasen..."
python3 manage.py migrate > $log_path &2> $log_path
#python3 manage.py loaddata dummydata.json >> $log_path

if [[ $? == 0 ]]
then
  rm $log_path
  echo "Lasta inn data."
else
  echo $check_log
  exit 1
fi

echo "Kopierer statiske filer..."
python manage.py collectstatic --no-input > $log_path &2> $log_path
#python3 manage.py loaddata dummydata.json >> $log_path

if [[ $? == 0 ]]
then
  rm $log_path
  echo "Kopiert."
else
  echo $check_log
  exit 1
fi
