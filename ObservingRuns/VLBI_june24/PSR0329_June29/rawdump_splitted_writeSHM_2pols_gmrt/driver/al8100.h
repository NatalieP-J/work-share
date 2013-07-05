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
// $Id: al8100.h,v 1.1.1.1 2004/12/16 14:27:28 mwyrick Exp $
// $Log: al8100.h,v $
// Revision 1.1.1.1  2004/12/16 14:27:28  mwyrick
// ALLinux 2004
//
// Revision 1.1.1.1  2004/04/29 19:20:14  mwyrick
// AcqLog Linux Driver
//
// Revision 1.9  2002/11/27 15:32:17  mwyrick
// Good Working Version
//
// Revision 1.8  2002/11/19 21:22:27  mwyrick
// Working with AL8100 to download Waveforms
//
// Revision 1.7  2002/11/19 15:16:48  mwyrick
// no message
//
// Revision 1.6  2002/10/24 15:59:48  mwyrick
// Clean up under way
// NO boards except ALTLS
//
// Revision 1.5  2002/10/16 16:06:29  mwyrick
// ----------------------------------------------------------------
// Moved All Files into one compile so every function can be Static
// ----------------------------------------------------------------
//
// Revision 1.4  2002/10/16 15:54:35  mwyrick
// Semi-Working SGL
//
// Revision 1.3  2002/10/11 18:20:41  mwyrick
// More Registers
//
// Revision 1.2  2002/10/11 15:01:11  mwyrick
// Moved upload code to seperate files
//
// Revision 1.1.1.1  2002/08/21 13:37:36  mwyrick
// Acquisition Logic Linux Driver
//
//
//-----------------------------------------------------------------------------
#define CONF_OFFSET		0xFB
#define CONF_MASK		0x0D
#define CONF_START		0x00
#define CONF_NEXT		0x05
#define CONF_ERROR		0x01
#define CONF_DONE		0x0D

#define AL8100_FSR		0x0A
#define AL8100_SWTRIGGER  	0x97

