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
// $Id: al1g.c,v 1.2 2004/12/22 19:29:06 mwyrick Exp $
// $Log: al1g.c,v $
// Revision 1.2  2004/12/22 19:29:06  mwyrick
// Working on Multi Board
//
// Revision 1.1.1.1  2004/12/16 14:27:28  mwyrick
// ALLinux 2004
//
// Revision 1.1.1.1  2004/04/29 19:20:14  mwyrick
// AcqLog Linux Driver
//
// Revision 1.9  2002/12/24 19:15:53  mwyrick
// Debugging the AL1G.  Works with First BCB version of ALScope
//
// Revision 1.8  2002/12/18 21:50:37  mwyrick
// IOCTL_GET_BRDTYPE
//
// Revision 1.7  2002/12/18 14:50:06  mwyrick
// Working uploads to AL1G
//
// Revision 1.6  2002/12/17 19:46:07  mwyrick
// Started Adding AL1G Support
//
//-----------------------------------------------------------------------------

//----------------------------------------------------------------------------
//  Init1G
//----------------------------------------------------------------------------
static void initAL1G(int BrdNum)
{
}

//----------------------------------------------------------------------------
//  AL1G_SWTrigger
//----------------------------------------------------------------------------
static void AL1G_SWTrigger(int BrdNum)
{
  int fpga = brds[BrdNum].bar2start; 
  int tmp = inb(fpga + 0x94);
  
  outb(tmp | 0x80, fpga + 0x94);
}

//----------------------------------------------------------------------------
//  AL1G_BrdAbortDMA
//----------------------------------------------------------------------------
static void AL1G_BrdAbortDMA(int BrdNum)
{
  unsigned char tmp;
  int fpga = brds[BrdNum].bar2start; 

  tmp = inb(fpga + 0x80);   
   
  outb(tmp | 0x08, fpga + 0x80);
  outb(tmp, fpga + 0x80);
}

//----------------------------------------------------------------------------
//  Upload1GRBF
//----------------------------------------------------------------------------
#define AL1G_CONF_OFFSET	0x0C

#define AL1G_CONF_MASK		0x0D
#define AL1G_CONF_START		0x00
#define AL1G_CONF_NEXT		0x05
#define AL1G_CONF_ERROR		0x01
#define AL1G_CONF_DONE		0x0D

static int Upload1GRBF(int BrdNum, char *data, long size)
{
// Point to the Start of the FPGA Registers  
  int i, pdata, conf;
  char tmp;
  
  pdata = brds[BrdNum].bar2start + 0;
  conf  = brds[BrdNum].bar3start + AL1G_CONF_OFFSET;
       
  printk("<Upload1GRBF> pdata: %08X, conf: %08X\n", pdata, conf);       
  printk("<Upload1GRBF> Data: %08X, Size: %li\n",(int)data, size);
            
  // CONFIG to Low 
  outb(0, conf);
  udelay(8);
       
  tmp = inb(conf);                  
  if ( (tmp & AL1G_CONF_MASK) != AL1G_CONF_START) {
    printk("<Upload1GRBF> Upload Failed to Start. %02X \n", (unsigned char)tmp);
    return 0;
  }
                                 
  // CONFIG to High
  outb(1, conf);
  udelay(40);
                                        
  for(i = 0; i < size; i++) {
    tmp = inb(conf);
    if ( (tmp & AL1G_CONF_MASK) == AL1G_CONF_NEXT) {
      udelay(2);
      outb(data[i], pdata);
      udelay(2);  
    } else {  // NOT NEXT
      printk("CONFIG not NEXT for byte %i during upload, %02X.\n",i,tmp);  
      return i;
    } 
  }
                                                                                          
  udelay(10);  // Delay before access registers
  if ( (inb(conf) & AL1G_CONF_MASK) == AL1G_CONF_DONE) {
    brds[BrdNum].UploadStatus = 1;
    return size;
  } else if ( (inb(conf) & AL1G_CONF_MASK) == AL1G_CONF_ERROR)
    printk("Error occured during upload\n");  
    
  return 0;  
}
                                                                                                            
