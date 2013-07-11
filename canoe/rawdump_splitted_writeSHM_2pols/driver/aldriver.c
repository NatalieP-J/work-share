//-----------------------------------------------------------------------------
//title: Acquisition Logic A/D Board Kernel Driver
//version: Linux 0.1
//date: July 2002             
//designer: Michael Wyrick                                                
//programmer: Michael Wyrick                                               
//platform: Linux 2.4.x
//language: GCC 2.95 and 3.0
//module: aldriver
//-----------------------------------------------------------------------------
//  Purpose: Provide a Kernel Driver to Linux for the ALI A/D Boards
//  Docs:                                  
//    This driver supplies an interface to the raw Registers on the boards.
//    in is upto a user library or program to determine what to do with those
//    registers.
//-----------------------------------------------------------------------------
// RCS:
// $Id: aldriver.c,v 1.8 2005/11/08 21:09:09 mwyrick Exp $
// $Log: aldriver.c,v $
// Revision 1.8  2005/11/08 21:09:09  mwyrick
// Added Localbus Theshold to 60 Clocks from 12 clock to increase DMA Rate
//
// Revision 1.7  2005/11/04 15:52:52  mwyrick
// Max DMA Speed Testing, Got 190MB/S on 64/66 bus with 4108.
//
// Revision 1.6  2005/01/17 22:21:16  mwyrick
// Removed some debug Printk
//
// Revision 1.5  2004/12/29 20:12:57  mwyrick
// Working well with two acq buffers.  Debugging off
//
// Revision 1.4  2004/12/23 18:52:35  mwyrick
// Now has board enum in the main control number
//
// Revision 1.3  2004/12/23 14:52:19  mwyrick
// Multi Board is working.
// DMA Buffer is set to 10 Meg
//
// Revision 1.2  2004/12/22 19:29:06  mwyrick
// Working on Multi Board
//
// Revision 1.1.1.1  2004/12/16 14:27:28  mwyrick
// ALLinux 2004
//
// Revision 1.2  2004/10/06 13:53:13  mwyrick
// Added Proper Support for AL212.
// Changed the ResetPLX to reload the config from the EEPROM
// Made DMA Buffer size 8 Megs, there seems to be a problem when its
// larger than that.
//
// Revision 1.1.1.1  2004/04/29 19:20:14  mwyrick
// AcqLog Linux Driver
//
// Revision 1.58  2004/03/18 17:34:41  mwyrick
// Interm but AL4108 loads
//
// Revision 1.57  2004/03/18 17:12:59  mwyrick
// Added Shared Interrupt Support
//
// Revision 1.56  2004/03/18 16:12:10  mwyrick
// Check in before starting work on the AL4108
//
// Revision 1.55  2002/12/24 19:15:53  mwyrick
// Debugging the AL1G.  Works with First BCB version of ALScope
//
// Revision 1.54  2002/12/24 00:03:51  mwyrick
// Interm
//
// Revision 1.53  2002/12/18 21:50:37  mwyrick
// IOCTL_GET_BRDTYPE
//
// Revision 1.52  2002/12/18 14:50:06  mwyrick
// Working uploads to AL1G
//
// Revision 1.51  2002/12/17 19:46:08  mwyrick
// Started Adding AL1G Support
//
// Revision 1.50  2002/12/09 21:25:54  mwyrick
// Added RBF Upload Status to ioctl
//
// Revision 1.49  2002/11/27 21:14:23  mwyrick
// New memory Structure, DumpFPGA, DumpPLX
// IOCTL_COLLECTDATA
//
// Revision 1.48  2002/11/27 15:32:17  mwyrick
// Good Working Version
//
// Revision 1.47  2002/11/19 21:22:27  mwyrick
// Working with AL8100 to download Waveforms
//
// Revision 1.46  2002/11/05 19:29:45  mwyrick
// Interm Checkin
//
// Revision 1.45  2002/10/24 17:34:14  mwyrick
// First version working with new ALLOC_DMA_BUFFER code
//
// Revision 1.44  2002/10/24 17:20:17  mwyrick
// Added New IOCTL for NumInts and CircleBuffer Mode
//
// Revision 1.43  2002/10/24 17:01:48  mwyrick
// Working with new IOCTL Names
//
// Revision 1.42  2002/10/24 15:59:48  mwyrick
// Clean up under way
// NO boards except ALTLS
//
// Revision 1.41  2002/10/23 21:48:40  mwyrick
// Working
//
// Revision 1.40  2002/10/23 21:17:34  mwyrick
// Working on DELL
//
// Revision 1.39  2002/10/23 15:14:06  mwyrick
// Added AbortDMA on Unload
// Changed TINTS to Every 64 nodes
// Start Recording in DoDMA not initBRD
//
// Revision 1.38  2002/10/22 21:43:54  mwyrick
// Working with TLS board with real data
//
// Revision 1.37  2002/10/22 18:23:26  mwyrick
// First Working version with ALtls
//
// Revision 1.36  2002/10/21 18:54:42  mwyrick
// Working in the new ALTLS board
//
// Revision 1.35  2002/10/21 18:19:32  mwyrick
// Working Checkin
//
// Revision 1.34  2002/10/18 19:45:13  mwyrick
// Added CLR_CNTREG and fix damn spaces at end of vmem.*
//
// Revision 1.33  2002/10/16 22:59:37  mwyrick
// First Really Good Full DMA transfer BUT
// BUT
// BUT
// DEMAND MODE IS OFF. SO DON'T USE THIS ONE
//
// Revision 1.32  2002/10/16 21:18:28  mwyrick
// Hmm
//
// Revision 1.31  2002/10/16 20:59:47  mwyrick
// Changed Names on PLX Registers
//
// Revision 1.30  2002/10/16 20:09:05  mwyrick
// Testing out some stuff, don;t use this
//
// Revision 1.29  2002/10/16 16:41:35  mwyrick
// *** empty log message ***
//
// Revision 1.28  2002/10/16 16:06:29  mwyrick
// ----------------------------------------------------------------
// Moved All Files into one compile so every function can be Static
// ----------------------------------------------------------------
//
// Revision 1.27  2002/10/16 15:54:35  mwyrick
// Semi-Working SGL
//
// Revision 1.26  2002/10/16 13:38:36  mwyrick
// Testing new vmalloc buffer with DMA
// New BuildSGL function
//
// Revision 1.25  2002/10/16 13:20:38  mwyrick
// Added a few comments
// Made SGL size 10 pages (2560 nodes)
//
// Revision 1.24  2002/10/15 16:14:33  mwyrick
// Testout new Vmem functions
//
// Revision 1.23  2002/10/15 16:05:12  mwyrick
// Test out vmalloc type stuff
//
// Revision 1.22  2002/10/15 14:45:47  mwyrick
// Testing larger Block
//
// Revision 1.21  2002/10/14 19:18:42  mwyrick
// Working SGL
//
// Revision 1.20  2002/10/14 18:05:13  mwyrick
// Starting SGL mode
//
// Revision 1.19  2002/10/14 16:00:27  mwyrick
// Have mmap working
// Have Blocking/NonBlocking IO Working
//
// Revision 1.18  2002/10/12 00:38:37  mwyrick
// Giving up on mmap for the night.
//
// Revision 1.17  2002/10/11 22:19:05  mwyrick
// Renamed DMA.* to dma.*
//
// Revision 1.16  2002/10/11 20:57:57  mwyrick
// Starting to use waitqueues
//
// Revision 1.15  2002/10/11 20:49:36  mwyrick
// Moved Fops struct into fops.h
// Added $revision into version string
//
// Revision 1.14  2002/10/11 20:46:17  mwyrick
// Moved file operations to fops.c
//
// Revision 1.13  2002/10/11 20:27:52  mwyrick
// Added headers.h, isr.c and isr.h
//
// Revision 1.12  2002/10/11 20:19:49  mwyrick
// DMA Interrupts are now working
//
// Revision 1.11  2002/10/11 19:23:28  mwyrick
// working on getting interrupts to work
//
// Revision 1.10  2002/10/11 19:17:43  mwyrick
// Moved out proc functions to proc.c
//
// Revision 1.9  2002/10/11 19:11:09  mwyrick
// Working on Interrupts
//
// Revision 1.8  2002/10/11 18:30:56  mwyrick
// Added FPGAaddr and PLXaddr to brd struct
//
// Revision 1.7  2002/10/11 18:20:41  mwyrick
// More Registers
//
// Revision 1.6  2002/10/11 15:01:11  mwyrick
// Moved upload code to seperate files
//
// Revision 1.5  2002/10/11 14:45:14  mwyrick
// DMA is Working in Simple Mode
// New Structure of Makefile
// Driver is now named ali.o
// new DMA.c file that contains the code for DMA transfers
// .depend works in new Makefile
// PLX constants put into plx9054.h
//
// Revision 1.4  2002/10/10 18:20:21  mwyrick
// Seems that first DMA is now working
//
// Revision 1.3  2002/10/10 18:04:01  mwyrick
// More DMA Changes
//
// Revision 1.2  2002/10/10 17:06:14  mwyrick
// Starting the DMA Stuff
//
// Revision 1.1.1.1  2002/08/21 13:37:36  mwyrick
// Acquisition Logic Linux Driver
//
//-----------------------------------------------------------------------------
#define MODULE

