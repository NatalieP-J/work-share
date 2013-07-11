INCLUDE = /usr/src/linux-2.4.33-rc2/include
#INCLUDE = /usr/src/linux/include
CFLAGS = -O2 -Wall -D__KERNEL__ -I${INCLUDE}
TARGET = ali
SRC = aldriver.c 
CC = icc

all: .depend $(TARGET).o

ifeq (.depend,$(wildcard .depend))
include .depend
endif

$(TARGET).o: $(SRC:.c=.o)
	$(LD) -r $^ -o $@

clean:
	rm -f *.o *~ core .depend

depend .depend dep:
	$(CC) $(CFLAGS) -M *.c > $@

devices:
	mknod /dev/ali_main c 221 0
	mknod /dev/ali_brd1 c 221 1
	mknod /dev/ali_brd2 c 221 2
	mknod /dev/ali_brd3 c 221 3
	mknod /dev/ali_brd4 c 221 4
	chown root /dev/ali*
	chgrp users /dev/ali*
	chmod 666 /dev/ali*
