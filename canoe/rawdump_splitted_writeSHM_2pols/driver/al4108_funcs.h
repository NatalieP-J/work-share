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
// $Id: al4108_funcs.h,v 1.2 2004/12/22 19:29:06 mwyrick Exp $
// $Log: al4108_funcs.h,v $
// Revision 1.2  2004/12/22 19:29:06  mwyrick
// Working on Multi Board
//
// Revision 1.1.1.1  2004/12/16 14:27:28  mwyrick
// ALLinux 2004
//
// Revision 1.1.1.1  2004/04/29 19:20:14  mwyrick
// AcqLog Linux Driver
//
// Revision 1.1  2004/03/18 17:34:41  mwyrick
// Interm but AL4108 loads
//
//
//-----------------------------------------------------------------------------
static void initAL4108(int);
static int Upload4108RBF(int, char *data, long size);
static void AL4108_BrdAbortDMA(int);
