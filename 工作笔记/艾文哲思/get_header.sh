rm -rf /home/wzc/code/include/Comm/*
cp -r /home/tarsproto/XGame/Comm/* /home/wzc/code/include/Comm
cd /home/wzc/code/include/rpc/
if [ "$?" != 0 ]
then
	echo "enter dir failed!"
	exit -1
fi
rm -rf /home/wzc/code/include/rpc/*.h
FILES=$(find /home/tarsproto/XGame -name *.h)
for FILE in $FILES
do
	echo "Name:$FILE"
	TARGET=${FILE##*/}
	cat $FILE > $TARGET
done

# JFGame
cd /home/wzc/code/include/jfgame/
if [ "$?" != 0 ]
then
        echo "enter dir jfgame failed!"
        exit -1
fi
rm -rf /home/wzc/code/include/jfgame/*.h
FILES=$(find /home/tarsproto/JFGame -name *.h)
for FILE in $FILES
do
        echo "Name:$FILE"
        TARGET=${FILE##*/}
        cat $FILE > $TARGET
done



