cmake_minimum_required(VERSION 3.1)
project(EthSwBox VERSION 0.0.1
                  DESCRIPTION "Ethernet SW Toolbox"
                  LANGUAGES C)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} 
      ${CMAKE_CURRENT_SOURCE_DIR})


include_directories (src
                     src/conf
                     src/os
		             src/phy/mdio/lib   
                     src/api/gsw/src/include
                     src/api 
                     src/api/gpy/src/inc 
                     src/api/gpy/src/api/phy 
                     src/api/gpy/src/os/linux
                     src/api/gpy/utility/wip
                     src/api/gpy/ISC-DDK-160-BSD_v2.3/SafeXcel-IP-160_DDK_v2.3/Kit/SABuilder_MACsec/Example_AES/incl                      
                     src/fapi/mdio
                     src/fapi/ffu
                     src/cli
                     src/cli/cmds
                     src/apps)


#####################
#   OS library     #
#####################
SET (os_DIR src/os)

SET (os_SRCS  ${os_DIR}/os_linux.c)

add_library (os ${os_SRCS})


#####################
#   CLI library     #
#####################
SET (cli_DIR src/cli)

SET (cli_SRCS ${cli_DIR}/cmds/cmds.c
              ${cli_DIR}/cmds/cmds_apps.c
              ${cli_DIR}/cmds/cmds_fapi.c)

add_library (cli ${cli_SRCS})


#####################
#   APPS library    #
#####################
SET (apps_DIR src/apps)

SET (apps_SRCS ${apps_DIR}/apps_tools_gpy.c)
              
add_library (apps ${apps_SRCS})



#########################
#   FAPI FFU library    #
#########################
SET (fapi_ffu_DIR src/fapi/ffu)

SET (fapi_ffu_SRCS ${fapi_ffu_DIR}/fapi_gpy_ffu.c)

add_library (fapi_ffu ${fapi_ffu_SRCS})


#########################
#   FAPI MDIO library   #
#########################
SET (fapi_mdio_DIR src/fapi/mdio)

SET (fapi_mdio_SRCS ${fapi_mdio_DIR}/fapi_mdio.c)

add_library (fapi_mdio ${fapi_mdio_SRCS})



#########################
#   API GPY library     #
#########################
SET (api_gpy_DIR src/api/gpy)

SET (api_gpy_SRCS ${api_gpy_DIR}/../api_gpy.c
                  ${api_gpy_DIR}/src/api/phy/gpy211_phy.c
                  ${api_gpy_DIR}/src/api/phy/gpy211_chip.c                  
                  ${api_gpy_DIR}/src/api/macsec/gpy211_macsec.c
                  ${api_gpy_DIR}/ISC-DDK-160-BSD_v2.3/SafeXcel-IP-160_DDK_v2.3/Kit/SABuilder_MACsec/Example_AES/src/aes.c
                  ${api_gpy_DIR}/utility/wip/user_mdio_interface.c
                  ${api_gpy_DIR}/utility/wip/gpy211_utility_gpy2xx.c
                  ${api_gpy_DIR}/utility/wip/gpy211_utility_common.c
                  ${api_gpy_DIR}/utility/wip/gpy211_utility_f24s.c
                  ${api_gpy_DIR}/utility/wip/gpy211_utility_pg31.c
                  ${api_gpy_DIR}/utility/wip/gpy211_utility_uart.c
                  ${api_gpy_DIR}/utility/wip/gpy211_utility_cmdprocessor.c
                  ${api_gpy_DIR}/utility/wip/gpy211_utility_gpy211_menu.c
                  ${api_gpy_DIR}/utility/wip/gpy211_utility_main.c
                  ${api_gpy_DIR}/utility/wip/gpy211_utility_system.c
    )

add_library (api_gpy ${api_gpy_SRCS})


#########################
#   API GSW library     #
#########################
SET (api_gsw_DIR src/api/gsw)

#SET (api_gsw_SRCS ${api_gsw_DIR}/src/gsw_api_func.c
#                  ${api_gsw_DIR}/src/gsw_core.c
#                  ${api_gsw_DIR}/src/gsw_io_wrap.c
#                  ${api_gsw_DIR}/src/gsw_sw_init.c
#                  ${api_gsw_DIR}/src/gsw_multi.c
#                  ${api_gsw_DIR}/src/gsw_pce.c
#                  ${api_gsw_DIR}/src/gsw_qos.c
#                  ${api_gsw_DIR}/src/gsw_vlan.c)

#add_library (api_gsw ${api_gsw_SRCS})

#########################
#   PHY MDIO library    #
#########################
SET (phy_mdio_DIR src/phy/mdio)

SET (phy_mdio_SRCS ${phy_mdio_DIR}/lib/bcm2835.c
              ${phy_mdio_DIR}/lib/mdio.c)

add_library (phy_mdio ${phy_mdio_SRCS})


#########################
#   BINDINGS library    #
#########################
#add_library (cbindings ${fapi_ffu_SRCS} ${cli_DIR}/wb/vita_target_os_linux.c ${api_gpy_SRCS} ${phy_mdio_SRCS})

set(CURSES_USE_NCURSES TRUE)
find_package(Curses REQUIRED)
include_directories(${CURSES_INCLUDE_DIR})

find_package(Readline)
include_directories(${Readline_INCLUDE_DIR})

#############################   
#   ethswbox application    # 
#############################
add_executable(ethswbox ${cli_DIR}/ethswbox.c)

#target_link_libraries(ethswbox os cli_wb fapi_ffu api_gpy api_gsw phy_mdio)
#target_link_libraries(ethswbox os fapi_ffu api_gpy api_gsw phy_mdio)
target_link_libraries(ethswbox cli apps fapi_mdio fapi_ffu api_gpy phy_mdio os ${CURSES_LIBRARY} ${Readline_LIBRARY})

#############################   
#   pctools application    # 
#############################

add_executable(pctool ${cli_DIR}/pctool.c)
#target_link_libraries(ethswbox os cli_wb fapi_ffu api_gpy api_gsw phy_mdio)
#target_link_libraries(ethswbox os fapi_ffu api_gpy api_gsw phy_mdio)
target_link_libraries(pctool cli apps fapi_mdio fapi_ffu api_gpy phy_mdio os ${CURSES_LIBRARY} ${Readline_LIBRARY})

#############################   
#   pctools application    # 
#############################

add_executable(gpio22_rst ${cli_DIR}/gpio22_rst.c)
#target_link_libraries(ethswbox os cli_wb fapi_ffu api_gpy api_gsw phy_mdio)
#target_link_libraries(ethswbox os fapi_ffu api_gpy api_gsw phy_mdio)
target_link_libraries(gpio22_rst cli apps fapi_mdio fapi_ffu api_gpy phy_mdio os ${CURSES_LIBRARY} ${Readline_LIBRARY})
