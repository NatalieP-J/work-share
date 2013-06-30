static struct proc_dir_entry *ali_procdir;

//----------------------------------------------------------------------------
//  ali_procinfo()
//----------------------------------------------------------------------------
static int ali_procinfo(char *buf, char **start, off_t fpos, int lenght, int *eof, void *data)
{
  char *p;
  int i, x, bn;
  long dptr;

  // Point to the Start of the FPGA Registers  
  int pdata;

  p = buf;
  p += sprintf(p,"Acquisition Logic driver %s\n", Version); 
  p += sprintf(p,"Number of Boards: %i\n", NumberOfBoards);

  for(bn=0; bn < NumberOfBoards; bn++) {
      p += sprintf(p,"\nBoard Number %i\n", bn);
      p += sprintf(p,"Board Type  : %s      ", brds[bn].BrdTypeStr);

      p += sprintf(p,"Counter %i\n", brds[bn].DebugCounter);

      p += sprintf(p,"SGL Count %i   ", brds[bn].nodecnt);
      p += sprintf(p,"DMA STATUS %li   ", brds[bn].dma_status);
      p += sprintf(p,"brd STATUS %02lX\n", brds[bn].brd_status);

      dptr = inl(brds[bn].PLXaddr + PLX_DMADPR0);
      p += sprintf(p,"PLX DMA_DPTR %08lX", dptr);  
      i = FindSGN(bn, dptr);
      if (i >= 0)
        p += sprintf(p," is SGL Node %i\n", i);
      else
        p += sprintf(p," is Not a SGL Node\n");  

      dptr = inl(brds[bn].PLXaddr + PLX_DMASIZ0);
      p += sprintf(p,"PLX DMASIZ0 %08lX   ", dptr);      
      dptr = inb(brds[bn].PLXaddr + PLX_DMACSR0);
      p += sprintf(p,"PLX DMACSR0 %02lX   ", dptr);      
      dptr = inl(brds[bn].PLXaddr + PLX_INTCSR);
      p += sprintf(p,"PLX INTCSR %08lX\n", dptr);      

      pdata = brds[bn].ioFPGAaddr;    

      //if (brds[0].UploadStatus) {
        char b1,b2,b3;
        b1 = inb(pdata + 0x7C);
        b2 = inb(pdata + 0x7D);
        b3 = inb(pdata + 0x7E);   
        p += sprintf(p,"FPGA Version: %02X:%02X:%02X\n",b3,b2,b1);

        unsigned char *pm = brds[bn].vmemFPGAaddr;    

        for(x=0;x<256;x+=16) {
          p += sprintf(p,"%02X: ",x);    
          for(i=0;i<16;i++) {
            if (((x+i) < 0x40 || (x+i) > 0x5F))  // Don't read 0x40 - 0x6F
              p += sprintf(p, "%02X ", pm[x+i]);
            else
              p += sprintf(p, "** ");            
            if (i == 7)
              p += sprintf(p, "- ");      
          }
          p+= sprintf(p,"\n");
        }    
  }
   
  *eof = 1;
  return p - buf;
}

//----------------------------------------------------------------------------
//  register_proc()
//----------------------------------------------------------------------------
static void register_proc()
{
  ali_procdir = create_proc_entry("aldriver", S_IFREG | S_IRUGO, 0);
  ali_procdir->read_proc = ali_procinfo;
}

//----------------------------------------------------------------------------
//  unregister_proc()
//----------------------------------------------------------------------------
static void unregister_proc()
{
  remove_proc_entry("aldriver",0);
}
