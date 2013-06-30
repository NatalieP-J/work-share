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
// $Id: al212.h,v 1.1.1.1 2004/12/16 14:27:28 mwyrick Exp $
// $Log: al212.h,v $
// Revision 1.1.1.1  2004/12/16 14:27:28  mwyrick
// ALLinux 2004
//
// Revision 1.2  2004/10/06 13:53:13  mwyrick
// Added Proper Support for AL212.
// Changed the ResetPLX to reload the config from the EEPROM
// Made DMA Buffer size 8 Megs, there seems to be a problem when its
// larger than that.
//
// Revision 1.1.1.1  2004/04/29 19:20:14  mwyrick
// AcqLog Linux Driver
//
//
//-----------------------------------------------------------------------------
#define AL212_FSR		0x0A

