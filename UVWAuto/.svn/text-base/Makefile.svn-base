# Object files, for use in linker
CC=gcc 
FC=ifort

NOVAS = novas-c201/novas.o novas-c201/novascon.o novas-c201/solsys3.o\
        novas-c201/readeph0.o
FOBJ = Gibbs.o
LOCALOBJ = read_data.o utils.o froutines.o beam_model.o sampling.o
OBJ = $(LOCALOBJ) $(FOBJ) $(NOVAS) -lm
COBJ = read_data.o utils.o beam_model.o sampling.o $(NOVAS) -lm
MOBJ = read_data.o utils.o beam_model.o $(NOVAS) -lm


# FLAGS:
#
# Aside from the 'obvious' (warning and optimization) flags
# there are several other options:
#
# CFLAGS:
#   -DSAVE_MEM = saves memory using NR style pointer references
#     (not official ANSI C, but works on $(CC))
#
# FFLAGS:
#   (none yet)
#
#CFLAGS = -g -O3 -Wall -DSAVE_MEM -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE=1 -D_LARGEFILE_SOURCE=1 #-openmp
CFLAGS = -g -O3 -Wall   -DSAVE_MEM -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE=1 -D_LARGEFILE_SOURCE=1 #-openmp
FFLAGS =  -save -g -O3 -Wall -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE=1 -D_LARGEFILE_SOURCE=1  #-openmp 

clean:
	rm *.o


test: *.c
# Fortran
	$(FC) Gibbs.f -c -o Gibbs.o $(FFLAGS)
# interfaces
	gcc froutines.c -c -o froutines.o $(CFLAGS)
# C
	$(CC) read_data.c -c -o read_data.o $(CFLAGS)
	$(CC) utils.c -c -o utils.o $(CFLAGS)
	$(CC) beam_model.c -c -o beam_model.o $(CFLAGS)
	$(CC) sampling.c -c -o sampling.o $(CFLAGS)
# main programs
	$(CC) test.c -c -o test.o $(CFLAGS)
	$(FC) -nofor_main test.o $(OBJ) -o test.x $(FFLAGS)

writeuvcoord.x: writeuvcoord.c utils.o read_data.o 
	$(CC) $(CFLAGS) $<  -o $@  $(NOVAS) utils.o read_data.o -lm -llapack  #-lg2c

uvbin: *.c
# Fortran
#	$(FC) Gibbs.f -c -o Gibbs.o $(FFLAGS)
# interfaces
#	gcc froutines.c -c -o froutines.o $(CFLAGS)
# C
	$(CC) read_data.c -c -o read_data.o $(CFLAGS)
	$(CC) utils.c -c -o utils.o $(CFLAGS)
	$(CC) beam_model.c -c -o beam_model.o $(CFLAGS)
#	$(CC) sampling.c -c -o sampling.o $(CFLAGS)
# main programs
	$(CC) -g3 uvbin.c -c -o uvbin.o $(CFLAGS)
	$(CC) -fpe0 -nofor_main uvbin.o $(MOBJ) -o uvbin.x $(FFLAGS)	

uvbin_norfi: *.c
# Fortran
	$(FC) Gibbs.f -c -o Gibbs.o $(FFLAGS)
# interfaces
	gcc froutines.c -c -o froutines.o $(CFLAGS)
# C
	$(CC) read_data.c -c -o read_data.o $(CFLAGS)
	$(CC) utils.c -c -o utils.o $(CFLAGS)
	$(CC) beam_model.c -c -o beam_model.o $(CFLAGS)
	$(CC) sampling.c -c -o sampling.o $(CFLAGS)
# main programs
	$(CC) -g3 uvbin_norfi.c -c -o uvbin_norfi.o $(CFLAGS)
	$(FC) -fpe0 -nofor_main uvbin_norfi.o $(OBJ) -o uvbin_norfi.x $(FFLAGS)	


src_params: *.c
# Fortran                                                                               
#	$(FC) Gibbs.f -c -o Gibbs.o $(FFLAGS)
# interfaces
	gcc froutines.c -c -o froutines.o $(CFLAGS)
# C                                                                                    
	$(CC) read_data.c -c -o read_data.o $(CFLAGS)
	$(CC) utils.c -c -o utils.o $(CFLAGS)
	$(CC) beam_model.c -c -o beam_model.o $(CFLAGS)
	$(CC) sampling.c -c -o sampling.o $(CFLAGS)
	$(CC) $(CFLAGS) -c src_params.c
# main programs
	$(CC) -openmp -g3 src_params.o $(MOBJ) -o src_params.x -lgsl -llapack -lgslcblas -lm -L/usr/lib -lg2c $(CFLAGS)
#	$(CC) -openmp -g3 src_params.o $(OBJ) -o src_params.x -L/opt/intel/mkl70/lib/64 -lmkl_lapack64 -lmkl_i2p -lm -L/usr/lib -lg2c $(CFLAGS)


uvcube: *.c
# Fortran
	$(FC) Gibbs.f -c -o Gibbs.o $(FFLAGS)
