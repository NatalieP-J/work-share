static void resetPLX(int);

static void ali_dma_timeout(unsigned long __data)
{
  int csr;
  char s[255];
  int BrdNum = (int)__data;
  
  brds[BrdNum].brd_status |= 0x01;  

  csr = inb(brds[BrdNum].PLXaddr + PLX_DMACSR0);

#ifdef DEBUGGING
  printk("<alidriver::ali_dma_timeout> DMA Timeout.\n"); 
  PrintFPGARegisters(BrdNum);
#endif

  if (csr & 0x10) {
    printk("<alidriver::ali_dma_timeout> DMA Timeout with DMA Finished\n"); 
    sprintf(s,"<alidriver::ali_dma_timeout> Ints=%i, IntsBS=%i\n", brds[BrdNum].NumInts, brds[BrdNum].NumIntsBS);
    printk(s);
  }

  if ((brds[BrdNum].BrdType == BRDTYPE_AL8100) || 
      (brds[BrdNum].BrdType == BRDTYPE_AL212) ||
      (brds[BrdNum].BrdType == BRDTYPE_AL2124))
    resetPLX(BrdNum);
    
  if (waitqueue_active(&brds[BrdNum].dma_wq))
    wake_up_interruptible(&brds[BrdNum].dma_wq);
}

static void ali_set_dma_timer(int BrdNum, int time)
{
  brds[BrdNum].timer_dma_timeout.expires = jiffies + time * HZ;
  add_timer(&brds[BrdNum].timer_dma_timeout);
}

static void ali_clr_dma_timer(int BrdNum)
{
  del_timer(&brds[BrdNum].timer_dma_timeout);
}

static void ali_init_dma_timer(int BrdNum)
{
  init_timer(&brds[BrdNum].timer_dma_timeout);
  brds[BrdNum].timer_dma_timeout.function = ali_dma_timeout;
  brds[BrdNum].timer_dma_timeout.data = BrdNum;
}

