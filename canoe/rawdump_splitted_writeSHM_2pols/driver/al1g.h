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
// $Id: al1g.h,v 1.1.1.1 2004/12/16 14:27:28 mwyrick Exp $
// $Log: al1g.h,v $
// Revision 1.1.1.1  2004/12/16 14:27:28  mwyrick
// ALLinux 2004
//
// Revision 1.1.1.1  2004/04/29 19:20:14  mwyrick
// AcqLog Linux Driver
//
// Revision 1.6  2002/12/17 19:46:08  mwyrick
// Started Adding AL1G Support
//
//
//-----------------------------------------------------------------------------
#define CONF_OFFSET		0xFB
#define CONF_MASK		0x0D
#define CONF_START		0x00
#define CONF_NEXT		0x05
#define CONF_ERROR		0x01
#define CONF_DONE		0x0D

#define AL1_FSR			0x0A

