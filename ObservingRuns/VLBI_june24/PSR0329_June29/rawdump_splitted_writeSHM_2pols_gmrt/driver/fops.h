//----------------------------------------------------------------------------
// Prototypes
//----------------------------------------------------------------------------
static int ali_open(struct inode *, struct file *);
static int ali_release(struct inode *, struct file *);
static ssize_t ali_read(struct file *,char *, size_t, loff_t *);
static ssize_t ali_write(struct file *,const char *, size_t, loff_t *);
static unsigned int ali_poll(struct file *, poll_table *);
static int ali_ioctl(struct inode *, struct file *, unsigned int, unsigned long);
static int ali_mmap(struct file *file,struct vm_area_struct *vma);
//static long long ali_llseek(struct file *,loff_t,int);
//static int ali_select(struct inode *inode,struct file *file,int mode, select_table *table);

//----------------------------------------------------------------------------
// Types
//----------------------------------------------------------------------------
static struct file_operations ali_fops = 
{
  read:     ali_read,
  write:    ali_write,
  poll:     ali_poll,    
  ioctl:    ali_ioctl,
  open:     ali_open,
  release:  ali_release, 
  mmap:     ali_mmap
};
