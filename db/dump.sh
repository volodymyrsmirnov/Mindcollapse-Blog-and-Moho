#!/bin/bash
cd /home/smirnov/www/mindcollapse.com/db
mysqldump -usmirnov_dump -pblogdump --tab --skip-extended-insert --lock-tables=false --ignore-table=smirnov_mindcollapse.auth_user --ignore-table=smirnov_mindcollapse.django_session smirnov_mindcollapse > db.sql
git commit -m "Database dump $(dare)"
git push