# interfaces
	gcc froutines.c -c -o froutines.o $(CFLAGS)
# C
	$(CC) read_data.c -c -o read_data.o $(CFLAGS)
	$(CC) utils.c -c -o utils.o $(CFLAGS)
	$(CC) beam_model.c -c -o beam_model.o $(CFLAGS)
	$(CC) sampling.c -c -o sampling.o $(CFLAGS)
# main programs
	$(CC) -g3 uvcube.c -c -o uvcube.o $(CFLAGS)
	$(FC) -fpe0 -nofor_main uvcube.o $(OBJ) -o uvcube.x $(FFLAGS)

wienermap: *.c
# Fortran
#	$(FC) Gibbs.f -c -o Gibbs.o $(FFLAGS)
# interfaces
#	gcc froutines.c -c -o froutines.o $(CFLAGS)
# C
	$(CC) read_data.c -c -o read_data.o $(CFLAGS)
	$(CC) utils.c -c -o utils.o $(CFLAGS)
	$(CC) beam_model.c -c -o beam_model.o $(CFLAGS)
# main programs
#	$(CC)   -mcmodel=medium  -shared-intel -fPIC -static -openmp -g   wienermap.c $(MOBJ) -o wienermap.x -lgsl /cita/d/scratch-month/tchang/liblapack.a -lgslcblas -lm -L/usr/lib64 -L /usr/lib/gcc/x86_64-redhat-linux/3.4.3/ -lg2c $(CFLAGS)
#	$(CC) -static -openmp -g -O2  wienermap.c $(MOBJ) -o wienermap.x -lgsl -L/opt/intel/mkl/9.0/lib/em64t/ -lmkl_lapack -lmkl_em64t -lgslcblas -lm -L/usr/lib -L /usr/lib/gcc/x86_64-redhat-linux/3.4.6/ -lg2c $(CFLAGS) 
	$(CC) -openmp -g3 wienermap.c $(MOBJ) -o wienermap.x -L/opt/intel/mkl70/lib/64 -lmkl_lapack64 -lmkl_i2p -lm -L/usr/lib -lg2c $(CFLAGS)

wienerfmap: wienerfmap.c
# C
	$(CC) read_data.c -c -o read_data.o $(CFLAGS)
	$(CC) utils.c -c -o utils.o $(CFLAGS)
	$(CC) beam_model.c -c -o beam_model.o $(CFLAGS)
# main programs
#	$(CC)   -mcmodel=medium  -shared-intel -fPIC -static -openmp -g   wienermap.c $(MOBJ) -o wienermap.x -lgsl /cita/d/scratch-month/tchang/liblapack.a -lgslcblas -lm -L/usr/lib64 -L /usr/lib/gcc/x86_64-redhat-linux/3.4.3/ -lg2c $(CFLAGS)
#	$(CC) -static -openmp -g -O3  wienerfmap.c $(MOBJ) -o wienerfmap.x -lgsl -L/opt/intel/mkl/9.0/lib/em64t/ -lmkl_lapack -lmkl_em64t -lgslcblas -lm -L/usr/lib -L /usr/lib/gcc/x86_64-redhat-linux/3.4.6/ -lg2c $(CFLAGS) 
	$(CC) -openmp -g3 wienerfmap.c $(MOBJ) -o wienerfmap.x -L/opt/intel/mkl70/lib/64 -lmkl_lapack64 -lmkl_i2p -lm -L/usr/lib -lg2c $(CFLAGS)

wiener_diffuse: *.c
# Fortran
	$(FC) Gibbs.f -c -o Gibbs.o $(FFLAGS)
# interfaces
	gcc froutines.c -c -o froutines.o $(CFLAGS)
# C
	$(CC) read_data.c -c -o read_data.o $(CFLAGS)
	$(CC) utils.c -c -o utils.o $(CFLAGS)
	$(CC) beam_model.c -c -o beam_model.o $(CFLAGS)
	$(CC) sampling.c -c -o sampling.o $(CFLAGS)
# main programs
	$(CC) -g3 wiener_diffuse.c -c -o wiener_diffuse.o $(CFLAGS)
	$(FC) -fpe0 -nofor_main wiener_diffuse.o $(OBJ) -o wiener_diffuse.x $(FFLAGS)

ptfg_sub: *.c
# Fortran
	$(FC) Gibbs.f -c -o Gibbs.o $(FFLAGS)
# interfaces
	gcc froutines.c -c -o froutines.o $(CFLAGS)
# C
	$(CC) read_data.c -c -o read_data.o $(CFLAGS)
	$(CC) utils.c -c -o utils.o $(CFLAGS)
	$(CC) beam_model.c -c -o beam_model.o $(CFLAGS)
	$(CC) sampling.c -c -o sampling.o $(CFLAGS)
# main programs
	$(CC) -g3 ptfg_sub.c -c -o ptfg_sub.o $(CFLAGS)
	$(FC) -fpe0 -nofor_main ptfg_sub.o $(OBJ) -o ptfg_sub.x $(FFLAGS)


