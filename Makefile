.PHONY: all link unlink

#because of xunfei library, should found lib in the path of exe

all:

MSC_LIB_PATH=/usr/local/lib
PYTHON_BIN_PATH=/usr/bin
current_path=$(shell pwd)
link:
	ln -sf ${MSC_LIB_PATH}/libmsc.so ${PYTHON_BIN_PATH}/libmsc.so
	ln -sf ${MSC_LIB_PATH}/libamr.so ${PYTHON_BIN_PATH}/libamr.so
	ln -sf ${MSC_LIB_PATH}/libamr_wb.so ${PYTHON_BIN_PATH}/libamr_wb.so
	ln -sf ${MSC_LIB_PATH}/libspeex.so ${PYTHON_BIN_PATH}/libspeex.so

unlink:
	rm -rf ${PYTHON_BIN_PATH}/libmsc.so
	rm -rf ${PYTHON_BIN_PATH}/libamr.so
	rm -rf ${PYTHON_BIN_PATH}/libamr_wb.so
	rm -rf ${PYTHON_BIN_PATH}/libspeex.so
