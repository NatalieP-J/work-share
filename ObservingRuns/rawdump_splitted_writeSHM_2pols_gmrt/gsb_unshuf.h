/*
 *
 */

#ifndef  SOFTCORR_H
#define  SOFTCORR_H

#define  DasHeaderKey   1031
#define  DasBufferKey   1032

#include  <sys/ipc.h>
#include  <sys/shm.h>
#include  <sys/types.h>

#define  SpillBufSize  8*1024 // 8KB, for the spillover of the pointer for each chan. 
// which is equivalent of 245. uSec.
#define  DasBufferSize  2*32*1024*1024
#define  BoardDataSize  (DasBufferSize/2)
#define  MaxDataBlocks  8
#define  TimeSize       sizeof(double)
#define  DataSize       (BoardDataSize)

#define  ChanDataSize         8*1024*1024
#define  TimeSampleDataSize   4     // in bytes...

enum ChanOffset { ChAOffset=0, ChBOffset=1, ChCOffset=2, ChDOffset=3 };

enum BufFlag { _BufMarked=1, _BufReady=1<<1, _BufOverflow=1<< 2, _BufFinish=1<<3, _MaxBufs=100 };

typedef struct
{
  unsigned int flag, curBlock, curRecord, blockSize;
  int overFlow;
  double pcTime[MaxDataBlocks],dataTime[MaxDataBlocks];
  char data[ BoardDataSize*MaxDataBlocks];
} DataBuffer;

typedef struct
{
  unsigned int active, status;
  double pcTime, dataTime, refTime;
  struct timeval timestamp;
} DataHeader;

//DataHeader *dataHdr;
//DataBuffer *dataBuf;

#endif  // SOFTCORR_H
