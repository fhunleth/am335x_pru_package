INCDIR_APP_LOADER?=../../../app_loader/include
PASM?=../../../utils/pasm_2

binaries=simple.bin
all: simple.bin

%.bin : %.p
	${PASM} -I${INCDIR_APP_LOADER} -V3 -b $<

clean:
	rm ${binaries}
