static int opened[MAX_MINOR+1];

//------------------------------------------------------------------------
// 
//------------------------------------------------------------------------
static int CheckBrdNum(int BrdNum)
{
  if (BrdNum > NumberOfBoards) {
    printk("<aldriver::CheckBrdNum> Invalid Board Number. Reset to 0\n");
    return 0;
  }

  return BrdNum;
}

//------------------------------------------------------------------------
// PrintPLXRegisters
//------------------------------------------------------------------------
static void PrintPLXRegisters(int BrdNum)
{
  char p[255];
  int x, i;

  printk("<aldriver> PLX Registers\n");  
  for(x=0;x<256;x+=16) {
    sprintf(p,"<aldriver> %02X: ",x); printk(p);
    for(i=0;i<16;i++) {
      sprintf(p, "%02X ", inb(brds[BrdNum].PLXaddr + x + i)); printk(p);
      if (i == 7) {
        printk("- "); 
      }  
    }
    printk("\n");
  }    
}

//------------------------------------------------------------------------
// PrintFPGARegisters
//------------------------------------------------------------------------
static void PrintFPGARegisters(int BrdNum)
{
  char p[255];
  int x, i;

  printk("<aldriver> FPGA Registers\n");  
  for(x=0;x<256;x+=16) {
    sprintf(p,"<aldriver> %02X: ",x); printk(p);
    for(i=0;i<16;i++) {
      if (((x+i) < 0x40 || (x+i) >= 0x60)) { // Don't read 0x40 - 0x5F
          sprintf(p, "%02X ", inb(brds[BrdNum].ioFPGAaddr + x + i)); printk(p);
        } else
          printk("** ");            
      if (i == 7) {
        printk("- "); 
      }  
    }
    printk("\n");
  }    
}

//------------------------------------------------------------------------
// WriteReg
//------------------------------------------------------------------------
static void WriteReg(int BrdNum, TReg_Def *reg)
{
  int v;
  
  switch (reg->Size) {
    case REGSIZE_BYTE:
      *(unsigned char*)(brds[BrdNum].vmemFPGAaddr + reg->Address) = reg->Value;
      break;
    
    case REGSIZE_WORD:
      *(unsigned short*)(brds[BrdNum].vmemFPGAaddr + reg->Address) = reg->Value;
      break;
  
    case REGSIZE_LONG:
      *(unsigned long*)(brds[BrdNum].vmemFPGAaddr + reg->Address) = reg->Value;
    break;

    case REGSIZE_RBW_BYTE:
      v = *(unsigned char*)(brds[BrdNum].vmemFPGAaddr + reg->Address);
      v &= ~reg->Mask;
      v |= (reg->Value << reg->Shift) & reg->Mask;
      *(unsigned char*)(brds[BrdNum].vmemFPGAaddr + reg->Address) = v;
    break;
    
    case REGSIZE_RBW_WORD:
      v = *(unsigned short*)(brds[BrdNum].vmemFPGAaddr + reg->Address);
      v &= ~reg->Mask;
      v |= (reg->Value << reg->Shift) & reg->Mask;
      *(unsigned short*)(brds[BrdNum].vmemFPGAaddr + reg->Address) = v;
    break;
  
    case REGSIZE_RBW_LONG:
      v = *(unsigned long*)(brds[BrdNum].vmemFPGAaddr + reg->Address);
      v &= ~reg->Mask;      
      v |= (reg->Value << reg->Shift) & reg->Mask;
      *(unsigned long*)(brds[BrdNum].vmemFPGAaddr + reg->Address) = v;
    break;
  }  
}

//------------------------------------------------------------------------
// ReadReg
//------------------------------------------------------------------------
static void ReadReg(int BrdNum, TReg_Def *reg)
{
  int v;
  
  switch (reg->Size) {
    case REGSIZE_RBW_BYTE:
    case REGSIZE_BYTE:
      v = *(unsigned char*)(brds[BrdNum].vmemFPGAaddr + reg->Address);
      v &= reg->Mask;
      reg->Value = (v >> reg->Shift);
    break;

    case REGSIZE_RBW_WORD:    
    case REGSIZE_WORD:
      v = *(unsigned short*)(brds[BrdNum].vmemFPGAaddr + reg->Address);      
      v &= reg->Mask;
      reg->Value = (v >> reg->Shift);
    break;

    case REGSIZE_RBW_LONG:  
    case REGSIZE_LONG:
      v = *(unsigned long*)(brds[BrdNum].vmemFPGAaddr + reg->Address);
      v &= reg->Mask;
      reg->Value = (v >> reg->Shift);
    break;
    default:
      printk("Reading Unknown\n");
      break;
  }
}

