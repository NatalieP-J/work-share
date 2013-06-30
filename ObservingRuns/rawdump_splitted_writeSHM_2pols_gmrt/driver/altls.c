//****************************************************************************
//****************************************************************************
//
// Board Functions
//
//****************************************************************************
//****************************************************************************

static void initALTLS(int BrdNum)
{
  int fpga = brds[BrdNum].bar2start;

//  outb(0x10, fpga + ALTLS_GCR);
//  outb(0x00, fpga + ALTLS_GCR);
//  outb(0x80, fpga + ALTLS_SR);
}

//----------------------------------------------------------------------------
//  ALTLS_BrdAbortDMA
//----------------------------------------------------------------------------
static void ALTLS_BrdAbortDMA(int BrdNum)
{
  int fpga = brds[BrdNum].bar2start;
  
  outb(0x08, fpga + ALTLS_GCR);
  outb(0x00, fpga + ALTLS_GCR);
}

//----------------------------------------------------------------------------
//  Upload TLS RBF
//----------------------------------------------------------------------------
static int UploadTLSRBF(int BrdNum, char *data, long size)
{
  // Point to the Start of the FPGA Registers  
  int i;
  char tmp;
  int conf  = brds[BrdNum].bar3start + ALTLS_CONF_OFFSET;   
  int pdata = brds[BrdNum].bar2start + 0;

  printk("<UploadTLSRBF> Data: %08X, Size: %li\n",(int)data, size);
  
  // CONFIG to Low 
  outb(0, conf);
  udelay(8);
  
  if ( (inb(conf) & CONF_MASK) != CONF_START) {
    printk("<UploadTLSRBF> Upload Failed to Start\n");
    return 0;
  }
  
  // CONFIG to High
  outb(1, conf);
  udelay(40);

  for(i = 0; i < size; i++) {
    tmp = inb(conf);
    if ( (tmp & CONF_MASK) == CONF_NEXT) {
      udelay(2);
      outb(data[i], pdata);
      udelay(2);  
    } else {  // NOT NEXT
      printk("CONFIG not NEXT for byte %i during upload, %02X.\n",i,tmp);  
      return i;
    } 
  }

  udelay(10);  // Delay before access registers

  if ( (inb(conf) & CONF_MASK) == CONF_DONE) {
    brds[BrdNum].UploadStatus = 1;
    return size;
  } else if ( (inb(conf) & CONF_MASK) == CONF_ERROR)
    printk("Error occured during upload\n");  
  
  return 0;  
}
