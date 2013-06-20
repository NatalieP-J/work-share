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

static MPI_Request request[2*NUM_PROCESSES*NNODECORR];
static MPI_Status status[2*NUM_PROCESSES*NNODECORR];
const int MPIWAITCHUNK=1;

int nrecv=0;
MPI_Comm MPI_COMM_GROUP1, MPI_COMM_G1, MPI_COMM_G2,MPI_COMM_G3,MPI_COMM_G4,MPI_COMM_G5,MPI_COMM_G6,MPI_COMM_G7,MPI_COMM_G8,MPI_COMM_G9,MPI_COMM_G10,MPI_COMM_G11,MPI_COMM_G12,MPI_COMM_G13,MPI_COMM_G14,MPI_COMM_G15;
MPI_Group group1, g0, g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, g12, g13, g14, g15;

void corr_driver(signed char *buffer, int dump_bit, int nint_corr, struct timeval timestamp, double *ch_freq, int w_buff, int fstop, float step, short int *phase)
	
{	register __m128i r0,r1,r2,r3,r4,r5,r6,r7;
        register __m128 r11,r22,r33,r44,r55,r66,r77,r88;

	__declspec(align(128)) static char rbuf[2][ACQ_LEN];
	__declspec(align(128)) static char muxbuf[2][NCHAN][ACQ_LEN/NCHAN];
	__declspec(align(128)) static char obuf[2][NCHAN][ACQ_LEN/NCHAN];

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
	long long total_power; // total power buffer
	double total_power_out; 
  	nchunk=ACQ_LEN/(decimate*CORRLEN);

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

#ifdef RAW_DUMP
		if(myrank >= numprocs/2)	
		  //fp1 = open("/mnt/a/jroy/raw_voltage1.dat", O_CREAT|O_WRONLY|O_SYNC,S_IRUSR|S_IWUSR);
		  //fp2 = open("/mnt/b/jroy/raw_voltage2.dat", O_CREAT|O_WRONLY|O_SYNC,S_IRUSR|S_IWUSR);
		  //fp3 = open("/mnt/c/jroy/raw_voltage3.dat", O_CREAT|O_WRONLY|O_SYNC,S_IRUSR|S_IWUSR);
		  //fp4 = open("/mnt/d/jroy/raw_voltage4.dat", O_CREAT|O_WRONLY|O_SYNC,S_IRUSR|S_IWUSR);
                fp1 = open("/home/njones/raw_voltage1.dat", O_CREAT|O_TRUNC|O_WRONLY|O_SYNC,S_IRUSR|S_IWUSR);
                //fp1 = open("/mnt/data0/pen/raw_voltage.dat", O_CREAT|O_TRUNC|O_WRONLY|O_SYNC,S_IRUSR|S_IWUSR);
                //fp2 = open("/home/pen/raw_voltage2.dat", O_CREAT|O_TRUNC|O_WRONLY|O_SYNC,S_IRUSR|S_IWUSR);
                //fp1 = open("/dev/null", O_CREAT|O_TRUNC|O_WRONLY|O_SYNC,S_IRUSR|S_IWUSR);
                fp2 = open("/dev/null", O_CREAT|O_TRUNC|O_WRONLY|O_SYNC,S_IRUSR|S_IWUSR);
                //fp2 = open("/mnt/data2/pen/raw_voltage2.dat", O_CREAT|O_TRUNC|O_WRONLY|O_SYNC,S_IRUSR|S_IWUSR);
                fp3 = open("/dev/null", O_CREAT|O_TRUNC|O_WRONLY|O_SYNC,S_IRUSR|S_IWUSR);
                //fp3 = open("/mnt/data3/pen/raw_voltage3.dat", O_CREAT|O_TRUNC|O_WRONLY|O_SYNC,S_IRUSR|S_IWUSR);
                fp4 = open("/dev/null", O_CREAT|O_TRUNC|O_WRONLY|O_SYNC,S_IRUSR|S_IWUSR);
                if (fp1<0 || fp2<0 || fp3<0 || fp4<0) perror(" raw voltage open");

#endif		
	}
		
		ftime(&start);
                // NODE1 has to broadcast its timestamp
		        MPI_Bcast(&timestamp,sizeof(struct timeval),MPI_CHAR,0,MPI_COMM_WORLD);
		
		ftime(&current);
                sec = (((current.time - start.time) * 1000) + (current.millitm - start.millitm)) / 1000.0;
		

        MPI_Barrier(MPI_COMM_WORLD);

	if(firsttime > 2)  // IGNORE FIRST BUFFER
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
	//OPENMP threading loop start here
	
	omp_set_num_threads(6);	
	#pragma omp parallel default(shared) private(start,current)
	#pragma omp sections nowait (signed char)rbuf[1-iteration%2][i]
	{       
	{	ftime(&start);
			
		// NETWORK DATA SHARING IN TDM MODE
		
		if (myrank<numprocs/2){
                itarget=(myrank)%(numprocs/2)+numprocs/2;
                MPI_Isend(buffer, ACQ_LEN*4/4, MPI_CHAR, itarget, 100, MPI_COMM_WORLD, request);
                MPI_Waitall(1,request,status);
		}
                else{
                itarget=(NUM_CORR+myrank)%(numprocs/2);
                MPI_Irecv(rbuf[iteration%2], ACQ_LEN*4/4, MPI_CHAR, itarget, 100, MPI_COMM_WORLD,request);
                MPI_Waitall(1,request,status);
		}

		// Demultiplexing on quad core received data
		if (myrank>=numprocs/2){
			
		for (acqcnt=0;acqcnt<nchunk;acqcnt++)
        	{
			imp=omp_get_thread_num();
                	acq_chunk_offset=acqcnt*CORRLEN;

        	for(j=0;j<NCHAN*FFTLEN;j+=64)
        	{
                        r0 = _mm_load_si128(&rbuf[1-iteration%2][acq_chunk_offset+j]);
                        r1 = _mm_load_si128(&rbuf[1-iteration%2][acq_chunk_offset+j+16]);
                        r2 = _mm_load_si128(&rbuf[1-iteration%2][acq_chunk_offset+j+32]);
                        r3 = _mm_load_si128(&rbuf[1-iteration%2][acq_chunk_offset+j+48]);

                        r4 = _mm_slli_epi32(r0,24);       // ...A1 0 0 0
                        r5 = _mm_slli_epi32(r1,24);       // ...A1 0 0 0
                        r4 = _mm_srai_epi32(r4,16);       // shiftimg in sign bit to avoid saturation for negative nos
                        r5 = _mm_srai_epi32(r5,16);
                        r4 = _mm_packs_epi32(r4,r5);

                        r4 = _mm_srai_epi16(r4,8);

                        r5 = _mm_slli_epi32(r2,24);       // ...A1 0 0 0
                        r6 = _mm_slli_epi32(r3,24);       // ...A1 0 0 0
                        r5 = _mm_srai_epi32(r5,16);       // shiftimg in sign bit to avoid saturation for negative nos
                        r6 = _mm_srai_epi32(r6,16);
                        r5 = _mm_packs_epi32(r5,r6);

                        r5 = _mm_srai_epi16(r5,8);

                        r4 = _mm_packs_epi16(r4,r5);
                        _mm_store_si128(&muxbuf[1-iteration%2][0][acqcnt*FFTLEN+j/4],r4);

                        r4 = _mm_srli_epi32(r0,8);       // ...A1 A4 A3 A2
                        r4 = _mm_slli_epi32(r4,24);       // ...A2 0 0 0
                        r5 = _mm_srli_epi32(r1,8);       // ...A1 0 0 0
                        r5 = _mm_slli_epi32(r5,24);       // ...A1 0 0 0
                        r4 = _mm_srai_epi32(r4,16);       // shiftimg in sign bit to avoid saturation for negative nos
                        r5 = _mm_srai_epi32(r5,16);
                        r4 = _mm_packs_epi32(r4,r5);
                        r4 = _mm_srai_epi16(r4,8);

                        r5 = _mm_srli_epi32(r2,8);       // ...A1 A4 A3 A2
                        r5 = _mm_slli_epi32(r5,24);       // ...A1 0 0 0
                        r6 = _mm_srli_epi32(r3,8);       // ...A1 A4 A3 A2
                        r6 = _mm_slli_epi32(r6,24);       // ...A1 0 0 0
                        r5 = _mm_srai_epi32(r5,16);       // shiftimg in sign bit to avoid saturation for negative nos
			r6 = _mm_srai_epi32(r6,16);
                        r5 = _mm_packs_epi32(r5,r6);
                        r5 = _mm_srai_epi16(r5,8);

                        r4 = _mm_packs_epi16(r4,r5);
                        _mm_store_si128(&muxbuf[1-iteration%2][1][acqcnt*FFTLEN+j/4],r4);

                        r4 = _mm_srli_epi32(r0,16);       // ...A1 A4 A3 A2
                        r4 = _mm_slli_epi32(r4,24);       // ...A2 0 0 0
                        r5 = _mm_srli_epi32(r1,16);       // ...A1 0 0 0
                        r5 = _mm_slli_epi32(r5,24);       // ...A1 0 0 0
                        r4 = _mm_srai_epi32(r4,16);       // shiftimg in sign bit to avoid saturation for negative nos
                        r5 = _mm_srai_epi32(r5,16);
                        r4 = _mm_packs_epi32(r4,r5);
                        r4 = _mm_srai_epi16(r4,8);

                         r5 = _mm_srli_epi32(r2,16);       // ...A1 A4 A3 A2
                        r5 = _mm_slli_epi32(r5,24);       // ...A1 0 0 0
                        r6 = _mm_srli_epi32(r3,16);       // ...A1 A4 A3 A2
                        r6 = _mm_slli_epi32(r6,24);       // ...A1 0 0 0
                        r5 = _mm_srai_epi32(r5,16);       // shiftimg in sign bit to avoid saturation for negative nos
                        r6 = _mm_srai_epi32(r6,16);
                        r5 = _mm_packs_epi32(r5,r6);
                        r5 = _mm_srai_epi16(r5,8);

                        r4 = _mm_packs_epi16(r4,r5);
                        _mm_store_si128(&muxbuf[1-iteration%2][2][acqcnt*FFTLEN+j/4],r4);

                        r4 = _mm_srli_epi32(r0,24);       // ...A1 A4 A3 A2
                        r4 = _mm_slli_epi32(r4,24);       // ...A2 0 0 0
                        r5 = _mm_srli_epi32(r1,24);       // ...A1 0 0 0
                        r5 = _mm_slli_epi32(r5,24);       // ...A1 0 0 0
                        r4 = _mm_srai_epi32(r4,16);       // shiftimg in sign bit to avoid saturation for negative nos
                        r5 = _mm_srai_epi32(r5,16);
                        r4 = _mm_packs_epi32(r4,r5);
                        r4 = _mm_srai_epi16(r4,8);

                        r5 = _mm_srli_epi32(r2,24);       // ...A1 A4 A3 A2
                        r5 = _mm_slli_epi32(r5,24);       // ...A1 0 0 0
                        r6 = _mm_srli_epi32(r3,24);       // ...A1 A4 A3 A2
                        r6 = _mm_slli_epi32(r6,24);       // ...A1 0 0 0
                        r5 = _mm_srai_epi32(r5,16);       // shiftimg in sign bit to avoid saturation for negative nos
                        r6 = _mm_srai_epi32(r6,16);
                        r5 = _mm_packs_epi32(r5,r6);
                        r5 = _mm_srai_epi16(r5,8);

                        r4 = _mm_packs_epi16(r4,r5);
                        _mm_store_si128(&muxbuf[1-iteration%2][3][acqcnt*FFTLEN+j/4],r4);
        } // NCHAN*FFTLEN (j)
        } // acqcnt
	} // myrank
                ftime(&current);
		sec = (((current.time - start.time) * 1000) + (current.millitm - start.millitm)) / 1000.0;
  		printf("$MPI %d %d 	%d ms\n",myrank, iteration,(int)(sec*1000));
		//#endif
	}
	
	#pragma omp section
	{ 	ftime(&start);	
		if(myrank>=numprocs/2){
		
		omp_set_num_threads(2);
	ftime(&start);

	
	if(dump_bit == 4){
	#pragma omp parallel for default(shared) private(imp,i,acqcnt,acq_chunk_offset) schedule(dynamic,1)
	for (acqcnt=0;acqcnt<nchunk/NCHAN;acqcnt++)
        {
	      imp=omp_get_thread_num();
              acq_chunk_offset=acqcnt*CORRLEN;

	for(i=0; i<NCHAN*FFTLEN; i=i+2)
        {     muxbuf[iteration%2][0][i+acq_chunk_offset]=((muxbuf[iteration%2][0][i+acq_chunk_offset] & 0xf0)>>4) & 0x0f;
              muxbuf[iteration%2][1][i+acq_chunk_offset]=((muxbuf[iteration%2][1][i+acq_chunk_offset] & 0xf0)>>4) & 0x0f;
              muxbuf[iteration%2][2][i+acq_chunk_offset]=((muxbuf[iteration%2][2][i+acq_chunk_offset] & 0xf0)>>4) & 0x0f;
              muxbuf[iteration%2][3][i+acq_chunk_offset]=((muxbuf[iteration%2][3][i+acq_chunk_offset] & 0xf0)>>4) & 0x0f;
        
              muxbuf[iteration%2][0][i+acq_chunk_offset+1]=((muxbuf[iteration%2][0][i+acq_chunk_offset+1] & 0xf0));
              muxbuf[iteration%2][1][i+acq_chunk_offset+1]=((muxbuf[iteration%2][1][i+acq_chunk_offset+1] & 0xf0));
              muxbuf[iteration%2][2][i+acq_chunk_offset+1]=((muxbuf[iteration%2][2][i+acq_chunk_offset+1] & 0xf0));
              muxbuf[iteration%2][3][i+acq_chunk_offset+1]=((muxbuf[iteration%2][3][i+acq_chunk_offset+1] & 0xf0));
		
              obuf[1-iteration%2][0][buff_cnt]=muxbuf[iteration%2][0][i+acq_chunk_offset] | muxbuf[iteration%2][0][i+acq_chunk_offset+1];
              obuf[1-iteration%2][1][buff_cnt]=muxbuf[iteration%2][1][i+acq_chunk_offset] | muxbuf[iteration%2][1][i+acq_chunk_offset+1];
              obuf[1-iteration%2][2][buff_cnt]=muxbuf[iteration%2][2][i+acq_chunk_offset] | muxbuf[iteration%2][2][i+acq_chunk_offset+1];
              obuf[1-iteration%2][3][buff_cnt]=muxbuf[iteration%2][3][i+acq_chunk_offset] | muxbuf[iteration%2][3][i+acq_chunk_offset+1];
              buff_cnt++;
        }
	} // acqcnt
	} // dump_bit
	/*
	if(dump_bit == 2){
	for(i=0; i<ACQ_LEN; i=i+4)
	{     rbuf[1-iteration%2][i]=((rbuf[1-iteration%2][i] & 0xc0)>>6) & 0x03;
              rbuf[1-iteration%2][i+1]=((rbuf[1-iteration%2][i+1] & 0xc0)>>4) & 0x0c;
              rbuf[1-iteration%2][i+2]=((rbuf[1-iteration%2][i+2] & 0xc0)>>2) & 0x30;
              rbuf[1-iteration%2][i+3]=((rbuf[1-iteration%2][i+3] & 0xc0));
              rbuf[1-iteration%2][buff_cnt]=rbuf[1-iteration%2][i] | rbuf[1-iteration%2][i+1] | rbuf[1-iteration%2][i+2] |rbuf[1-iteration%2][i+3];
              buff_cnt++;
	}
	write(fp1,rbuf[1-iteration%2],ACQ_LEN/16);
        write(fp1,(rbuf[1-iteration%2]+ACQ_LEN/16),ACQ_LEN/16);
        write(fp1,(rbuf[1-iteration%2]+2*ACQ_LEN/16),ACQ_LEN/16);
        write(fp1,(rbuf[1-iteration%2]+3*ACQ_LEN/16),ACQ_LEN/16);
	}

	if(dump_bit == 8){
	write(fp1,rbuf[1-iteration%2],ACQ_LEN/4);
        write(fp1,(rbuf[1-iteration%2]+ACQ_LEN/4),ACQ_LEN/4);
        write(fp1,(rbuf[1-iteration%2]+2*ACQ_LEN/4),ACQ_LEN/4);
        write(fp1,(rbuf[1-iteration%2]+3*ACQ_LEN/4),ACQ_LEN/4);
	}
	*/

	ftime(&current);
        sec = (((current.time - start.time) * 1000) + (current.millitm - start.millitm)) / 1000.0;
	printf("#PACKING %d %d 				%d ms\n",myrank, iteration,(int)(sec*1000));
	} //mpyrank if
        } // omp sections


	// FIRST THREAD
	#pragma omp section
        {       int icount,ilen;
		ftime(&start);
                if(myrank>=numprocs/2){

	        ftime(&start);
		ilen=ACQ_LEN; //removed division by 4
        	//write(fp1,obuf[iteration%2][3],ACQ_LEN/8);
        	icount=write(fp1,rbuf[1-iteration%2],ilen);
		if (icount != ilen) fprintf(stderr,"only wrote %d of %d bytes\n",icount,ilen);

//	ftsamp=fopen("/mnt/a/jroy/timestamp_voltage.dat","a");
	ftsamp=fopen("/home/njones/timestamp_voltage.dat","a"); // IMPORTANT PATH
        if (ftsamp == NULL) perror("ftsamp fopen");
        strftime (time_string, sizeof (time_string), "%Y %m %d %H %M %S", local_t);
	//printf("TIME VALUE %s \n", time_string);
	fprintf(ftsamp,"%s %lf \n", time_string, time_ms);
	fclose(ftsamp);
	ftime(&current);
        sec = (((current.time - start.time) * 1000) + (current.millitm - start.millitm)) / 1000.0;
        printf("#WRITE %d %d            			%d ms\n",myrank, iteration,(int)(sec*1000));

	} //mpyrank if
	} // omp sections

	 #pragma omp section
        {       ftime(&start);
                if(myrank>=numprocs/2){
		  
                ftime(&start);
                //write(fp2,obuf[iteration%2][2],ACQ_LEN/8);
        	//write(fp2,rbuf[1-iteration%2]+ACQ_LEN/4,ACQ_LEN/400);
		for ((i=0;i<ACQ_LEN;i++)){
		  int t = (signed char)rbuf[1-iteration%2][i];
		  total_power += t*t;
		}
		total_power_out = total_power;
		total_power_out /= ACQ_LEN;
		write(ftotal,&total_power_out,sizeof(double));
	ftime(&current);
        sec = (((current.time - start.time) * 1000) + (current.millitm - start.millitm)) / 1000.0;
        printf("#WRITE %d %d                                    %d ms\n",myrank, iteration,(int)(sec*1000));

        } //mpyrank if
        } // omp sections

	 #pragma omp section
        {       ftime(&start);
                if(myrank>=numprocs/2){

                ftime(&start);
                //write(fp3,obuf[iteration%2][2],ACQ_LEN/8);
        	//write(fp3,rbuf[1-iteration%2]+2*ACQ_LEN/4,ACQ_LEN/400);

        ftime(&current);
        sec = (((current.time - start.time) * 1000) + (current.millitm - start.millitm)) / 1000.0;
        printf("#WRITE %d %d                                    %d ms\n",myrank, iteration,(int)(sec*1000));

        } //mpyrank if
        } // omp sections

	 #pragma omp section
        {       ftime(&start);
                if(myrank>=numprocs/2){

                ftime(&start);
                //write(fp4,obuf[iteration%2][2],ACQ_LEN/8);
        	//write(fp4,rbuf[1-iteration%2]+3*ACQ_LEN/4,ACQ_LEN/4000);

        ftime(&current);
        sec = (((current.time - start.time) * 1000) + (current.millitm - start.millitm)) / 1000.0;
        printf("#WRITE %d %d                                    %d ms\n",myrank, iteration,(int)(sec*1000));

        } //mpyrank if
        } // omp sections

	
        } // main parallel loop
	} // ignore first buffer
        iteration++;
 
    	firsttime++;	
}	
