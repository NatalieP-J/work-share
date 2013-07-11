//------------------------------------------------------------------------
// FindSGN
//   With a given dptr, find which Node the dma is working on
//------------------------------------------------------------------------
static int FindSGN(int BrdNum, long dptr)
{
  struct sgl_node *node;
  int x;

  node = brds[BrdNum].sgl;
  
  if (node == 0) 
    return -1;

  for(x=0; x< brds[BrdNum].nodecnt; x++) {
    // or with EOC so this will still work if we mark the EOC in the chain
    if ((node->next | PLX_EOC | PLX_TINT) == (dptr | PLX_EOC | PLX_TINT))
      return x;
    node++;  
  }
  return -1;
}

//------------------------------------------------------------------------
// GetSGN
//   Return the sgl_node number nodenumber
//------------------------------------------------------------------------
static struct sgl_node* GetSGN(int BrdNum, int nodenumber)
{
  struct sgl_node *node;

  node = brds[BrdNum].sgl + nodenumber;
  return node;
}

//------------------------------------------------------------------------
//  CountDMADone
//    return how much DMA is already done
//------------------------------------------------------------------------
static int CountDMADone(int BrdNum)
{
  int cnt = 0;
  int sgn = FindSGN(BrdNum, inl(brds[BrdNum].PLXaddr + PLX_DMADPR0));
  if (sgn < 0)
    return 0;
    
  cnt = sgn * PAGE_SIZE;
  cnt += GetSGN(BrdNum, sgn)->size;
  return cnt;
}

//------------------------------------------------------------------------
// BuildSGL
//------------------------------------------------------------------------
static void BuildSGL(int BrdNum, long Laddr, long count)
{
  struct sgl_node *node;
  unsigned long adr;
  long size = count;
  int numnodes, numqn;
  int x;
  int Sgl_PAGE_SIZE = PAGE_SIZE;

  brds[BrdNum].nodecnt = 0;
  node = brds[BrdNum].sgl;

  if (node == 0) {
    printk("<BuildSGL> brds[].sgl equal to NULL\n");
    return;
  } 

  adr=(unsigned long) brds[BrdNum].dma_addr;
  while (size > 0) {
    brds[BrdNum].nodecnt++;
    node->pciaddr   	= kvirt_to_pa(adr);
    node->localaddr 	= Laddr;

    if (size > Sgl_PAGE_SIZE)
      node->size	= Sgl_PAGE_SIZE;
    else
      node->size	= size;         
      
    adr  += Sgl_PAGE_SIZE;
    size -= Sgl_PAGE_SIZE;
    if (size > 0) {
      node->next	= kvirt_to_pa((unsigned long)(node + 1));
      node->next       |= PLX_READ | PLX_PCI;
      node++;    
    }  else {
      // Mark end of List
      if (brds[BrdNum].CircleBuffer) {
        #ifdef DEBUGGING
        printk("aldriver::BuildSDL> Circle Mode Active\n");
        #endif
        node->next  = kvirt_to_pa((unsigned long)brds[BrdNum].sgl);
        node->next |= PLX_READ | PLX_PCI;     
      } else {
        node->next = PLX_READ | PLX_EOC | PLX_TINT | PLX_PCI;     
      }
    }
  }

  // Setup the Number of Interrupts per Circle
  if (brds[BrdNum].NumIntsPerCircle > 0) {        
    numnodes = brds[BrdNum].nodecnt;
    numqn = numnodes / brds[BrdNum].NumIntsPerCircle;
    #ifdef DEBUGGING    
    printk("<aldriver::BuildSGL> # Nodes is %i\n", numnodes);
    #endif
    if (numqn > 0) {
      for(x=1; x<= brds[BrdNum].NumIntsPerCircle; x++) {
        int j = (numqn * x) - 1;
        brds[BrdNum].sgl[j].next |= PLX_TINT;
        #ifdef DEBUGGING        
        printk("<aldriver::BuildSGL> Int on %i\n", j);
        #endif
      }  
    }
  }
}

