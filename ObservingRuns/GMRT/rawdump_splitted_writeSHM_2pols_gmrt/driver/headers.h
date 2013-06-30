#include <linux/config.h>
#include <linux/version.h>

#ifdef CONFIG_MODVERSIONS
  #define MODVERSIONS
  #include <linux/modversions.h>
#endif

#include <linux/module.h>
#include <linux/types.h>
#include <linux/errno.h>
#include <linux/proc_fs.h>
#include <linux/pci.h>
#include <linux/poll.h>
#include <linux/delay.h>
#include <linux/vmalloc.h>
#include <linux/interrupt.h>
#include <asm/io.h>
#include <asm/uaccess.h>

#include "types.h"
#include "plx9054.h"
#include "vmem.h"
#include "timers.h"

extern ADBoard brds[MAX_MINOR+1];        
