//****************************************************************************
//****************************************************************************
//
// Board Functions
//
//****************************************************************************
//****************************************************************************
//----------------------------------------------------------------------------
//  Init8100
//----------------------------------------------------------------------------
static void initAL8100(int BrdNum)
{
}

//----------------------------------------------------------------------------
//  AL8100_SWTrig
//----------------------------------------------------------------------------
static void AL8100_SWTrigger(int BrdNum)
{
  int fpga = brds[BrdNum].bar2start;
  
  outb(0x00, fpga + AL8100_SWTRIGGER);
}
    
//----------------------------------------------------------------------------
//  AL8100_BrdAbortDMA
//----------------------------------------------------------------------------
static void AL8100_BrdAbortDMA(int BrdNum)
{
  int fpga = brds[BrdNum].bar2start;
  
  outb(0x01, fpga + AL8100_FSR);
  outb(0x00, fpga + AL8100_FSR);
}

//----------------------------------------------------------------------------
//  Upload8100RBF
//----------------------------------------------------------------------------
static int Upload8100RBF(int BrdNum, char *data, long size)
{
  // Point to the Start of the FPGA Registers  
  int i;
  char tmp;
  int FPGAaddr = brds[BrdNum].bar2start;   

  // Mark as Not Uploaded
  brds[BrdNum].UploadStatus = 0;  
  
  printk("<Upload8100RBF> Data: %08X, Size: %li\n",(int)data, size);
  
  // CONFIG to Low 
  outb(0, FPGAaddr + CONF_OFFSET);
  udelay(8);
  
  if ( (inb(FPGAaddr + CONF_OFFSET) & CONF_MASK) != CONF_START) {
    // Lets try one more time
    // CONFIG to Low 
    outb(0, FPGAaddr + CONF_OFFSET);
    udelay(8);
    if ( (inb(FPGAaddr + CONF_OFFSET) & CONF_MASK) != CONF_START) { 
      printk("Upload Failed to Start\n");
      return 0;
    }  
  }
  
  // CONFIG to High
  outb(1, FPGAaddr + CONF_OFFSET);
  udelay(40);

  for(i = 0; i < size; i++) {
    tmp = inb(FPGAaddr + CONF_OFFSET);
    if ( (tmp & CONF_MASK) == CONF_NEXT) {
      udelay(2);
      outb(data[i], FPGAaddr);
      udelay(2);  
    } else {  // NOT NEXT
      printk("CONFIG not NEXT for byte %i during upload, %02X.\n",i,tmp);  
      return i;
    } 
  }

  udelay(10);  // Delay before access registers

  if ( (inb(FPGAaddr + CONF_OFFSET) & CONF_MASK) == CONF_DONE) {
    brds[BrdNum].UploadStatus = 1;  
    return size;
  } else if ( (inb(FPGAaddr + CONF_OFFSET) & CONF_MASK) == CONF_ERROR) {
    printk("Error occured during upload\n");  
  }
  
  return 0;  
}

