//------------------------------------------------------------------------------  
//title: Acquisition Logic A/D Board Kernel Driver
//version: Linux 0.0
//date: July 2002                                                              
//designer: Michael Wyrick                                                      
//programmer: Michael Wyrick                                                    
//platform: Linux 2.4.x
//language: GCC 2.95 and 3.0
//module: aldriver
//------------------------------------------------------------------------------  
//  Purpose: Provide a Kernel Driver to Linux for the ALI A/D Boards
//  Docs:                                  
//    This driver supplies an interface to the raw Registers on the boards.
//    in is upto a user library or program to determine what to do with those
//    registers.
//------------------------------------------------------------------------------  
// RCS:
// $Id: plx9054.h,v 1.1.1.1 2004/12/16 14:27:28 mwyrick Exp $
// $Log: plx9054.h,v $
// Revision 1.1.1.1  2004/12/16 14:27:28  mwyrick
// ALLinux 2004
//
// Revision 1.1.1.1  2004/04/29 19:20:14  mwyrick
// AcqLog Linux Driver
//
// Revision 1.6  2002/10/16 21:47:37  mwyrick
// Tring to Get DMA Working Again
//
// Revision 1.5  2002/10/16 20:59:47  mwyrick
// Changed Names on PLX Registers
//
// Revision 1.4  2002/10/14 16:00:27  mwyrick
// Have mmap working
// Have Blocking/NonBlocking IO Working
//
// Revision 1.3  2002/10/11 19:11:09  mwyrick
// Working on Interrupts
//
// Revision 1.2  2002/10/11 14:45:14  mwyrick
// DMA is Working in Simple Mode
// New Structure of Makefile
// Driver is now named ali.o
// new DMA.c file that contains the code for DMA transfers
// .depend works in new Makefile
// PLX constants put into plx9054.h
//
// Revision 1.1.1.1  2002/08/21 13:37:36  mwyrick
// Acquisition Logic Linux Driver
//
//
//-----------------------------------------------------------------------------
// DMASTATUS >= 0 is location in Buffer of good data
#define DMASTATUS_DONE	 	-1
#define DMASTATUS_INPROGRESS 	-2
#define DMASTATUS_ABORTING	-3
#define DMASTATUS_ERROR         -4

#define PLX_LAS0RR	0x00
#define PLX_LAS0BA	0x04
#define PLX_MARBR	0x08
#define PLX_BIGEND	0x0C
#define PLX_LMISC	0x0D
#define PLX_PROT_AREA	0x0E
#define PLX_EROMRR	0x10
#define PLX_EROMBA	0x14
#define PLX_LBRD0	0x18
#define PLX_DMRR	0x1C
#define PLX_DMLBAM	0x20
#define PLX_DMLBAI	0x24
#define PLX_DMPBAM	0x28
#define PLX_DMCFGA	0x2C
#define PLX_LAS1RR	0xF0
#define PLX_LAS1BA	0xF4
#define PLX_LBRD1	0xF8
#define PLX_DMDAC	0xFC
#define PLX_MBOX0	0x40
#define PLX_MBOX1	0x44
#define PLX_MBOX2	0x48
#define PLX_MBOX3	0x4C
#define PLX_MBOX4	0x50
#define PLX_MBOX5	0x54
#define PLX_MBOX6	0x58
#define PLX_MBOX7	0x5C
#define PLX_P2LDBELL	0x60
#define PLX_L2PDBELL	0x64
#define PLX_INTCSR	0x68
#define PLX_CNTRL	0x6C
#define PLX_PCIHIDR	0x70
#define PLX_PCIHREV	0x74
#define PLX_DMAMODE0	0x80
#define PLX_DMAPADR0	0x84
#define PLX_DMALADR0	0x88
#define PLX_DMASIZ0	0x8C
#define PLX_DMADPR0	0x90
#define PLX_DMAMODE1	0x94
#define PLX_DMAPADR1	0x98
#define PLX_DMALADR1	0x9C
#define PLX_DMASIZ1	0xA0
#define PLX_DMADPR1	0xA4
#define PLX_DMACSR0	0xA8
#define PLX_DMACSR1	0xA9
#define PLX_DMAARB	0xAC
#define PLX_DMATHR	0xB0
#define PLX_DMADAC0	0xB4
#define PLX_DMADAC1	0xB8
#define PLX_OPQIS	0x30
#define PLX_OPQIM	0x34
#define PLX_IQP		0x40
#define PLX_OQP		0x44
#define PLX_MQCR	0xC0
#define PLX_QBAR	0xC4
#define PLX_IFHPR	0xC8
#define PLX_IFTPR	0xCC
#define PLX_IPDPR	0xD0
#define PLX_IPTPR	0xD4
#define PLX_OFHPR	0xD8
#define PLX_OFTPR	0xDC
#define PLX_OPDPR	0xE0
#define PLX_OPTPR	0xE4
#define PLX_QSR		0xE8