fringestop:  *.c
# C
	$(CC) read_data.c -c -o read_data.o $(CFLAGS)
	$(CC) utils.c -c -o utils.o $(CFLAGS)
	$(CC) beam_model.c -c -o beam_model.o $(CFLAGS)
# main programs
	$(CC) -g3 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE=1 -D_LARGEFILE_SOURCE=1 fringestop.c -o fringestop.x $(MOBJ) 


fringestop64:  *.c
# C
	$(CC) read_data.c -c -o read_data.o $(CFLAGS)
	$(CC) utils.c -c -o utils.o $(CFLAGS)
	$(CC) beam_model.c -c -o beam_model.o $(CFLAGS)
# main programs
	$(CC) -g3 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE=1 -D_LARGEFILE_SOURCE=1 fringestop64.c -o fringestop64.x $(MOBJ)

fringestopall:  *.c
# C
	$(CC) read_data.c -c -o read_data.o $(CFLAGS)
	$(CC) utils.c -c -o utils.o $(CFLAGS)
	$(CC) beam_model.c -c -o beam_model.o $(CFLAGS)
# main programs
	$(CC) -g3 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE=1 -D_LARGEFILE_SOURCE=1 fringestopall.c -o fringestopall.x $(MOBJ) 

defringestop:  *.c
# C
	$(CC) read_data.c -c -o read_data.o $(CFLAGS)
	$(CC) utils.c -c -o utils.o $(CFLAGS)
	$(CC) beam_model.c -c -o beam_model.o $(CFLAGS)
# main programs
	$(CC) -g3 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE=1 -D_LARGEFILE_SOURCE=1 defringestop.c -o defringestop.x $(MOBJ) 


modelvis:  *.c
# C
	$(CC) read_data.c -c -o read_data.o $(CFLAGS)
	$(CC) utils.c -c -o utils.o $(CFLAGS)
	$(CC) beam_model.c -c -o beam_model.o $(CFLAGS)
# main programs
	$(CC) -g3 modelvis.c -o modelvis.x $(MOBJ)


cleanmap:  *.c
#C
	$(CC) -O3 -Wall cleanmap.c -o cleanmap.x -lm 


chopvis:  *.c
# C
	$(CC) read_data.c -c -o read_data.o $(CFLAGS)
	$(CC) utils.c -c -o utils.o $(CFLAGS)
	$(CC) beam_model.c -c -o beam_model.o $(CFLAGS)
# main programs
	$(CC) -g3 chopvis.c -o chopvis.x $(MOBJ)


zerovis:  *.c
# C
	$(CC) read_data.c -c -o read_data.o $(CFLAGS)
	$(CC) utils.c -c -o utils.o $(CFLAGS)
	$(CC) beam_model.c -c -o beam_model.o $(CFLAGS)
# main programs
	$(CC) -g3 zerovis.c -o zerovis.x $(MOBJ)

modelvisgain:  *.c
# C
	$(CC) read_data.c -c -o read_data.o $(CFLAGS)
	$(CC) utils.c -c -o utils.o $(CFLAGS)
	$(CC) beam_model.c -c -o beam_model.o $(CFLAGS)
# main programs
	$(CC) -g3 modelvisgain.c -o modelvisgain.x $(MOBJ)

avevis:  *.c
# C
	$(CC) read_data.c -c -o read_data.o $(CFLAGS)
	$(CC) utils.c -c -o utils.o $(CFLAGS)
	$(CC) beam_model.c -c -o beam_model.o $(CFLAGS)
# main programs
	$(CC) -g3 avevis.c -o avevis.x $(MOBJ)

reducevis:  *.c
# C
	$(CC) read_data.c -c -o read_data.o $(CFLAGS)
	$(CC) utils.c -c -o utils.o $(CFLAGS)
	$(CC) beam_model.c -c -o beam_model.o $(CFLAGS)
# main programs
	$(CC) -g3 reducevis.c -o reducevis.x $(MOBJ)

caldt:  *.c
# C
	$(CC) read_data.c -c -o read_data.o $(CFLAGS)
	$(CC) utils.c -c -o utils.o $(CFLAGS)
	$(CC) beam_model.c -c -o beam_model.o $(CFLAGS)
# main programs
	$(CC) -g3 caldt.c -o caldt.x $(MOBJ)


uvbin_model: *.c
# Fortran
	$(FC) Gibbs.f -c -o Gibbs.o $(FFLAGS)
# interfaces
	gcc froutines.c -c -o froutines.o $(CFLAGS)
# C
	$(CC) read_data.c -c -o read_data.o $(CFLAGS)
	$(CC) utils.c -c -o utils.o $(CFLAGS)
	$(CC) beam_model.c -c -o beam_model.o $(CFLAGS)
	$(CC) sampling.c -c -o sampling.o $(CFLAGS)
# main programs
	$(CC) -g3 uvbin_model.c -c -o uvbin_model.o $(CFLAGS)
	$(FC) -fpe0 -nofor_main uvbin_model.o $(OBJ) -o uvbin_model.x $(FFLAGS)

