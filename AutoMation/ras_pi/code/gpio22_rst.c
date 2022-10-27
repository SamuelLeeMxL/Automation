/******************************************************************************

  Copyright (c) 2014 Lantiq Deutschland GmbH
  Copyright 2016, Intel Corporation.

  For licensing information, see the file 'LICENSE' in the root folder of
  this software module.

******************************************************************************/

/**
   \file ethswbox.c
   
*/
#include "os_linux.h"
#include <windows_stub.h>
#include <stdio.h>
#include <string.h>
#include <signal.h>
#include <gpy211.h>
//#include <gpy211_gmac.h>
#include <gpy211_macsec.h>
#include "gpy211_utility.h"

#include "gpy211_utility_gpy2xx.h"
#include "gpy211_utility_common.h"
#include "user_mdio_interface.h"

#include <inttypes.h>
#include "api_gpy.h"

#include "gpy211_common.h"
#include "gpy211_phy.h"
#include "gpy211_regs.h"

#include "conf_if.h"

int main(int argc, char *argv[])
{
   int ret;
  
/* Initialize the BCM mdio library
      Open the mdio
*/      
    if (!bcm2835_init(1))
	return 1;
   
	bcm2835_gpio_fsel(22, BCM2835_GPIO_FSEL_OUTP);
 
    /*  with a pullup */
    bcm2835_gpio_set_pud(22, BCM2835_GPIO_PUD_UP);

	bcm2835_gpio_write(22, 1);
	bcm2835_gpio_write(22, 0);
	udelay(800000u);
	bcm2835_gpio_write(22, 1);
	udelay(1000000u);
			
   return 0;         
}
