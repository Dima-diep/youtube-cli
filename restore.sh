echo 'Write file (current dir is youtube-cli)'
read file
mv $file channels
cd channels
tar -xzf $file
rm -rf $file
cd backup
mv *.py ..
mv *.txt ../../config
cd ..
rm -rf backup
cd ..