//------------------------------------------------------------------------
// DoDMA
//   Setup and start the DMA
//------------------------------------------------------------------------
#define LOCALBURSTMODE    	
static void DoDMA(int BrdNum, long Laddr, long count)
{ 
  int PLXaddr  = brds[BrdNum].PLXaddr;

  brds[BrdNum].AbortingDMA = 0;
  ali_clr_dma_timer(BrdNum);

  if (brds[BrdNum].dma_size == 0) {
    printk("<DoDMA> DMA buffer not Allocated\n");
    return;
  }

  if ( count > brds[BrdNum].dma_size )
    count = brds[BrdNum].dma_size;

  // Clear out the Memory so we can check for errors
#ifdef DEBUGGING
  memset((void*)brds[BrdNum].dma_addr, 0xAD, count);
#endif

  brds[BrdNum].WhichBuffer = 0;

  brds[BrdNum].dma_transcnt = count; 
  BuildSGL(BrdNum, Laddr, count);  
  brds[BrdNum].brd_status = 0;

  outl( PLX_32BIT 	|  	// Transfer Size
    	PLX_TARDY 	|	// TA#/READY#
    	PLX_SCATTER  	|   	// Used for Scatter/Gather List Mode
    	PLX_0WS         |
#ifdef LOCALBURSTMODE    	
    	PLX_BTERM	|	// BTERM Ends Burst
    	PLX_LOCBURS	|	// LocalBus Burst
#endif    	
    	PLX_DINT  	| 	// Done Interrupt
    	PLX_LOCINC 	| 	// Local Address Don't Inc
  	PLX_DEMAND 	| 	// Demand Mode
  	PLX_EOT 	| 	// EOT
   	PLX_PCIINT, 		// PCI Interrupt
        PLXaddr + PLX_DMAMODE0);

  // Setup PLX for SGL Mode
  outl(kvirt_to_pa((unsigned long)brds[BrdNum].sgl) | PLX_PCI, PLXaddr + PLX_DMADPR0);

  brds[BrdNum].dma_status = DMASTATUS_INPROGRESS; 
  ali_set_dma_timer(BrdNum, DMATimeout);  // Timeout in Seconds

  // OK, Start the DMA Transfer
  outb(PLX_ENABLE | PLX_START, PLXaddr + PLX_DMACSR0);
}

//------------------------------------------------------------------------
// AbortDMA
//------------------------------------------------------------------------
static void AbortDMA(int BrdNum)
{
  int csr;
  
#define TERMNODES
#undef TERMNODES  

#ifdef TERMNODES  
  int PLXaddr  = brds[BrdNum].PLXaddr;
  struct sgl_node *node;
  int x;
  
  node = brds[BrdNum].sgl;
  for(x=0; x < brds[BrdNum].nodecnt; x++) {
    node->next |= PLX_EOC;
    node++;  
  }
#endif  

  ali_clr_dma_timer(BrdNum);

  csr = inb(brds[BrdNum].PLXaddr + PLX_DMACSR0);

  // Check if DMA is already finished
  if ((csr & 0x10) == 0) {
    if (brds[BrdNum].BrdType == BRDTYPE_AL8100)
      AL8100_BrdAbortDMA(BrdNum);
    else if (brds[BrdNum].BrdType == BRDTYPE_AL1G)
      AL1G_BrdAbortDMA(BrdNum);  
    else if (brds[BrdNum].BrdType == BRDTYPE_AL212)
      AL212_BrdAbortDMA(BrdNum);  
    else if (brds[BrdNum].BrdType == BRDTYPE_AL4108)
      AL4108_BrdAbortDMA(BrdNum);  
    brds[BrdNum].AbortingDMA = 1;
  } else {
    brds[BrdNum].AbortingDMA = 0;
    outb(0, brds[BrdNum].PLXaddr + PLX_DMACSR0);
  }
}

//------------------------------------------------------------------------
// free_dma_buffer
//------------------------------------------------------------------------
static void free_dma_buffer(int BrdNum)
{
  if (brds[BrdNum].dma_addr) {
    ali_free((void*)brds[BrdNum].dma_addr, brds[BrdNum].dma_size);
    brds[BrdNum].dma_addr = 0;
    brds[BrdNum].dma_size = 0;
  }
  
  if (brds[BrdNum].sgl) {
    ali_free((void*)brds[BrdNum].sgl, brds[BrdNum].sgl_size);
    brds[BrdNum].sgl      = 0;
    brds[BrdNum].sgl_size = 0;
  }  
}

//------------------------------------------------------------------------
// alloc_dma_buffer
//------------------------------------------------------------------------
static int alloc_dma_buffer(int BrdNum, long arg)
{
  int sgl_size;

  free_dma_buffer(BrdNum);
  
  brds[BrdNum].dma_addr = (int)ali_malloc(arg);
  
  if (!brds[BrdNum].dma_addr) {
    printk(KERN_ERR "alloc for DMA Failed.\n");
    return 1;
  }

  brds[BrdNum].dma_size = arg;

  // This will create a sgl buffer 
  sgl_size = (arg / PAGE_SIZE) * 16;
  brds[BrdNum].sgl = (struct sgl_node *)ali_malloc( sgl_size );
  brds[BrdNum].sgl_size = sgl_size;

  if (!brds[BrdNum].sgl) {
    printk(KERN_ERR "alloc for SGL Failed.\n");
    free_dma_buffer(BrdNum);
    return 1;
  }
  
  return (0);
}