//#define DEBUGGING

#define DMA_DEMAND

static char Version[] = "0.971 2005NOV03";

#include <linux/config.h>
#include <linux/version.h>

#ifdef CONFIG_MODVERSIONS
  #define MODVERSIONS
  #include <linux/modversions.h>
#endif

#include <linux/module.h>
#include <linux/types.h>
#include <linux/errno.h>
#include <linux/proc_fs.h>
#include <linux/pci.h>
#include <linux/poll.h>
#include <linux/delay.h>
#include <linux/vmalloc.h>
#include <linux/interrupt.h>
#include <linux/sched.h>
#include <linux/spinlock.h>
#include <asm/pgtable.h>
#include <asm/io.h>
#include <asm/uaccess.h>

#define UNI_MAJOR      221
#define MAX_MINOR 	     4
#define CONTROL_MINOR    0 

//----------------------------------------------------------------------------
// Include Our Header Files
//----------------------------------------------------------------------------
#include "plx9054.h"
#include "types.h"
#include "aldriver.h"
#include "proc.h"
#include "isr.h"
#include "al8100.h"
#include "al8100_funcs.h"
#include "al1g.h"
#include "al1g_funcs.h"
#include "al212.h"
#include "al212_funcs.h"
#include "al4108.h"
#include "al4108_funcs.h"
#include "dma.h"
#include "fops.h"
#include "vmem.h"
#include "timers.h"

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Acquisition Logic");
MODULE_DESCRIPTION("AL8100, AL1G, AL212, AL4108 A/D Board Kernel Driver");

