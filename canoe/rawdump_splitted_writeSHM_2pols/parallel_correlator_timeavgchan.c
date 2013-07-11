/* Program for raw voltage dumping -- Written by Jayanta Roy (Last modified on 31 aug 2007)
   Latest modification done on 06 dec 2007 -- Jayanta Roy
*/

#include <stdio.h>
#include <time.h>
#include <sys/timeb.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>
#include "mpi.h"
#include "omp.h"
#include <xmmintrin.h>
#include <emmintrin.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#include "parallel_correlator_timeavgchan.h"
#include "newcorr.h"
#include "gsb_unshuf.h"

#define decimate 1


static inline u_int64_t
rdtsc ()
{         u_int64_t d;
          __asm__ __volatile__ ("rdtsc" : "=&A" (d));
          return d;
}

static u_int64_t start_dcal, end_dcal;
static u_int64_t start_fft, end_fft;
static u_int64_t start_mac, end_mac;
static u_int64_t start_gather, end_gather;
static u_int64_t dcal_count = 0, fft_count = 0, mac_count = 0, gather_count = 0;

static int shmHId, shmBId;
static DataHeader *dataHdr;
static DataBuffer *dataBuf;

static MPI_Request request[2*NUM_PROCESSES*NNODECORR];
static MPI_Status status[2*NUM_PROCESSES*NNODECORR];
const int MPIWAITCHUNK=1;

int nrecv=0;
MPI_Comm MPI_COMM_GROUP1, MPI_COMM_G1, MPI_COMM_G2,MPI_COMM_G3,MPI_COMM_G4,MPI_COMM_G5,MPI_COMM_G6,MPI_COMM_G7,MPI_COMM_G8,MPI_COMM_G9,MPI_COMM_G10,MPI_COMM_G11,MPI_COMM_G12,MPI_COMM_G13,MPI_COMM_G14,MPI_COMM_G15;
MPI_Group group1, g0, g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, g12, g13, g14, g15;

void initialise (char *data) {
  shmHId = shmget(DasHeaderKey, sizeof( DataHeader ), 0644|IPC_CREAT );
  shmBId = shmget(DasBufferKey, sizeof( DataBuffer ), 0644|IPC_CREAT );

  if( shmHId < 0 || shmBId < 0 ) {
    perror("SHMGET");
    return;
  }

  dataHdr = (DataHeader *) shmat( shmHId, 0, 0 ); if (dataHdr == -1 ){perror("DataHdr");exit;}
  dataBuf = (DataBuffer *) shmat( shmBId, 0, 0 ); if (dataBuf == -1 ){perror("DataBuf");exit;}

  mlock( dataBuf, sizeof( DataBuffer ));
  dataBuf->flag = _BufMarked;
  dataBuf->curBlock = 0;
  dataBuf->curRecord = 0;
  dataBuf->blockSize = 0;
  dataBuf->overFlow = 0;
	dataHdr->refTime = 0.0;
}

void corr_driver(signed char *buffer, int dump_bit, int nint_corr, struct timeval timestamp, double *ch_freq, int w_buff, int fstop, float step, short int *phase)
	