//------------------------------------------------------------------------
// wait_for_isr
//------------------------------------------------------------------------
static void wait_for_isr(int BrdNum)
{
  int csr;
  DECLARE_WAITQUEUE(wait, current);

  csr = inb(brds[BrdNum].PLXaddr + PLX_DMACSR0);

  add_wait_queue(&brds[BrdNum].dma_wq, &wait);
  
  // Check if DMA is already finished
  // If Not, then Sleep
  cli();
  if ((csr & 0x10) == 0) {
    set_current_state(TASK_INTERRUPTIBLE);
    schedule();
  } else {
    sti();
//    printk("Call to wait for isr with DMA Done\n");
  }
  
  set_current_state(TASK_RUNNING);
  remove_wait_queue(&brds[BrdNum].dma_wq, &wait);
}

//------------------------------------------------------------------------
// Clear Buffer Status
//------------------------------------------------------------------------
static void ClearStatus(int BrdNum, int Status)
{
    unsigned long flags;
    ADBoard *brd = &brds[BrdNum];
    spin_lock_irqsave(&brd->sl_status, flags);
    if (Status == 0) {
      brd->BufferStatus &= ~0x01;        
    } else if (Status == 1) {  
      brd->BufferStatus &= ~0x02;
    }
    outb(brd->BufferStatus << 1, brd->ioFPGAaddr + 0x34);
    spin_unlock_irqrestore(&brd->sl_status, flags);
}

//------------------------------------------------------------------------
// Get Buffer Status
//------------------------------------------------------------------------
static long GetStatus(int BrdNum)
{
    unsigned long flags;
    long retval;
    ADBoard *brd = &brds[BrdNum];
    spin_lock_irqsave(&brd->sl_status, flags);
    retval =  brd->BufferStatus;        
    spin_unlock_irqrestore(&brd->sl_status, flags);
    
    return retval;
}

//----------------------------------------------------------------------------
//
//  ali_poll()
//
//----------------------------------------------------------------------------
static unsigned int ali_poll(struct file* file, poll_table* wait)
{
  return 0;
}

//----------------------------------------------------------------------------
//
//  ali_open()
//
//----------------------------------------------------------------------------
static int ali_open(struct inode *inode,struct file *filp)
{
  unsigned int minor = MINOR(inode->i_rdev);
  TFile_Private *pri = NULL;
  
  int BrdNum = CheckBrdNum(minor - 1);

  if (minor == CONTROL_MINOR) {
    opened[minor]++;
    return(0);
  }

  if (minor > MAX_MINOR) {
    return(-ENODEV);
  }

  brds[BrdNum].DebugCounter = 1;  
  opened[minor] = 1;
  filp->private_data = kmalloc(sizeof(TFile_Private), GFP_KERNEL);
  if (!(filp->private_data))
    return -ENOMEM;
  pri = filp->private_data;
  pri->ReadType = 0;       
  pri->BrdNum = BrdNum;

  return(0);
}

//----------------------------------------------------------------------------
//
//  ali_release()
//
//----------------------------------------------------------------------------
static int ali_release(struct inode *inode,struct file *filp)
{
  unsigned int minor = MINOR(inode->i_rdev);

  int BrdNum = CheckBrdNum(minor - 1);

  if (minor > MAX_MINOR) {
    return(-ENODEV);
  }

  if (minor == CONTROL_MINOR) {
    opened[minor]--;
    return(0);
  }

  AbortDMA(BrdNum);

  cli();
  kfree(filp->private_data);
  filp->private_data = NULL;
  sti();
  
  opened[minor]--;

  return 0;
}

//----------------------------------------------------------------------------
//
//  ali_read()
//
//----------------------------------------------------------------------------
static ssize_t ali_read(struct file *filp, char *buf, size_t count, loff_t *ppos)
{
  unsigned int minor = MINOR(filp->f_dentry->d_inode->i_rdev);  
  TFile_Private *pri = filp->private_data;
  int x;  
  char *ptr;

  int BrdNum = CheckBrdNum(minor - 1);

  if (count > PAGE_SIZE)
    count = PAGE_SIZE;
  
  ptr = (char*)brds[BrdNum].dma_addr;
  for(x=0;x<count;x++)
    ptr[x] = 0xBA;

  DoDMA(BrdNum, pri->LocalBusAddress, count);
   
  copy_to_user(buf, (void*)brds[BrdNum].dma_addr, count);
  *ppos += count;
  return (count);
}

