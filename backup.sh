mkdir backup
cp channels/* backup
rm -rf backup/excode.py
cp config/channels.txt backup
cp config/scripts.txt backup
tar -czf backup.tar.gz backup/*
rm -rf backup
