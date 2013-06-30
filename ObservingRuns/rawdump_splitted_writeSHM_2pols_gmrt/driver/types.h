#include <linux/wait.h>

#define UNI_MAJOR      221
#define MAX_MINOR 	 4
#define CONTROL_MINOR    0 

struct sgl_node {
   unsigned long pciaddr;
   unsigned long localaddr;
   unsigned long size;
   unsigned long next;
   // NEXT  31:4  Addr, 3 = DIR, 2 = INT, 1 = EOC, 0 = LOC
   // DIR = 1 LOC -> PCI
   //     = 0 PCI -> LOC
   // INT = 1 Interrupt on Transfer Finished
   // EOC = 1 this is end of chain
   // LOC = 1 Desc on PCI Bus
   //     = 0 Desc on LocalBus
};

typedef struct {
  char *BrdTypeStr;
  int BrdType;
  int UploadStatus;    // 0 = NotUploaded, 1 = Uploaded
  unsigned long PLXaddr;
  unsigned long ioFPGAaddr;
  unsigned long memFPGAaddr;
  unsigned char *vmemFPGAaddr;
  
  unsigned long dma_addr;
  unsigned long dma_size;
  unsigned long dma_status;
  unsigned long dma_transcnt;
  struct sgl_node *sgl;
  int sgl_size;
  int nodecnt;
  unsigned long brd_status;
  unsigned long fifo_status;
  int CircleBuffer;
  int NumIntsPerCircle;

  // PCI Resources
  int irq;
  unsigned int bar0start;  int bar0size;
  unsigned int bar1start;  int bar1size;
  unsigned int bar2start;  int bar2size; 
  unsigned int bar3start;  int bar3size; 
  unsigned int bar4start;  int bar4size; 
  unsigned int bar5start;  int bar5size; 
  
  struct tq_struct bottomhalf;

  struct pci_dev *ali_pci_dev;
  int AbortingDMA;
  //DECLARE_WAIT_QUEUE_HEAD(dma_wq);
  wait_queue_head_t dma_wq;
  struct timer_list timer_dma_timeout;

  int NumInts;
  int NumIntsBS;
  int DebugCounter;

  // Hold bits for ping ponging data buffers
  int BufferStatus;
  int WhichBuffer;
  spinlock_t sl_status;

} ADBoard;

