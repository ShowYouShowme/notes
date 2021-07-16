#!/bin/bash
#usage:将TARGET设置为makefile里面的TARGET
echo "Invoke auto compile copy and reboot service Script"
TARGET=${1}
rm -f ~/bin/XGame.${TARGET}/bin/${TARGET}
if [ $? != 0 ]
then
	echo "删除${TARGET}失败!"
        exit -127
fi
cp ./${TARGET} ~/bin/XGame.${TARGET}/bin/
if [ $? != 0 ]
then
	echo "Copy ${TARGET}失败!"
        exit -127
fi
TARGETPID=$(ps -ef | grep XGame.${TARGET} | awk '{if($6 == "?") print $2}')
echo ${TARGETPID}
kill -9 ${TARGETPID}
