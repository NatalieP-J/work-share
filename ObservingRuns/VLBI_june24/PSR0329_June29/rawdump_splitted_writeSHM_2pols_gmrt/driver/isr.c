//----------------------------------------------------------------------------
//  irq_handler()
//----------------------------------------------------------------------------
static int LocateBrdNum(struct pci_dev *dev_id)
{
  int x = 0;
  for (x=0; x < NumberOfBoards; x++) {
      if (dev_id == brds[x].ali_pci_dev) {
          return x;
      }
  }

//  printk("<aldriver::LocateBrdNum> ISR called with unknown dev_id\n");
  return -1;
}

//----------------------------------------------------------------------------
//  irq_handler()
//----------------------------------------------------------------------------
static void irq_handler(int irq, void *dev_id, struct pt_regs *regs)
{
  int BrdNum = LocateBrdNum(dev_id);
  int ics;
  int csr;
  ADBoard *brd = &brds[BrdNum];

  if (BrdNum >= 0) {
    ics = inl(brd->PLXaddr + PLX_INTCSR);

    // Clear the DMA Channel 0 Interrupt
    if (ics & PLX_DMA0I) {
//      printk("<aldriver::LocateBrdNum> Interrupt on Board %i\n", BrdNum);

      outb(1, brd->ioFPGAaddr + 0x34);       
      
      brd->NumInts++;
  
      csr = inb(brd->PLXaddr + PLX_DMACSR0);
      if (brd->AbortingDMA) {
        outb(PLX_CLEARINT, brd->PLXaddr + PLX_DMACSR0);
      } else {
        outb(csr | PLX_CLEARINT, brd->PLXaddr + PLX_DMACSR0);    
      }

      brd->fifo_status = (inb(brd->ioFPGAaddr + 0x81) & 0x80) >> 7;

      if (brd->CircleBuffer) {
          outl(0x789ABCDE, brds[BrdNum].ioFPGAaddr + 0x70);

        // Mark the Buffer Status for ping ponging buffers
       spin_lock(&brd->sl_status);
//       printk("<aldriver> Status is %02x, Ints %i, fifo %i\n", 
//               brd->BufferStatus, brd->NumInts, brd->fifo_status);
       if (brd->WhichBuffer == 0) {
         brd->WhichBuffer = 1;
         brd->BufferStatus |= 1;
       } else {
         brd->WhichBuffer = 0;
         brd->BufferStatus |= 2;
       }
       spin_unlock(&brd->sl_status);
      }

      brd->bottomhalf.data = dev_id;
      queue_task(&(brd->bottomhalf), &tq_immediate);
      mark_bh(IMMEDIATE_BH);
      
      outb(brd->BufferStatus << 1, brd->ioFPGAaddr + 0x34);
    }
  }
}

//----------------------------------------------------------------------------
//  bottom_half()
//----------------------------------------------------------------------------
static void bottom_half(void *data)
{
  int BrdNum = LocateBrdNum(data);
  int csr = inb(brds[BrdNum].PLXaddr + PLX_DMACSR0);  
  
#ifdef DEBUGGING
  printk("<aldriver::bottom_half> Called for Board %i\n", BrdNum);
#endif


  if (!brds[BrdNum].AbortingDMA && !(csr & 0x10)) {
    // Reset the DMA Timeout Timer
    ali_clr_dma_timer(BrdNum);
    ali_set_dma_timer(BrdNum, DMATimeout); 
  } else {  // DMA is Finished
     brds[BrdNum].AbortingDMA = 0;    
    ali_clr_dma_timer(BrdNum);
  }  
  
  brds[BrdNum].dma_status = CountDMADone(BrdNum); 
  
  // Ok, Wake up the dma wait queue
  if (waitqueue_active(&brds[BrdNum].dma_wq)) {
      wake_up_interruptible(&brds[BrdNum].dma_wq);
      brds[BrdNum].DebugCounter++;
  }
//  else
//    printk("<aldriver> bottom_half called with No dma_wq active.\n");
}
