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
// $Id: al212.c,v 1.2 2004/12/22 19:29:06 mwyrick Exp $
// $Log: al212.c,v $
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
//
//-----------------------------------------------------------------------------

//----------------------------------------------------------------------------
//  Init212
//----------------------------------------------------------------------------
static void initAL212(int BrdNum)
{
}

//----------------------------------------------------------------------------
//  AL212_SWTrigger
//----------------------------------------------------------------------------
static void AL212_SWTrigger(int BrdNum)
{
  int fpga = brds[BrdNum].bar2start; 
  int tmp = inb(fpga + 0x94);
  
  outb(tmp | 0x80, fpga + 0x94);
}

//----------------------------------------------------------------------------
//  AL212_BrdAbortDMA
//----------------------------------------------------------------------------
static void AL212_BrdAbortDMA(int BrdNum)
{
  unsigned char tmp;
  int fpga = brds[BrdNum].bar2start; 

  tmp = inb(fpga + 0x80);   
   
  outb(tmp | 0x08, fpga + 0x80);
  outb(tmp, fpga + 0x80);
}

//----------------------------------------------------------------------------
//  Upload212RBF
//----------------------------------------------------------------------------
#define AL212_CONF_OFFSET	0xFC

#define AL212_CONF_MASK		0x0D
#define AL212_CONF_START	0x00
#define AL212_CONF_NEXT		0x05
#define AL212_CONF_ERROR	0x01
#define AL212_CONF_DONE		0x0D

static int Upload212RBF(int BrdNum, char *data, long size)
{
// Point to the Start of the FPGA Registers  
  int i, pdata, conf;
  char tmp;
  
  pdata = brds[BrdNum].bar2start + 0;
  conf  = brds[BrdNum].bar2start + AL212_CONF_OFFSET;
  //unsigned char *pm = brds[0].bar3start;
       
  printk("<Upload212RBF> pdata: %08X, conf: %08X\n", pdata, conf);       
  printk("<Upload212RBF> Data: %08X, Size: %li\n",(int)data, size);
            
  // CONFIG to Low 
  outb(0, conf);
//  pm[AL212_CONF_OFFSET] = 0;
  udelay(800);
       
  tmp = inb(conf);                  
//  tmp = pm[AL212_CONF_OFFSET];
  if ( (tmp & AL212_CONF_MASK) != AL212_CONF_START) {
    printk("<Upload212RBF> Upload Failed to Start. %02X \n", (unsigned char)tmp);
    return 0;
  }
                                 
  // CONFIG to High
  outb(1, conf);
//  pm[AL212_CONF_OFFSET] = 1;
  udelay(40);
                                        
  for(i = 0; i < size; i++) {
  //  tmp = pm[AL212_CONF_OFFSET];
    tmp = inb(conf);
    if ( (tmp & AL212_CONF_MASK) == AL212_CONF_NEXT) {
      udelay(2);
      outb(data[i], pdata);
    //  pm[0] = data[i];
      udelay(2);  
    } else {  // NOT NEXT
      printk("CONFIG not NEXT for byte %i during upload, %02X.\n",i,tmp);  
      return i;
    } 
  }
                                                                                          
  udelay(10);  // Delay before access registers

  //tmp = pm[AL212_CONF_OFFSET];  
  tmp = inb(conf);                  
  if ( (tmp & AL212_CONF_MASK) == AL212_CONF_DONE) {
    brds[BrdNum].UploadStatus = 1;
    return size;
  } else if ( (tmp & AL212_CONF_MASK) == AL212_CONF_ERROR)
    printk("Error occured during upload\n");  
    
  return 0;  
}
                                                                                                            
