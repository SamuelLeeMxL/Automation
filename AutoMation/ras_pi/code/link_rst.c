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


int main(int argc, char *argv[])
{
   int ret;
   struct gpy211_device* p_phy0;
   struct gpy211_device* p_phy1;
   struct gpy211_device* p_phy2;
   struct gpy211_device* p_phy3;

/* Initialize the BCM mdio library
      Open the mdio
      
   bcm2835_init (RPI4B_GPIO_MEM);
   ret = mdio_open(RPI4B_GPIO_MDIO_CLK_PIN, RPI4B_GPIO_MDIO_DATA_PIN);
*/


   p_phy0 = (struct gpy211_device*)api_gpy_open (0, 1, 28);
   p_phy1 = (struct gpy211_device*)api_gpy_open (1, 2, 29);
   p_phy2 = (struct gpy211_device*)api_gpy_open (2, 3, 30);
   p_phy3 = (struct gpy211_device*)api_gpy_open (3, 4, 31);

printf("\t%30s:\t%d\n", "1", p_phy0->phy_addr);
printf("\t%30s:\t%d\n", "2", p_phy1->phy_addr);
printf("\t%30s:\t%d\n", "3", p_phy2->phy_addr);
printf("\t%30s:\t%d\n", "3", p_phy3->phy_addr);
   
   ret = gpy2xx_init(p_phy0);
	if (ret < 0)
		printf("\nERROR: GPY0 init failed.\n");

   ret = gpy2xx_init(p_phy1);
	if (ret < 0)
		printf("\nERROR: GPY1 init failed.\n");

   ret = gpy2xx_init(p_phy2);
	if (ret < 0)
		printf("\nERROR: GPY2 init failed.\n");

   ret = gpy2xx_init(p_phy3);
	if (ret < 0)
		printf("\nERROR: GPY2 init failed.\n");

	u16 status, count_test=0;
	
	while (1)
	{
		count_test++;
		printf("\t%30s:\t%d\n", "Test time", count_test);
		u16 i;
		u16 link_check_count, count_error=0;
		// check pma/pcs link status	
		
		do {
			link_check_count=0;
			status = PHY_READ(p_phy0, STD_STD_STAT);
			if (status !=0x796d) {
			//	printf("\t%40s:\t0x%x\n", "Slice0 status", status);
				link_check_count++;
				count_error++;
			}
			status = PHY_READ(p_phy1, STD_STD_STAT);
			if (status !=0x796d) {
			//	printf("\t%40s:\t0x%x\n", "Slice1 status", status);
				link_check_count++;
				count_error++;
			}
			
			status = PHY_READ(p_phy2, STD_STD_STAT);
			if (status !=0x796d) {
			//	printf("\t%40s:\t0x%x\n", "Slice2 status", status);
				link_check_count++;
				count_error++;
			}
			
			status = PHY_READ(p_phy3, STD_STD_STAT);
			if (status !=0x796d) {
			//	printf("\t%40s:\t0x%x\n", "Slice3 status", status);
				link_check_count++;
				count_error++;
			}

			if(link_check_count != 0  )	
				printf("\t%40s:\t%d\n", "No link now, wait: ", count_error);
			
			if (count_error > 300) {
				status = PHY_READ(p_phy0, STD_STD_STAT);
				if (status !=0x796d) {
					printf("\t%40s:\t0x%x\n", "Slice0 status", status);
					count_error++;
				}
				status = PHY_READ(p_phy1, STD_STD_STAT);
				if (status !=0x796d) {
					printf("\t%40s:\t0x%x\n", "Slice1 status", status);
					count_error++;
				}
				
				status = PHY_READ(p_phy2, STD_STD_STAT);
				if (status !=0x796d) {
					printf("\t%40s:\t0x%x\n", "Slice2 status", status);
					count_error++;
				}
				
				status = PHY_READ(p_phy3, STD_STD_STAT);
				if (status !=0x796d) {
					printf("\t%40s:\t0x%x\n", "Slice3 status", status);
					count_error++;
				}
				
				status = PHY_READ(p_phy0, 0x16*2);
					printf("%s:0x%x ", "PHY_RES1", status);
				status = PHY_READ(p_phy1, 0x16*2);
					printf("0x%x ", status);
				status = PHY_READ(p_phy2, 0x16*2);
					printf("0x%x ", status);
				status = PHY_READ(p_phy3, 0x16*2);
					printf("0x%x \n", status);

				status = PHY_READ(p_phy0, 0x17*2);
					printf("%s:0x%x ", "PHY_RES2", status);
				status = PHY_READ(p_phy1, 0x17*2);
					printf("0x%x ", status);
				status = PHY_READ(p_phy2, 0x17*2);
					printf("0x%x ", status);
				status = PHY_READ(p_phy3, 0x17*2);
					printf("0x%x \n", status);

				status = PHY_READ(p_phy0, 0x1f*2);
					printf("%s:0x%x ", "PHY_TEST", status);
				status = PHY_READ(p_phy1, 0x1f*2);
					printf("0x%x ", status);
				status = PHY_READ(p_phy2, 0x1f*2);
					printf("0x%x ", status);
				status = PHY_READ(p_phy3, 0x1f*2);
					printf("0x%x \n", status);

				status = PHY_READ_MMD(p_phy0, 0x1f , 0xff4*2 );
					printf("%s:0x%x ", "PDI_PS_ANEG", status);
				status = PHY_READ_MMD(p_phy1, 0x1f , 0xff4*2 );
					printf("0x%x ", status);
				status = PHY_READ_MMD(p_phy2, 0x1f , 0xff4*2 );
					printf("0x%x ", status);
				status = PHY_READ_MMD(p_phy3, 0x1f , 0xff4*2 );
					printf("0x%x \n", status);
				
				status = PHY_READ_MMD(p_phy0, 0x1f , 0xff2*2 );
					printf("%s:0x%x ", "PDI_PS_P1A", status);
				status = PHY_READ_MMD(p_phy1, 0x1f , 0xff2*2 );
					printf("0x%x ", status);
				status = PHY_READ_MMD(p_phy2, 0x1f , 0xff2*2 );
					printf("0x%x ", status);
				status = PHY_READ_MMD(p_phy3, 0x1f , 0xff2*2 );
					printf("0x%x \n", status);
				
			
				return 0;
			}
									
			udelay(1000000u);
		}while(link_check_count != 0  );

		
		if ( count_test > 2000 )
			break;

#if 1
		bcm2835_gpio_write(22, 1);
		bcm2835_gpio_fsel(22, BCM2835_GPIO_FSEL_OUTP);
		bcm2835_gpio_write(22, 0);
		udelay(800000u);
		bcm2835_gpio_write(22, 1);
		
		udelay(1000000u);
#endif
	//	SMDIO_WRITE(p_phy0, GPIO_PDI_REGISTERS_GPIO_PDI_REGISTERS_GPIO_ALTSEL1, 0xf3f3);
	//		PHY_WRITE(p_phy3, PHY_PHY_CTL1, 0x0);   // Disable AMDIX , MDI normal
	//		PHY_WRITE(p_phy2, PHY_PHY_CTL1, 0xc);   // Disable AMDIX , MDI cross A/B , C/D swap
	//	 PHY_WRITE(p_phy3, STD_CTRL, 0x3240);   // Re-ANEG
	//	 PHY_WRITE(p_phy2, STD_CTRL, 0x3240);   // Re-ANEG
		// SMDIO_WRITE(p_phy0, TOP_PDI_REGISTERS_TOP_SLICE_IF, 0x0002);
		udelay(800000u);
		/*
		mdio_c22_write(17, 27,  29, 0, STD_CTRL_PD_MASK);
		udelay(800000u);
		mdio_c22_write(17, 27,  30, 0, STD_CTRL_PD_MASK);		
		udelay(800000u);
		mdio_c22_write(17, 27,  31, 0, STD_CTRL_PD_MASK);
		udelay(1000000u);	
		mdio_c22_write(17, 27,  29, 0, 0x3040);
		udelay(800000u);
		mdio_c22_write(17, 27,  30, 0, 0x3040);		
		udelay(800000u);
		mdio_c22_write(17, 27,  31, 0, 0x3040);
		*/
		// PHY_WRITE(p_phy2, STD_STD_CTRL, 0x3240);
		udelay(7000000u);


	};
		
   return 0;         
}
