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

//#define PNT_RA 5.450813061405754115 //b2045-16-Jun 21 2011
//#define PNT_DEC -0.28337325723894701157

//#define PNT_RA  5.2368626022705502 //PSR B1957+20 May 16 2013
//#define PNT_DEC 0.36375085679967373

//#define PNT_RA 5.0715791948861657 //PSR B1919+21 May 16 2013
//#define PNT_DEC 0.38240013618954616

//#define PNT_RA 5.1377213557725776 // PSR B1937+21 June 11 2013
//#define PNT_DEC 0.37467055774614433 

//#define PNT_RA 0.9338347801769575 // PSR B0329+54 June 29 2013
//#define PNT_DEC 0.953358324077975 

//#define PNT_RA 5.317237195986454 //PSR B2016+28 July 2 2013
//#define PNT_DEC 0.5010438856747761

//#define PNT_RA 5.071603193163381 //PSR B1919+21 July 2 2013
//#define PNT_DEC 0.382404451031308

#define PNT_RA 5.2368866005477654 //PSR B1957+20 July 2 2013
#define PNT_DEC 0.3637570139334238

#define NPOD 30 /*Number of baselines over which to iterate*/
#define EPOCH_START (0)
#define NEPOCH (6843) /*Number of lines in my timestamp file plus 1 - specifies the number of times we want antenna coordinates 4797 for 1957, 1197 for 1919, 6702 for 1937,4306 for 0329,2385 for 1919 on July 2,6843 for 1957 on July 2,716 for 2016 on July 2*/
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
  get_antenna_coords("data/coords60_2013.dat", coords, NPOD);

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
  
  printf("RAJ=%f radians DECJ=%f radians NEPOCH=%i iterations\n",PNT_RA,PNT_DEC,NEPOCH);

  /* first loop over time */
  for(iepoch=(tstart+T_CUTOFF);iepoch<(NEPOCH_READ-T_CUTOFF);iepoch++) {
          ha=RA_pt[iepoch]-GST[iepoch]-TEL_LON;
          chi=atan2(cos(TEL_LAT)*sin(ha),sin(TEL_LAT)*cos(PNT_DEC)-cos(TEL_LAT)*sin(PNT_DEC)*cos(ha));
	  // printf("iepoch=%i h=%f chi=%f\n",iepoch,ha,chi);

    tsize = NCROSS*iepoch;

     /* loop over baselines */
    for(bi=0;bi<1;bi++) //bi<1 => we want to delay wrt to one antenna, not all
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
	  thisu=ul*SPEED_OF_LIGHT;
	  thisv=vl*SPEED_OF_LIGHT;
	  thisw=wl*SPEED_OF_LIGHT;
	  fprintf(fp,"%d  %d  %f  %f  %f %f\n", bi,bj,thisu,thisv,thisw,chi);
	
      }
  }
  fclose(fp);
  return(0);
}