static ADBoard brds[MAX_MINOR+1];        

static int DMATimeout = 1;

// This holds the number of A/D boards that we are using
static int NumberOfBoards = 0;

//----------------------------------------------------------------------------
// Include Other Source Files
//   We do this so all our functions can be static.  If they are not,
//   then they will be public in the Kernel namespace and we don't want that
//----------------------------------------------------------------------------
#include "al8100.c"
#include "al1g.c"
#include "al212.c"
#include "al4108.c"
#include "dma.c"
#include "fops.c"
#include "isr.c"
#include "proc.c"
#include "timers.c"
#include "vmem.c"

//----------------------------------------------------------------------------
// Vars and Defines
//----------------------------------------------------------------------------

//-----------------------------------------------------------------------------
// Function   : resetPLX
// Inputs     : void
// Outputs    : void
// Description: 
// Remarks    : 
// History    : 
//-----------------------------------------------------------------------------
static void resetPLX(int BrdNum)
{
  int result = inl(brds[BrdNum].PLXaddr + PLX_CNTRL);
  
  outl(result | 0x40000000, brds[BrdNum].PLXaddr + PLX_CNTRL);
  int clred = result & ~0x40000000;
  outl(clred, brds[BrdNum].PLXaddr + PLX_CNTRL);  

  udelay(500);
  
  // Load the Configurations Registers
  // Reload happens on Rising Edge
  clred = result & ~0x20000000;
  outl(clred, brds[BrdNum].PLXaddr + PLX_CNTRL);   
  outl(result | 0x20000000, brds[BrdNum].PLXaddr + PLX_CNTRL);
  udelay(500);  
  outl(clred, brds[BrdNum].PLXaddr + PLX_CNTRL);  
}