{
//	__declspec(align(128)) static char rbuf[2][ACQ_LEN];
	__declspec(align(128)) static char rbuf[ACQ_LEN];

	struct timeb start, current;
	double sec;
	int numthreads, mythread, itarget, isource, nstep1,nstep2,nstep3,nstep4; 
	static int numprocs, myrank, numnode, ranknode;
	FILE *ftsamp;
	int i,j,k,l,m,io,iot,imp,acqcnt;
	int acq_chunk_offset, node_chunk_offset;
	static int firsttime=1, nchunk;
	static int nbuff = 0;
	static int iteration = 0;
	static int g_size = 2;
	static int nint = 0;
	static int rankcnt;
	static int r_array[(NUM_PROCESSES-1)*2];
	static float delay_t0[NCHAN*NUM_CORR],delay_ti[2][NCHAN*NUM_CORR],dd_t0[2][NCHAN*NUM_CORR];
	static float acq_chunktime, ffttime, pi, tstep, blocktime;
	static double tm0, time_sec = 0;
	struct tm* local_t;
	char time_string[40], *time_ptr;
	double mjd, time_ms, tm1, time_usec;
	int shuffle = 255;
	long buff_cnt=0;
        int fp1,fp2, fp3, fp4;
  	nchunk=ACQ_LEN/(decimate*CORRLEN);

	static unsigned int curBlock=0, curRec = 0;
 
	if (firsttime == 1) {
		MPI_Comm_size(MPI_COMM_WORLD,&numprocs);
		MPI_Comm_rank(MPI_COMM_WORLD,&myrank);

	#ifdef GATEHR
		r_array[0] = 0;
		r_array[1] = NUM_CORR;
		r_array[2] = NUM_CORR+1;
		r_array[3] = NUM_CORR+2;
		r_array[4] = NUM_CORR+3;
		r_array[5] = NUM_CORR+4;
		r_array[6] = NUM_CORR+5;
		r_array[7] = NUM_CORR+6;
		r_array[8] = NUM_CORR+7;
		r_array[17] = NUM_CORR;
		r_array[18] = NUM_CORR+2;
		r_array[19] = NUM_CORR+4;
		r_array[20] = NUM_CORR+6;
		r_array[25] = NUM_CORR;
		r_array[26] = NUM_CORR+4;

		MPI_Comm_group(MPI_COMM_WORLD,&g0);
		MPI_Group_incl(g0,(NUM_PROCESSES/2+1),&r_array[0],&group1);
		MPI_Group_incl(g0,g_size,&r_array[1],&g1);
		MPI_Group_incl(g0,g_size,&r_array[3],&g2);
		MPI_Group_incl(g0,g_size,&r_array[5],&g3);
		MPI_Group_incl(g0,g_size,&r_array[7],&g4);
                MPI_Group_incl(g0,g_size,&r_array[17],&g9);
                MPI_Group_incl(g0,g_size,&r_array[19],&g10);
                MPI_Group_incl(g0,g_size,&r_array[25],&g13);

		MPI_Comm_create(MPI_COMM_WORLD,group1,&MPI_COMM_GROUP1);
		MPI_Comm_create(MPI_COMM_WORLD,g1,&MPI_COMM_G1);
		MPI_Comm_create(MPI_COMM_WORLD,g2,&MPI_COMM_G2);
		MPI_Comm_create(MPI_COMM_WORLD,g3,&MPI_COMM_G3);
		MPI_Comm_create(MPI_COMM_WORLD,g4,&MPI_COMM_G4);
                MPI_Comm_create(MPI_COMM_WORLD,g9,&MPI_COMM_G9);
                MPI_Comm_create(MPI_COMM_WORLD,g10,&MPI_COMM_G10);
                MPI_Comm_create(MPI_COMM_WORLD,g13,&MPI_COMM_G13);
	#endif	

		blocktime = (((32*1.024*1.024)/4)/100)*3;
		acq_chunktime = blocktime/NUM_CORR;
                ffttime = acq_chunktime/(nchunk/NUM_CORR);  
		pi = 2.0*M_PI;		

#ifdef SHM_DUMP
		if (myrank>=numprocs/2){
			initialise(buffer);
		}
#endif
#ifdef RAW_DUMP
		if(myrank >= numprocs/2)	
//		fp1 = open("/mnt/a/jroy/raw_voltage1.dat", O_CREAT|O_TRUNC|O_WRONLY|O_SYNC,S_IRUSR|S_IWUSR);
//		fp2 = open("/mnt/b/jroy/raw_voltage2.dat", O_CREAT|O_TRUNC|O_WRONLY|O_SYNC,S_IRUSR|S_IWUSR);
//		fp3 = open("/mnt/c/jroy/raw_voltage3.dat", O_CREAT|O_TRUNC|O_WRONLY|O_SYNC,S_IRUSR|S_IWUSR);
//		fp4 = open("/mnt/d/jroy/raw_voltage4.dat", O_CREAT|O_TRUNC|O_WRONLY|O_SYNC,S_IRUSR|S_IWUSR);
		fp1 = open("/home/pen/raw_voltage1.dat", O_CREAT|O_TRUNC|O_WRONLY|O_SYNC,S_IRUSR|S_IWUSR);
		fp2 = open("/dev/null", O_CREAT|O_TRUNC|O_WRONLY|O_SYNC,S_IRUSR|S_IWUSR);
		fp3 = open("/dev/null", O_CREAT|O_TRUNC|O_WRONLY|O_SYNC,S_IRUSR|S_IWUSR);
		fp4 = open("/dev/null", O_CREAT|O_TRUNC|O_WRONLY|O_SYNC,S_IRUSR|S_IWUSR);
		if (fp1<0 || fp2<0 || fp3<0 || fp4<0) perror("open");
#endif		
	}
		ftime(&start);
                // NODE1 has to broadcast its timestamp
		        MPI_Bcast(&timestamp,sizeof(struct timeval),MPI_CHAR,0,MPI_COMM_WORLD);
		
		ftime(&current);
                sec = (((current.time - start.time) * 1000) + (current.millitm - start.millitm)) / 1000.0;
		

        MPI_Barrier(MPI_COMM_WORLD);

	if(firsttime > 0)  // IGNORE FIRST BUFFER
	{
		ftime(&start);
		if(myrank>=numprocs/2){
        	//#ifdef DEBUG
                	start_dcal = rdtsc ();
        	//#endif
		
		time_ms = timestamp.tv_usec/1000000.000;
		local_t = localtime(&timestamp.tv_sec);
		tm1 = local_t->tm_sec + local_t->tm_min*60 + local_t->tm_hour*3600 + time_ms;
		}

		ftime(&start);
		// NETWORK DATA SHARING IN TDM MODE
		if (myrank<numprocs/2){
//			itarget=(myrank)%(numprocs/2)+numprocs/2; //TDM transfer
			itarget=(myrank)+(numprocs/2); // node-to-node transfer
			MPI_Isend(buffer, ACQ_LEN, MPI_CHAR, itarget, 100, MPI_COMM_WORLD, request);
			MPI_Waitall(1,request,status);
		} else {
//			itarget=(NUM_CORR+myrank)%(numprocs/2);  // TDM Transfer
			itarget=(myrank)-(numprocs/2); // node-to-node transfer
//			MPI_Irecv(rbuf[iteration%2], ACQ_LEN, MPI_CHAR, itarget, 100, MPI_COMM_WORLD,request);
			MPI_Irecv(rbuf, ACQ_LEN, MPI_CHAR, itarget, 100, MPI_COMM_WORLD,request);
			MPI_Waitall(1,request,status);
//			fprintf(stdout, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>> curBlock = %d\n", curBlock);
		}

// Writing to SHM after all MPI_Waitall
		if (myrank>=numprocs/2){
			dataHdr->refTime = timestamp.tv_sec + timestamp.tv_usec/1e6;
			memcpy(&dataHdr->timestamp, &timestamp, sizeof(timestamp));
                        dataHdr->dataTime = dataHdr->refTime;
                        curBlock = curRec%MaxDataBlocks;
                        dataBuf->blockSize = DataSize;
                        memcpy(dataBuf->data+curBlock*DataSize, rbuf, BoardDataSize);
                        dataBuf->flag = BufReady;
                        dataBuf->curBlock = curBlock;
                        dataBuf->curRecord = curRec++;
                        //fprintf(stdout, ">>>>>>>>>>>> curBlock = %d\n", curBlock);
		}
		ftime(&current);
		sec = (((current.time - start.time) * 1000) + (current.millitm - start.millitm)) / 1000.0;
		//printf("$MPI %d %d 	%d ms\n",myrank, iteration,(int)(sec*1000));
	} // ignore first buffer
	iteration++;
	firsttime++;	
}