//DMAMODE defines
#define PLX_8BIT	0x00000000
#define	PLX_16BIT	0x00000001
#define	PLX_32BIT	0x00000002
#define	PLX_0WS		0x00000000
#define	PLX_1WS		0x00000004
#define	PLX_2WS		0x00000008
#define	PLX_3WS		0x0000000C
#define	PLX_4WS		0x00000010
#define	PLX_5WS		0x00000014
#define	PLX_6WS		0x00000018
#define	PLX_7WS		0x0000001C
#define	PLX_8WS		0x00000020
#define	PLX_9WS		0x00000024
#define	PLX_10WS	0x00000028
#define	PLX_11WS	0x0000002C
#define	PLX_12WS	0x00000030
#define	PLX_13WS	0x00000034
#define	PLX_14WS	0x00000038
#define	PLX_15WS	0x0000003C
#define	PLX_TARDY	0x00000040
#define PLX_BTERM	0x00000080
#define	PLX_LOCBURS	0x00000100
#define	PLX_SCATTER 	0x00000200
#define	PLX_DINT	0x00000400
#define	PLX_LOCINC	0x00000800
#define	PLX_DEMAND	0x00001000
#define	PLX_INVALIDATE	0x00002000
#define	PLX_EOT		0x00004000
#define	PLX_FASTTERM	0x00008000
#define	PLX_CLEARCOUNT	0x00010000
#define	PLX_PCIINT	0x00020000
#define	PLX_DACCHAIN	0x00040000

//DMADPR defines
#define	PLX_LOCAL	0x00000000
#define	PLX_PCI		0x00000001
#define	PLX_EOC		0x00000002
#define PLX_TINT	0x00000004
#define PLX_READ	0x00000008
#define PLX_WRITE	0x00000000

//DMACSR defines
#define PLX_ENABLE	0x00000001
#define PLX_START	0x00000002
#define PLX_ABORT	0x00000004
#define PLX_CLEARINT	0x00000008
#define PLX_DONE	0x00000010

//INTCSR
#define PLX_TEAIE	0x00000001
#define PLX_TEAE	0x00000002
#define PLX_SERRI	0x00000004
#define PLX_MBIE	0x00000008
#define PLX_PMIE	0x00000010
#define PLX_PMI 	0x00000020
#define PLX_LDPCE 	0x00000040
#define PLX_LDPC	0x00000080
#define PLX_PCIIE	0x00000100
#define PLX_PDBIE	0x00000200
#define PLX_PAIE 	0x00000400
#define PLX_LIIE	0x00000800
#define PLX_RAE		0x00001000
#define PLX_PDBI	0x00002000
#define PLX_PAI 	0x00004000
#define PLX_LII		0x00008000
#define PLX_LOIE	0x00010000
#define PLX_LDBIE	0x00020000
#define PLX_DMA0IE	0x00040000
#define PLX_DMA1IE	0x00080000
#define PLX_LDBI	0x00100000
#define PLX_DMA0I	0x00200000
#define PLX_DMA1I	0x00400000
#define PLX_BISTI	0x00800000
#define PLX_PCIABORT	0x01000000
#define PLX_DMA0ABORT	0x02000000
#define PLX_DMA1ABORT	0x04000000
#define PLX_256ABORT	0x08000000
#define PLX_PMB0	0x10000000
#define PLX_PMB1	0x20000000
#define PLX_PMB2	0x40000000
#define PLX_PMB3	0x80000000