//-----------------------------------------------------------------------------
// Function   : cleanup_module
// Inputs     : void
// Outputs    : void
// Description: 
// Remarks    : 
// History    : 
//-----------------------------------------------------------------------------
void cleanup_module(void)
{ 
  int x;
         
  for(x=0; x < NumberOfBoards; x++) {
    printk("Cleaning up Board %i\n", x);
    AbortDMA(x);
    free_irq(brds[x].irq, brds[x].ali_pci_dev);  
    free_dma_buffer(x);
    pci_release_regions(brds[x].ali_pci_dev);
  }
    
  unregister_proc();
  unregister_chrdev(UNI_MAJOR, "AcqLog");
}

//----------------------------------------------------------------------------
//  Build a Board Object from the Pci Device
//----------------------------------------------------------------------------
int CreateBoard(int BrdNum, struct pci_dev *pci_dev, char *brdstr, int BrdType) {
  char vstr[80];
  char p[80];
  int result;
  int x, i;
  u8 val;
  ADBoard *brd = &brds[BrdNum];

  brd->ali_pci_dev = pci_dev;
  brd->BrdTypeStr  = brdstr;                                     
  brd->BrdType     = BrdType;                                       

  init_waitqueue_head(&(brd->dma_wq));

      // Display PCI Registers  
  printk("  Board Number %02i\n", BrdNum);
  printk("  Vendor = %04X  Device = %04X\n", pci_dev->vendor, pci_dev->device);
  printk("  Class = %08X\n", pci_dev->class);
  sprintf(vstr, "  Board Type is %s\n", brd->BrdTypeStr);
  printk(vstr);   

  printk("<aldriver> PCI Config Registers\n");  
  for(x=0;x<256;x+=16) {
    sprintf(p,"<aldriver> %02X: ",x); printk(p);
    for(i=0;i<16;i++) {
      pci_read_config_byte(pci_dev, x + i, &val);
      sprintf(p, "%02X ", val); printk(p);
      if (i == 7) {
        printk("- "); 
      }  
    }
    printk("\n");
  }    
  
  brd->bar0start = pci_resource_start(pci_dev,0);
  brd->bar0size  = pci_resource_len(pci_dev,0);    
  brd->bar1start = pci_resource_start(pci_dev,1);
  brd->bar1size  = pci_resource_len(pci_dev,1);

  brd->bar2start = pci_resource_start(pci_dev,2);
  brd->bar2size  = pci_resource_len(pci_dev,2);

  brd->bar3start = pci_resource_start(pci_dev,3);
  brd->bar3size  = pci_resource_len(pci_dev,3);

  brd->bar4start = pci_resource_start(pci_dev,4);
  brd->bar4size  = pci_resource_len(pci_dev,4);
  brd->bar5start = pci_resource_start(pci_dev,5);
  brd->bar5size  = pci_resource_len(pci_dev,5);

  brd->PLXaddr     = brds[BrdNum].bar1start;
  brd->ioFPGAaddr  = brds[BrdNum].bar2start;
  brd->memFPGAaddr = brds[BrdNum].bar3start;
 
  brd->irq = pci_dev->irq;

  result = request_irq(brd->irq, 
                       irq_handler, 
                       SA_INTERRUPT | SA_SHIRQ, 
                       brd->BrdTypeStr, 
                       pci_dev);

  if (result) {
    printk("  aldriver: can't get assigned pci irq vector %02X\n", brd->irq);
  } 
     
  if (pci_enable_device(pci_dev)) {
    printk(KERN_ERR "pci_enable_device failed!\n");
    free_irq(brd->irq, NULL);
    return -EIO;
  }

  if (pci_request_regions(pci_dev,"ALIDriver")) {
    printk(KERN_ERR "pci_request_regions Failed.\n");
    free_irq(brd->irq, NULL);
    return 1;
  }
  
  // Map the FPGA into kernel Virtual Memory
  brd->vmemFPGAaddr = ioremap(brd->bar3start, 256);

  brd->dma_addr = 0;
  brd->dma_size = 0;
  brd->sgl      = 0;
  brd->sgl_size = 0;
  brd->CircleBuffer     = 1;
  brd->NumIntsPerCircle = 64;
  brd->bottomhalf.routine = bottom_half;

  brd->NumInts = 0;
  brd->NumIntsBS = 0;
  brd->DebugCounter = 0;

  alloc_dma_buffer(BrdNum, ALDMABUFFERSIZE);

  resetPLX(BrdNum);  

  // Program DMA Threshold Registers
  outl(0x00000000, brds[BrdNum].PLXaddr + PLX_DMATHR);
  outl(0x0021003b, brds[BrdNum].PLXaddr + PLX_MARBR);  // max local burst 60 clocks
  
  brd->sl_status = SPIN_LOCK_UNLOCKED;
  brd->BufferStatus = 0;
  brd->WhichBuffer  = 0;

  // Enable PLX PCI Interrupts
  outl(0x00040100, brds[BrdNum].PLXaddr + PLX_INTCSR);

  outb(5, brd->ioFPGAaddr + 0x32);
  
  ali_init_dma_timer(BrdNum);
  return 0;
}

