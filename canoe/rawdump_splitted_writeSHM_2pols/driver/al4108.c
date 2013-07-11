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
// $Id: al4108.c,v 1.2 2004/12/22 19:29:06 mwyrick Exp $
// $Log: al4108.c,v $
// Revision 1.2  2004/12/22 19:29:06  mwyrick
// Working on Multi Board
//
// Revision 1.1.1.1  2004/12/16 14:27:28  mwyrick
// ALLinux 2004
//
// Revision 1.1.1.1  2004/04/29 19:20:14  mwyrick
// AcqLog Linux Driver
//
// Revision 1.2  2004/03/18 17:57:31  mwyrick
// Uploading RBF Is working
//
// Revision 1.1  2004/03/18 17:34:41  mwyrick
// Interm but AL4108 loads
//
//
//-----------------------------------------------------------------------------

//----------------------------------------------------------------------------
//  Init4108
//----------------------------------------------------------------------------
static void initAL4108(int BrdNum)
{
}

//----------------------------------------------------------------------------
//  AL4108_SWTrigger
//----------------------------------------------------------------------------
static void AL4108_SWTrigger(int BrdNum)
{
  int fpga = brds[BrdNum].bar2start; 
  int tmp = inb(fpga + 0x94);
  
  outb(tmp | 0x80, fpga + 0x94);
}

//----------------------------------------------------------------------------
//  AL4108_BrdAbortDMA
//----------------------------------------------------------------------------
static void AL4108_BrdAbortDMA(int BrdNum)
{
  unsigned char tmp;
  int fpga = brds[BrdNum].bar2start; 

  tmp = inb(fpga + 0x80);   
   
  outb(tmp | 0x08, fpga + 0x80);
  outb(tmp, fpga + 0x80);
}

//----------------------------------------------------------------------------
//  Upload4108RBF
//----------------------------------------------------------------------------
#define AL4108_CONF_OFFSET	0xFC

#define AL4108_CONF_MASK	0x0D
#define AL4108_CONF_START	0x00
#define AL4108_CONF_NEXT	0x05
#define AL4108_CONF_ERROR	0x01
#define AL4108_CONF_DONE	0x0D

static int Upload4108RBF(int BrdNum, char *data, long size)
{
// Point to the Start of the FPGA Registers  
  int i, pdata, conf;
  char tmp;
  
  pdata = brds[BrdNum].bar2start + 0;
  conf  = brds[BrdNum].bar2start + AL4108_CONF_OFFSET;
       
  printk("<Upload4108RBF> pdata: %08X, conf: %08X\n", pdata, conf);       
  printk("<Upload4108RBF> Data: %08X, Size: %li\n",(int)data, size);
            
  // CONFIG to Low 
  outb(0, conf);
  udelay(8);
       
  tmp = inb(conf);                  
  if ( (tmp & AL4108_CONF_MASK) != AL4108_CONF_START) {
    printk("<Upload4108RBF> Upload Failed to Start. %02X \n", (unsigned char)tmp);
    return 0;
  }
                                 
  // CONFIG to High
  outb(1, conf);
  udelay(40);
                                        
  for(i = 0; i < size; i++) {
    tmp = inb(conf);
    if ( (tmp & AL4108_CONF_MASK) == AL4108_CONF_NEXT) {
      outb(data[i], pdata);
      udelay(3);  
    } else {  // NOT NEXT
      udelay(10);  // Delay before access registers
      if ( (inb(conf) & AL4108_CONF_MASK) == AL4108_CONF_DONE) {
        brds[BrdNum].UploadStatus = 1;
        return size;
      } else {
        printk("CONFIG not NEXT for byte %i during upload, %02X.\n",i,tmp);  
        return i;
      }
    } 
  }
                                                                                          
  udelay(10);  // Delay before access registers
  if ( (inb(conf) & AL4108_CONF_MASK) == AL4108_CONF_DONE) {
    brds[BrdNum].UploadStatus = 1;
    return size;
  } else if ( (inb(conf) & AL4108_CONF_MASK) == AL4108_CONF_ERROR)
    printk("Error occured during upload\n");  
    
  return 0;  
}
                                                                                                            