//----------------------------------------------------------------------------
//
//  ali_write()
//
//----------------------------------------------------------------------------
static ssize_t ali_write(struct file *filp, const char *buf, size_t count, loff_t *ppos)
{
  unsigned int minor = MINOR(filp->f_dentry->d_inode->i_rdev);  
  char *temp = (char *)buf;
  char *tempdata;
  int realcount = 0;
//  TFile_Private *pri = filp->private_data;
  
  int BrdNum = CheckBrdNum(minor - 1);

  tempdata = vmalloc(count);
  if (!tempdata) {
    printk("<<ali_write>> kmalloc failed\n");
  } else {  
    copy_from_user(tempdata, temp, count);
    if (brds[BrdNum].BrdType == BRDTYPE_AL8100)
      realcount = Upload8100RBF(BrdNum, tempdata, count);
    else if (brds[BrdNum].BrdType == BRDTYPE_AL1G)
      realcount = Upload1GRBF(BrdNum, tempdata, count);
    else if (brds[BrdNum].BrdType == BRDTYPE_AL212)
      realcount = Upload212RBF(BrdNum, tempdata, count);
    else if (brds[BrdNum].BrdType == BRDTYPE_AL4108)
      realcount = Upload4108RBF(BrdNum, tempdata, count);
      
    vfree(tempdata);
  }  
  
  *ppos += realcount;
  return(realcount);
}

//----------------------------------------------------------------------------
//  ali_mmap()
//----------------------------------------------------------------------------
static int ali_mmap(struct file *filp, struct vm_area_struct *vma)
{
  unsigned int minor = MINOR(filp->f_dentry->d_inode->i_rdev);  
  TFile_Private *pri = filp->private_data;
  
  int BrdNum = CheckBrdNum(minor - 1);

  unsigned long pa;
  unsigned long va;
  unsigned long start = vma->vm_start;
  long size = vma->vm_end - vma->vm_start;
  
  if (pri->mmapType == 0) {
    va = brds[BrdNum].dma_addr; 
    while (size > 0) {
      pa = kvirt_to_pa(va);
      if (remap_page_range(start, pa, PAGE_SIZE, PAGE_SHARED)) {
        printk("<mmap>remap Failed\n");
        return -EAGAIN;
      }
      start += PAGE_SIZE;
      va    += PAGE_SIZE;
      size  -= PAGE_SIZE;
    }             
  } else {
    pa = brds[BrdNum].memFPGAaddr;

    vma->vm_flags |= VM_IO | VM_SHM | VM_LOCKED | VM_RESERVED; 
    pgprot_val(vma->vm_page_prot) |= __PAGE_KERNEL_NOCACHE;
    
    if (io_remap_page_range(start, pa, size, vma->vm_page_prot)) {
      printk("<mmap>remap Failed\n");
      return -EAGAIN;
    }
  } 
  
  return 0;
}

