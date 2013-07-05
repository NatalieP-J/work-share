#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "mpi.h"

#define M_PI 3.141592654

int main(int argc, char *argv[])
{
	FILE *fp;
	float theta, step_deg, step_rad;
	int myid, numprocs;
	
	MPI_Init(&argc,&argv);
	MPI_Comm_size(MPI_COMM_WORLD,&numprocs);
    	MPI_Comm_rank(MPI_COMM_WORLD,&myid);
	
	if(argc<2)
	{	fprintf(stderr,"Usage:%s<the resolution of phase in degree\n>", argv[0]);
		exit(-1);
	}
		
	step_deg = atof(argv[1]);
	fp = fopen("/mnt/raid0/jroy/fringe_table.fix.dat","w");
	step_rad = step_deg*M_PI/180;
	for(theta=0;theta<=2*M_PI;theta=theta+step_rad)
		fprintf(fp, "%hi %hi \n", (short int)(16384*cos(theta)), (short int)(16384*sin(theta)));
	fclose(fp);
	MPI_Finalize();
	return 0;
}
	
 	