//----------------------------------------------------------------------------
//  init_module()
//----------------------------------------------------------------------------
int init_module(void)
{
  char vstr[80];
  int result;

  struct pci_dev *ali_pci_dev = NULL;
  int BrdNum = 0;
  int x;
  
  // Clear out the Board Types in the Brd Array
  for(x = 0; x < 4; x++)
    brds[x].BrdType = BRDTYPE_NONE;
  
  sprintf(vstr,"Acquisition Logic A/D Driver %s\n",Version);
  printk(vstr);
  printk("  Copyright 2002-2005, Acquisition Logic\n");
 
  // LookFor AL8100
  while((ali_pci_dev = pci_find_device(PCI_VENDOR_ID_ACQUISITIONLOGIC,
                                     PCI_DEVICE_ID_ACQUISITIONLOGIC_AL8100, 
                                     ali_pci_dev)) != NULL) {
    result = CreateBoard(BrdNum, ali_pci_dev, "AL8100", BRDTYPE_AL8100);
    if (result) {
        return result;
    }
    BrdNum++;  
  } 
  
  while ((ali_pci_dev = pci_find_device(PCI_VENDOR_ID_ACQUISITIONLOGIC,
                                     PCI_DEVICE_ID_ACQUISITIONLOGIC_AL1G, 
                                     ali_pci_dev)) != NULL) {
    result = CreateBoard(BrdNum, ali_pci_dev, "AL1G", BRDTYPE_AL1G);
    if (result) {
        return result;
    }
    BrdNum++;  
  } 
  
  while ((ali_pci_dev = pci_find_device(PCI_VENDOR_ID_ACQUISITIONLOGIC,
                                     PCI_DEVICE_ID_ACQUISITIONLOGIC_AL500, 
                                     ali_pci_dev)) != NULL) {
    result = CreateBoard(BrdNum, ali_pci_dev, "AL500", BRDTYPE_AL500);
    if (result) {
        return result;
    }
    BrdNum++;  
  } 
  
  while ((ali_pci_dev = pci_find_device(PCI_VENDOR_ID_ACQUISITIONLOGIC,
                                     PCI_DEVICE_ID_ACQUISITIONLOGIC_AL1G4, 
                                     ali_pci_dev)) != NULL) {
    result = CreateBoard(BrdNum, ali_pci_dev, "AL1G4", BRDTYPE_AL1G4);
    if (result) {
        return result;
    }
    BrdNum++;  
  } 
  
  while ((ali_pci_dev = pci_find_device(PCI_VENDOR_ID_ACQUISITIONLOGIC,
                                     PCI_DEVICE_ID_ACQUISITIONLOGIC_AL5004, 
                                     ali_pci_dev)) != NULL) {
    result = CreateBoard(BrdNum, ali_pci_dev, "AL5004", BRDTYPE_AL5004);
    if (result) {
        return result;
    }
    BrdNum++;  
  }
  
  while ((ali_pci_dev = pci_find_device(PCI_VENDOR_ID_ACQUISITIONLOGIC,
                                     PCI_DEVICE_ID_ACQUISITIONLOGIC_AL212, 
                                     ali_pci_dev)) != NULL) {
    result = CreateBoard(BrdNum, ali_pci_dev, "AL212", BRDTYPE_AL212);
    if (result) {
        return result;
    }
    BrdNum++;  
  } 
  
  while ((ali_pci_dev = pci_find_device(PCI_VENDOR_ID_ACQUISITIONLOGIC,
                                     PCI_DEVICE_ID_ACQUISITIONLOGIC_AL2124, 
                                     ali_pci_dev)) != NULL) {
   result = CreateBoard(BrdNum, ali_pci_dev, "AL2124", BRDTYPE_AL2124);
   if (result) {
     return result;
   }
   BrdNum++;  
  } 
  
  while ((ali_pci_dev = pci_find_device(PCI_VENDOR_ID_ACQUISITIONLOGIC,
                                     PCI_DEVICE_ID_ACQUISITIONLOGIC_AL4108, 
                                     ali_pci_dev)) != NULL) {
    result = CreateBoard(BrdNum, ali_pci_dev, "AL4108", BRDTYPE_AL4108);
    if (result) {
      return result;
    }
    BrdNum++;  
  } 
  
  while ((ali_pci_dev = pci_find_device(PCI_VENDOR_ID_ACQUISITIONLOGIC,
                                     PCI_DEVICE_ID_ACQUISITIONLOGIC_AL2114, 
                                     ali_pci_dev)) != NULL) {
    result = CreateBoard(BrdNum, ali_pci_dev, "AL2114", BRDTYPE_AL2114);
    if (result) {
      return result;
    }
    BrdNum++;  
  } 
  
  while ((ali_pci_dev = pci_find_device(PCI_VENDOR_ID_ACQUISITIONLOGIC,
                                     PCI_DEVICE_ID_ACQUISITIONLOGIC_ALTLS, 
                                     ali_pci_dev)) != NULL) {
    result = CreateBoard(BrdNum, ali_pci_dev, "ALTLS", BRDTYPE_ALTLS);
    if (result) {
        return result;
    }
    BrdNum++;  
  } 
  
  while ((ali_pci_dev = pci_find_device(0x10B5, 0x9054, ali_pci_dev)) != NULL) {
    printk("<ALDRIVER> Found a board with the Generic PLX PCI ID.\n");
    printk("<ALDRIVER> This board needs to have a Valid ALI PCI ID on it.\n");
    printk("<ALDRIVER> Contact Acquisition Logic to have the board reprogrammed.\n");
    return 1;
  } 

  if (BrdNum == 0) {
    printk(" Acquisition Logic Board(s) Not Found on the PCI Bus.\n");
    return 1;
  }                                      

  NumberOfBoards = BrdNum;

  if (register_chrdev(UNI_MAJOR, "AcqLog", &ali_fops)) {
    printk("  Error getting Major Number for Drivers\n");
    //free_irq(brds[BrdNum].irq, NULL);
    return(1);
  } else {
    printk("  Acquisition Logic Driver Loaded.\n"); 
  }

  register_proc();

  return 0;
}