//----------------------------------------------------------------------------
//  ali_ioctl()
//----------------------------------------------------------------------------
static int ali_ioctl(struct inode *inode,struct file *filp,unsigned int cmd, unsigned long arg)
{
  unsigned int minor = MINOR(filp->f_dentry->d_inode->i_rdev);  
  TFile_Private *pri = filp->private_data; 
  int BrdNum = CheckBrdNum(minor - 1);
  
  switch(cmd) {
    case IOCTL_GET_BRDTYPE:
      *(long*)arg = brds[BrdNum].BrdType;
      break;
      
    case IOCTL_GET_NUMBOARDS:
      *(long*)arg = NumberOfBoards;
      break;

    case IOCTL_GET_BRD0_TYPE:
      *(long*)arg = brds[0].BrdType;
      break;

    case IOCTL_GET_BRD1_TYPE:
      *(long*)arg = brds[1].BrdType;
      break;
      
    case IOCTL_GET_BRD2_TYPE:
      *(long*)arg = brds[2].BrdType;
      break;
      
    case IOCTL_GET_BRD3_TYPE:
      *(long*)arg = brds[3].BrdType;
      break;
      
      
    case IOCTL_INITBRD:
      if (brds[BrdNum].BrdType == BRDTYPE_AL8100)            
        initAL8100(BrdNum);
      else  if (brds[BrdNum].BrdType == BRDTYPE_AL1G)            
        initAL1G(BrdNum);
      else  if ((brds[BrdNum].BrdType == BRDTYPE_AL212) || (brds[BrdNum].BrdType == BRDTYPE_AL2124))
        initAL212(BrdNum);
      else  if (brds[BrdNum].BrdType == BRDTYPE_AL4108)            
        initAL4108(BrdNum);
      break;

    case IOCTL_PRINTPLX:
      PrintPLXRegisters(BrdNum);
      break;

    case IOCTL_PRINTFPGA:
      PrintFPGARegisters(BrdNum);
      break;

    // DMA Stuff
    case IOCTL_LOCALBUS_ADDR:
      pri->LocalBusAddress = arg;
      break;

    case IOCTL_TRANSFERCOUNT:
      pri->TransferCount = arg;
      break;

    case IOCTL_GET_DMASTATUS:
      *(long*)arg = brds[BrdNum].dma_status;
      break;

    case IOCTL_GET_BRDSTATUS:
      *(long*)arg = brds[BrdNum].brd_status;
      break;

    case IOCTL_GET_RBFSTATUS:
      *(long*)arg = brds[BrdNum].UploadStatus;
      break;

    case IOCTL_GET_FIFOSTATUS:
      *(long*)arg = brds[BrdNum].fifo_status;
      break;
    
    case IOCTL_STARTDMA:      
      brds[BrdNum].WhichBuffer = 0;
      DoDMA(BrdNum, pri->LocalBusAddress, pri->TransferCount);            
      brds[BrdNum].NumIntsBS = brds[BrdNum].NumInts;  // Record the Number of Interrupts We have had
      break;
      
    case IOCTL_ABORTDMA:
      AbortDMA(BrdNum);
      if (brds[BrdNum].AbortingDMA == 0) { 
        brds[BrdNum].dma_status = DMASTATUS_DONE;
      } else {
        brds[BrdNum].dma_status = DMASTATUS_ABORTING;
      }
      break;

    case IOCTL_COLLECTDATA:      
      // Set Transfer Size
      pri->TransferCount = arg;        
      
      // StartDMA
      
      //
      // WARNING TURNING OFF INTERRUPTS
      //
      cli();
      
      DoDMA(BrdNum, pri->LocalBusAddress, pri->TransferCount);            
      brds[BrdNum].NumIntsBS = brds[BrdNum].NumInts;  // Record the Number of Interrupts We have had      
      
      // SW Trigger
      if (brds[BrdNum].BrdType == BRDTYPE_AL8100)            
        AL8100_SWTrigger(BrdNum);
      else  if (brds[BrdNum].BrdType == BRDTYPE_AL1G)            
        AL1G_SWTrigger(BrdNum);     
      else  if ((brds[BrdNum].BrdType == BRDTYPE_AL212) || (brds[minor].BrdType == BRDTYPE_AL2124))
        AL212_SWTrigger(BrdNum);     
      else  if (brds[BrdNum].BrdType == BRDTYPE_AL4108)            
        AL4108_SWTrigger(BrdNum);     
      
      brds[BrdNum].NumIntsBS = brds[BrdNum].NumInts;
      wait_for_isr(BrdNum);
      break;

    case IOCTL_SET_CIRCLEBUFFER:
      brds[BrdNum].CircleBuffer = arg;
      break;

    case IOCTL_SET_NUMINTS:
      brds[BrdNum].NumIntsPerCircle = arg;
      break;
    
    case IOCTL_CLR_CNTREG:
      outb(arg, brds[BrdNum].ioFPGAaddr + 0x78);
      break;

    case IOCTL_WAITPROGRESS:      
      wait_for_isr(BrdNum);
      break;

    case IOCTL_SWTRIGGER:         
      if (brds[BrdNum].BrdType == BRDTYPE_AL8100)            
        AL8100_SWTrigger(BrdNum);
      else  if (brds[BrdNum].BrdType == BRDTYPE_AL1G)            
        AL1G_SWTrigger(BrdNum);
      else  if (brds[BrdNum].BrdType == BRDTYPE_AL4108)            
        AL4108_SWTrigger(BrdNum);
      else  if ((brds[BrdNum].BrdType == BRDTYPE_AL212) || (brds[BrdNum].BrdType == BRDTYPE_AL2124))
        AL212_SWTrigger(BrdNum);     
      brds[BrdNum].NumIntsBS = brds[BrdNum].NumInts;
      wait_for_isr(BrdNum);
      break;

    case IOCTL_SETDMATIMEOUT:
      DMATimeout = arg;
      break;

    case IOCTL_ALLOC_DMA_BUFFER:
      alloc_dma_buffer(BrdNum, arg);
      break;

    case IOCTL_FREE_DMA_BUFFER:      
      free_dma_buffer(BrdNum);
      break;

    case IOCTL_WRITE_REG:
      WriteReg(BrdNum, (TReg_Def *)arg);
      break;
      
    case IOCTL_READ_REG:
      ReadReg(BrdNum, (TReg_Def *)arg);      
      break;

    case IOCTL_SETMEMTYPE:
      pri->mmapType = arg;
      break;

    case IOCTL_GETBUFFERSTATUS:
      *(long*)arg = GetStatus(BrdNum);
      break;
         
    case IOCTL_CLEARBUFFERSTATUS:
      ClearStatus(BrdNum, arg);
      break;

    default:
      return -EINVAL;    
  }
  
  return(0);
}

