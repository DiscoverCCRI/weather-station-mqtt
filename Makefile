CC		= gcc
SQLFLG	= `mysql_config --cflags --libs`
BIN		= bin
FILES	= scrub.c

compile:
	${CC} ${FILES} -o ${BIN} ${SQLFLG}

clean:
	rm ${BIN}

