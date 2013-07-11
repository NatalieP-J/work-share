#include <linux/mm.h>
#include <linux/wrapper.h>
#include <linux/highmem.h>

#ifndef vmalloc_to_page
struct page * vmalloc_to_page(void * vmalloc_addr)
{
  unsigned long addr = (unsigned long) vmalloc_addr;
  struct page *page = NULL;
  pmd_t *pmd;
  pte_t *pte;
  pgd_t *pgd;
  
  pgd = pgd_offset_k(addr);
  if (!pgd_none(*pgd)) {
    pmd = pmd_offset(pgd, addr);
    if (!pmd_none(*pmd)) {
      pte = pte_offset(pmd, addr);
      if (pte_present(*pte)) {
        page = pte_page(*pte);
      }
    }
  }
  return page;
}
#endif
//------------------------------------------------------------------------
// kvirt_to_pa
//------------------------------------------------------------------------
static inline unsigned long kvirt_to_pa(unsigned long adr) 
{
  unsigned long kva, ret;

  kva = (unsigned long) page_address(vmalloc_to_page((void *)adr));
  kva |= adr & (PAGE_SIZE-1); /* restore the offset */
  ret = __pa(kva);
  return ret;
}

//------------------------------------------------------------------------
// ali_malloc
//------------------------------------------------------------------------
static void * ali_malloc(signed long size)
{
  void *mem;
  unsigned long adr;

  size=PAGE_ALIGN(size);
  mem=vmalloc_32(size);
  if (NULL != mem) {
    /* Mark the ram so users can check mmapings */
    memset(mem, 0xAD, size);

    adr=(unsigned long) mem;
    while (size > 0) {
      mem_map_reserve(vmalloc_to_page((void*)adr));
      adr+=PAGE_SIZE;
      size-=PAGE_SIZE;
    }  
  } else {
    printk(KERN_INFO "<aldriver> vmalloc_32(%ld) failed\n",size);
  }
  return mem;
}

//------------------------------------------------------------------------
// ali_free
//------------------------------------------------------------------------
static void ali_free(void *mem, signed long size)
{
  unsigned long adr;
        
  if (mem) {
    adr=(unsigned long) mem;
    while (size > 0) {
      mem_map_unreserve(vmalloc_to_page((void*)adr));
      adr+=PAGE_SIZE;
      size-=PAGE_SIZE;
    }
    vfree(mem);
  }
}
