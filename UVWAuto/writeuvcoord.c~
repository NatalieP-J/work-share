#include <stdlib.h>
#include <math.h>
#include <stdio.h>
#include <fenv.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

#include "constants.h"
#include "structures.h"
#include "routines.h"

//#define PNT_RA 2.163884  //B0809+74
//#define PNT_DEC 1.2995778

//#define PNT_RA 2.2580708  //B0834+06
//#define PNT_DEC 0.107214

//#define PNT_RA 5.8473282      // J2219
//#define PNT_DEC  0.83693676  // DEC  [rad]

#define PNT_RA 5.450813061405754115 //b2045-16-Jun 21 2011
#define PNT_DEC -0.28337325723894701157

#define NPOD 64
#define EPOCH_START (0)
#define NEPOCH (7)
#define NEPOCH_READ (NEPOCH+EPOCH_START)
#define DNEPOCH_CALIB (73)
#define DFREQ_CALIB  (512/32)
#define NBIN (512*4)
#define NF 64    //128
#define FBIN (32)
#define FBINSIZE (2)
#define BINSIZE (3.)  /* 1/radian without 2pi factor s.t the field of view is 30 deg */
#define T_CUTOFF 0
#define F_CUTOFF 0
#define round(x) ((x)>=0?(long long)((x)+0.5):(long long)((x)-0.5)) 
#define MAX(x,y) ((x>y)?x:y)
#define MIN(x,y) ((x<y)?x:y)
#define UVCUT 5
#define FREQCUT 0
#define SIGMACUT 3
#define FFTLEN (NF*2)
#define NCROSS (NPOD*(NPOD+1)/2 * FFTLEN)
#define NCROSSOUT (NPOD*(NPOD-1)/2 *FFTLEN/2)
#define NVIS (NEPOCH*NCROSS)

/* bin the visibilities into a 3-d (u,v,freq) 'horn' for wiener filtering
 * keep nf=4096 
 * -D CALIB for calibration
 */

int main(int argc, char *argv[]) {

  VIS v;
  ANTCOORDS coords[NPOD];
  int i,j, k, bi, bj, iepoch, df_index, dfbin;
  int fstart=0, nf=NF, tstart=EPOCH_START;  
  double TJD[NEPOCH_READ], GST[NEPOCH_READ];
  double RA_pt[NEPOCH_READ], Dec_pt[NEPOCH_READ];
  float datare[nf], dataim[nf], sigma[nf];
  double ul, vl, wl,ul1,vl1,chi,ha;
  double dt, dt_2pi, freq, FREQ0, FREQMIN;
  FILE *fp;
  double u_value=0., v_value=0.;
  double data_re=0.,data_im=0.;
  long long ncount=0;
  int fdinim, fdinre, fdsig, fdoutre, fdoutim;
  ssize_t size;


  if (argc != 3) { 
	fprintf(stdout,"usage: %s time.dat outfile.mat\n",argv[0]);
	exit(-1);
  }

  get_tjd_gst(argv[1], NEPOCH_READ, TJD, GST);
  get_antenna_coords("data/coords64_dec2.dat", coords, NPOD);

  int tsize,rsize,bindex;
  off_t offset;

  if ((fp=fopen(argv[2],"w")) == NULL)
   {
     printf("Unable to open for writing\n");
     exit(0);
   }

  for (iepoch=0;iepoch<NEPOCH_READ;iepoch++) {
    RA_pt[iepoch] = PNT_RA;
    Dec_pt[iepoch] = PNT_DEC;
  }


  /* first loop over time */
  for(iepoch=(tstart+T_CUTOFF);iepoch<(NEPOCH_READ-T_CUTOFF);iepoch++) {
          ha=RA_pt[iepoch]-GST[iepoch]-TEL_LON;
          chi=atan2(cos(TEL_LAT)*sin(ha),sin(TEL_LAT)*cos(PNT_DEC)-cos(TEL_LAT)*sin(PNT_DEC)*cos(ha));
//    printf("h=%f chi=%f\n",ha,chi);

    tsize = NCROSS*iepoch;

     /* loop over baselines */
    for(bi=0;bi<NPOD;bi++)
      for(bj=bi;bj<NPOD;bj++) {

	get_uv(RA_pt[iepoch]-GST[iepoch], Dec_pt[iepoch], bi, bj,
	       coords, &ul, &vl, &wl);

	FREQ0 = CORR_FREQ0 + CORR_DFREQ*(fstart+F_CUTOFF);
	FREQMIN = CORR_FREQ0 + CORR_DFREQ*(nf-F_CUTOFF);
	freq = CORR_FREQ0 + CORR_DFREQ*(fstart+F_CUTOFF);

	ncount=0;
	dfbin=0;
	float thisu, thisv, thisw, thisfreq;
	  thisfreq=CORR_FREQ0;
	  thisu=ul*thisfreq;
	  thisv=vl*thisfreq;
	  thisw=wl*thisfreq;
	  fprintf(fp,"%d  %d  %f  %f  %f %f\n", bi,bj,thisu,thisv,thisw,chi);
	
      }
  }
  fclose(fp);
  return(0);
}
