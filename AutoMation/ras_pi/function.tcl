####################################################################################
#                                                                                  #
# IxTclHAL Version :5.20.0.165                                                     #
# Product version :5.20.0 Build 165#                                               #
# File: IxSampleTCL.tcl                                                            #
#                                                                                  #
# Copyright © 1997 - 2009 by IXIA                                                  #
# All Rights Reserved.                                                             #
#                                                                                  #
# The following is an example of how streams, ports and filters are configured,    #
# data capture started, transmission started and statistics collected.             #
# The chassis is connected to first, streams are created, filters are set,         #
# then capture is started on Rx port and transmisssion is started on Tx port.      #
# After the transmition is complete, some statistics are collected and             #
# displayed to standard out.                                                       #
#                                                                                  #
# Note: This test requires two ports which should be connected via loopback cable. #
#                                                                                  #
####################################################################################

# ################################################################################
# # IXIA Variable define
# ################################################################################
source "C:\\Program Files (x86)\\Ixia\\IxOS\\9.00.1900.24\\TclScripts\\bin\\IxiaWish.tcl"

package req IxTclHal
package require logger

# option 0 : IXIA_IP
# option 1 : IXIA_ports
# option 2 : Function_Name
# option 3 : Packet_Size
# option 4 : DurationMS
# option 5 : MasterSlave
# option 6 : CableRelay_Port
# option 7 : PortSpeed
# option 8 : Number
# option 9 : TestTemp
# option 10: Loopback_YorN

#::hostname# set ::IXIA_IP [lindex $argv 0] over
#::port# set ::IXIA_Ports [lindex $argv 1] over
#::mode# set ::Function_Name [lindex $argv 2] over
#::detail# set ::Packet_Size [lindex $argv 3] over
# set ::DurationMS [lindex $argv 4] over
#::masterslave# set ::MasterSlave [lindex $argv 5] over           
#::csport# set ::CableRelay_Port [lindex $argv 6] over
#::portspeed# set ::PortSpeed [lindex $argv 7] over       
#::number# set ::Number [lindex $argv 8]
# set ::TestTemp [lindex $argv 9]    

set ::IXIA_IP [lindex $argv 0]
set ::card 2
set ::IXIA_Ports [lindex $argv 1]
set ::Function_Name [lindex $argv 2]
set ::Packet_Size [lindex $argv 3]

# DataPattem = 5  -> Repeating
# DataPattem = 4  -> Random
set ::DataPattem_Mode [lindex $argv 4]
set ::DurationMS [lindex $argv 5]

set ::MasterSlave [lindex $argv 6]
set ::CableRelay_Port [lindex $argv 7]
set ::PortSpeed [lindex $argv 8]
set ::Number [expr [lindex $argv 9]]
set ::TestTemp [lindex $argv 10] 


set ::summary ""
set ::summary_result ""
set ::speed_Check [string range $::PortSpeed 5 end]
set ::link_start 0
set ::link_end 0
set ::duration 0
set ::resultQQ ""

proc init {} {

puts "IXIA_IP = $::IXIA_IP"
puts "card = $::card"
puts "port = $::IXIA_Ports"
#puts "port1 = $::port1"
#puts "port2 = $::port2"
puts "mode = $::Function_Name"
puts "masterslave = $::MasterSlave"
puts "csport = $::CableRelay_Port"
puts "portspeed = $::PortSpeed"
puts "number = $::Number"

# ################################################################################
# # IXIA port and Connect to IxNet client
# ################################################################################

set userName "IxiaTclUser"

set ::retCode $::TCL_OK
ixConnectToTclServer $::IXIA_IP
ixLogin $userName
ixConnectToChassis $::IXIA_IP
#puts "sam debug 1111111111"
puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] User logged in as: $userName"
#puts "sam debug 2222222222"
set chasId [ixGetChassisID $::IXIA_IP]
#puts "sam debug 3333333333"

#$::IXIA_Ports transfer (A->10,B->11,C->12,D->13,E->14,F->15,G->16)
set i 0
while {$i<[string length $::IXIA_Ports]} {
	set a [string index $::IXIA_Ports $i]
	switch $a {
		0 {
		
		}
		A {
			lappend ::portList [list $chasId $::card 10]
		}
		B {
			lappend ::portList [list $chasId $::card 11]
		}
		C {
			lappend ::portList [list $chasId $::card 12]
		}
		D {
			lappend ::portList [list $chasId $::card 13]
		}
		E {
			lappend ::portList [list $chasId $::card 14]
		}
		F {
			lappend ::portList [list $chasId $::card 15]
		}
		G {
			lappend ::portList [list $chasId $::card 16]
		}
		default {
			lappend ::portList [list $chasId $::card $a]
		}
	}
	incr i 1
}

puts "portList = $::portList"
puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] Ixia Tcl Sample Script"

}
proc clearOwnershipAndLogout {} {
    ixClearOwnership $::portList
    # Log off user
    ixLogout
    cleanUp
}
proc set_IXIA_Hardware {} {
	ixPuts "set_IXIA_Hardware_1 = $::portList"
	ixPuts "portList = $::portList"
	set portList $::portList 
# Display version information
	ixPuts "\nIxTclHAL Version :[version cget -ixTclHALVersion]"
	ixPuts "Product version :[version cget -productVersion]"
	ixPuts "Installed version :[version cget -installVersion]\n"

# Set ports to factory defaults. Dumps out on error.
	ixPuts "Setting ports to factory defaults..."
	foreach item $portList {
	
		scan $item "%d %d %d" chasId card port
		ixPuts "chasId card port = $chasId $card $port"
		if [port setFactoryDefaults $chasId $card $port] {
			errorMsg "Error setting factory defaults on $chasId.$card.$port]."
			clearOwnershipAndLogout
			return $::TCL_ERROR
		}
	}

	# Config port properties
	# ######
	# ######
	# ######

	foreach item $portList {
		scan $item "%d %d %d" chasId card port
		#ixPuts "portPhyModeCopper = $::portPhyModeCopper"
		#set $::portPhyModeCopper 1
		# Cange port physical mode to copper
		if {[port setPhyMode $::portPhyModeCopper $chasId $card $port]} {
			errorMsg "Error calling port setPhyMode $::portPhyModeCopper $chasId $card $port"
			clearOwnershipAndLogout
			set ::retCode $::TCL_ERROR
		}
		## sam debug
		# ixPuts "sam debug card= $card"
		# ixPuts "sam debug port= $port"
		if {$::PortSpeed == "speed2500"} {
			port config -speed                              2500
		} 
		if {$::PortSpeed == "speed1000"} {
			port config -speed                              1000
		}
		if {$::PortSpeed == "speed100"} {
			port config -speed                              100
		}
		if {$::PortSpeed == "speed10"} {
			port config -speed                              10
		}
		#port config -duplex full
		port config -flowControl                        true
		port config -directedAddress  "01 80 C2 00 00 02"
		#port config -multicastPauseAddress  "01 80 C2 00 00 01"
		#port config -loopback portNormal
		port config -transmitMode                       portTxPacketStreams
		port config -receiveMode                        [expr $::portCapture|$::portRxModeWidePacketGroup]
		port config -autonegotiate                      true
		if {$::PortSpeed == "speed2500"} {
			port config -advertise100FullDuplex             false
			port config -advertise100HalfDuplex             false
			port config -advertise10FullDuplex              false
			port config -advertise10HalfDuplex              false
			port config -advertise1000FullDuplex            false
			#port config -advertise5FullDuplex true
			port config -advertise2P5FullDuplex true
		} 
		if {$::PortSpeed == "speed1000"} {
			port config -advertise100FullDuplex             false
			port config -advertise100HalfDuplex             false
			port config -advertise10FullDuplex              false
			port config -advertise10HalfDuplex              false
			port config -advertise1000FullDuplex            true
			#port config -advertise5FullDuplex true
			port config -advertise2P5FullDuplex false
		}
		if {$::PortSpeed == "speed100"} {
			port config -advertise100FullDuplex             true
			port config -advertise100HalfDuplex             false
			port config -advertise10FullDuplex              false
			port config -advertise10HalfDuplex              false
			port config -advertise1000FullDuplex            false
			#port config -advertise5FullDuplex true
			port config -advertise2P5FullDuplex false
		}
		if {$::PortSpeed == "speed10"} {
			port config -advertise100FullDuplex             false
			port config -advertise100HalfDuplex             false
			port config -advertise10FullDuplex              true
			port config -advertise10HalfDuplex              false
			port config -advertise1000FullDuplex            false
			#port config -advertise5FullDuplex true
			port config -advertise2P5FullDuplex false
		}
		
		#port config -portMode portEthernetMode
		#port config -enableDataCenterMode false
		#port config -dataCenterMode eightPriorityTrafficMapping
		#port config -flowControlType ieee8023x
		#port config -pfcEnableValueListBitMatrix  ""
		#port config -pfcResponseDelayEnabled 0
		#port config -pfcResponseDelayQuanta 0
		#port config -rxTxMode gigNormal
		#port config -ignoreLink false
		#port config -advertiseAbilities portAdvertiseNone
		#port config -timeoutEnable true
		port config -negotiateMasterSlave               1
		port config -masterSlave                        $::MasterSlave
		#port config -pmaClock pmaClockAutoNegotiate
		#port config -enableSimulateCableDisconnect false
		#port config -enableAutoDetectInstrumentation false
		#port config -autoDetectInstrumentationMode portAutoInstrumentationModeEndOfFrame
		#port config -enableRepeatableLastRandomPattern false
		#port config -transmitClockDeviation 0
		#port config -transmitClockMode portClockInternal
		#port config -preEmphasis preEmphasis0
		port config -transmitExtendedTimestamp          1
		#port config -enableFramePreemption false
		#port config -enableSmdVRExchange false
		#port config -operationModeList  [list]
		#port config -MacAddress  "00 de bb 00 00 01"
		#port config -DestMacAddress  "00 de bb 00 00 02"
		#port config -name  ""
		#port config -numAddresses 1
		#port config -enableManualAutoNegotiate false
		#port config -enablePhyPolling true
		#port config -enableTxRxSyncStatsMode false
		#port config -txRxSyncInterval 0
		#port config -enableTransparentDynamicRateChange false
		#port config -enableDynamicMPLSMode false
		#port config -enablePortCpuFlowControl false
		#port config -portCpuFlowControlDestAddr  "01 80 C2 00 00 02"
		#port config -portCpuFlowControlSrcAddr  "00 00 01 00 02 00"
		port config -portCpuFlowControlPriority         "1 1 1 1 1 1 1 1"
		#port config -portCpuFlowControlType 0
		#port config -enableWanIFSStretch false
		#port config -enableRestartStream false
		#port config -enableRxNonIEEEPreamble false
		#port config -enableRsFec false
		#port config -enableRsFecStats false
		#port config -enableLinkTraining false
		#port config -ieeeL1Defaults 0
		#port config -firecodeRequest 1
		#port config -firecodeAdvertise 1
		#port config -firecodeForceOn 0
		#port config -firecodeForceOff 0
		#port config -reedSolomonRequest 0
		#port config -reedSolomonAdvertise 0
		#port config -reedSolomonForceOn 0
		#port config -reedSolomonForceOff 0
		#port config -autoCtleAdjustment 0
		#port config -overrideLtTapSettings 0
		#port config -negotiatedCapability  ""
		#port config -am100GTwoLane 0
		if {[port set $chasId $card $port]} {
			errorMsg "Error calling port set $chasId $card $port"
			set ::retCode $::TCL_ERROR
		}
	
		stat setDefault 
		#stat config -mode statNormal
		#stat config -enableValidStats false
		#stat config -enableProtocolServerStats true
		#stat config -enableArpStats true
		#stat config -enablePosExtendedStats true
		#stat config -enableDhcpStats false
		#stat config -enableDhcpV6Stats false
		#stat config -enableEthernetOamStats false
		#stat config -enableFcoeStats false
		#stat config -fcoeRxSharedStatType1 statFcoeValidFrames
		#stat config -fcoeRxSharedStatType2 statFcoeValidFrames
		#stat config -enableLldpDcbxStats false
		stat config -enableBgpStats                     false
		#stat config -enableIcmpStats true
		stat config -enableOspfStats                    false
		stat config -enableIsisStats                    false
		stat config -enableRsvpStats                    false
		stat config -enableLdpStats                     false
		stat config -enableIgmpStats                    false
		stat config -enableOspfV3Stats                  false
		stat config -enablePimsmStats                   false
		stat config -enableMldStats                     false
		stat config -enableStpStats                     false
		stat config -enableEigrpStats                   false
		stat config -enableBfdStats                     false
		stat config -enableCfmStats                     false
		stat config -enableLacpStats                    false
		stat config -enableOamStats                     false
		stat config -enableMplsTpStats                  false
		stat config -enableElmiStats                    false
		if {[stat set $chasId $card $port]} {
			errorMsg "Error calling stat set $chasId $card $port"
			set ::retCode $::TCL_ERROR
		}
	
		packetGroup setDefault 
		#packetGroup config -signatureOffset 48
		#packetGroup config -signature  "08 71 18 05"
		#packetGroup config -insertSignature false
		#packetGroup config -ignoreSignature false
		#packetGroup config -groupId 0
		#packetGroup config -groupIdOffset 52
		#packetGroup config -enableGroupIdMask false
		#packetGroup config -enableInsertPgid true
		packetGroup config -groupIdMask                        4293918720
		#packetGroup config -latencyControl cutThrough
		#packetGroup config -measurementMode packetGroupModeLatency
		#packetGroup config -delayVariationMode delayVariationWithSequenceErrors
		#packetGroup config -preambleSize 8
		#packetGroup config -sequenceNumberOffset 44
		#packetGroup config -sequenceErrorThreshold 2
		#packetGroup config -insertSequenceSignature false
		#packetGroup config -allocateUdf true
		#packetGroup config -enableSignatureMask false
		#packetGroup config -signatureMask  "00 00 00 00"
		#packetGroup config -enableRxFilter false
		#packetGroup config -headerFilter  "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
		#packetGroup config -headerFilterMask  "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
		packetGroup config -enable128kBinMode                  true
		#packetGroup config -enableTimeBins false
		#packetGroup config -numPgidPerTimeBin 32
		packetGroup config -numTimeBins                        1
		#packetGroup config -timeBinDuration 1000000
		#packetGroup config -enableLatencyBins false
		#packetGroup config -latencyBinList  ""
		#packetGroup config -enableSizeBins false
		#packetGroup config -sizeBinList  ""
		#packetGroup config -groupIdMode packetGroupCustom
		#packetGroup config -sequenceCheckingMode seqThreshold
		#packetGroup config -multiSwitchedPathMode seqSwitchedPathPGID
		#packetGroup config -pgidStatMode 0
		#packetGroup config -enableLastBitTimeStamp false
		#packetGroup config -seqAdvTrackingLateThreshold 1000
		#packetGroup config -enableReArmFirstTimeStamp false
		if {[packetGroup setRx $chasId $card $port]} {
			errorMsg "Error calling packetGroup setRx $chasId $card $port"
			set ::retCode $::TCL_ERROR
		}
	
		linkFaultSignaling setDefault 
		#linkFaultSignaling config -contiguousErrorBlocks 4
		#linkFaultSignaling config -contiguousGoodBlocks 0
		#linkFaultSignaling config -sendSetsMode linkFaultAlternateOrderedSets
		#linkFaultSignaling config -loopCount 1
		#linkFaultSignaling config -enableLoopContinuously true
		#linkFaultSignaling config -enableTxIgnoresRxLinkFault false
		#linkFaultSignaling config -orderedSetTypeA linkFaultLocal
		#linkFaultSignaling config -orderedSetTypeB linkFaultRemote
		if {[linkFaultSignaling set $chasId $card $port]} {
			errorMsg "Error calling linkFaultSignaling set $chasId $card $port"
			set ::retCode $::TCL_ERROR
		}
	
		filter setDefault 
		#filter config -captureTriggerDA anyAddr
		#filter config -captureTriggerSA anyAddr
		#filter config -captureTriggerPattern anyPattern
		#filter config -captureTriggerError errAnyFrame
		#filter config -captureTriggerFrameSizeEnable false
		#filter config -captureTriggerFrameSizeFrom 64
		#filter config -captureTriggerFrameSizeTo 1518
		#filter config -captureTriggerCircuit filterAnyCircuit
		#filter config -captureFilterDA anyAddr
		#filter config -captureFilterSA anyAddr
		#filter config -captureFilterPattern anyPattern
		#filter config -captureFilterError errAnyFrame
		#filter config -captureFilterFrameSizeEnable false
		#filter config -captureFilterFrameSizeFrom 64
		#filter config -captureFilterFrameSizeTo 1518
		#filter config -captureFilterCircuit filterAnyCircuit
		#filter config -userDefinedStat1DA anyAddr
		#filter config -userDefinedStat1SA anyAddr
		#filter config -userDefinedStat1Pattern anyPattern
		#filter config -userDefinedStat1Error errAnyFrame
		#filter config -userDefinedStat1FrameSizeEnable false
		#filter config -userDefinedStat1FrameSizeFrom 64
		#filter config -userDefinedStat1FrameSizeTo 1518
		#filter config -userDefinedStat1Circuit filterAnyCircuit
		#filter config -userDefinedStat2DA anyAddr
		#filter config -userDefinedStat2SA anyAddr
		filter config -userDefinedStat2Pattern            pattern2
		filter config -userDefinedStat2Error              errGoodFrame
		#filter config -userDefinedStat2FrameSizeEnable 0
		#filter config -userDefinedStat2FrameSizeFrom 64
		#filter config -userDefinedStat2FrameSizeTo 1518
		#filter config -userDefinedStat2Circuit filterAnyCircuit
		#filter config -asyncTrigger1DA anyAddr
		#filter config -asyncTrigger1SA anyAddr
		#filter config -asyncTrigger1Pattern anyPattern
		#filter config -asyncTrigger1Error errAnyFrame
		#filter config -asyncTrigger1FrameSizeEnable false
		#filter config -asyncTrigger1FrameSizeFrom 64
		#filter config -asyncTrigger1FrameSizeTo 1518
		#filter config -asyncTrigger1Circuit filterAnyCircuit
		#filter config -asyncTrigger2DA anyAddr
		#filter config -asyncTrigger2SA anyAddr
		#filter config -asyncTrigger2Pattern anyPattern
		#filter config -asyncTrigger2Error errAnyFrame
		#filter config -asyncTrigger2FrameSizeEnable false
		#filter config -asyncTrigger2FrameSizeFrom 64
		#filter config -asyncTrigger2FrameSizeTo 1518
		#filter config -asyncTrigger2Circuit filterAnyCircuit
		#filter config -captureTriggerEnable true
		#filter config -captureFilterEnable true
		#filter config -userDefinedStat1Enable false
		filter config -userDefinedStat2Enable             true
		#filter config -asyncTrigger1Enable false
		#filter config -asyncTrigger2Enable false
		#filter config -userDefinedStat1PatternExpressionEnable false
		#filter config -userDefinedStat2PatternExpressionEnable false
		#filter config -captureTriggerPatternExpressionEnable false
		#filter config -captureFilterPatternExpressionEnable false
		#filter config -asyncTrigger1PatternExpressionEnable false
		#filter config -asyncTrigger2PatternExpressionEnable false
		filter config -userDefinedStat1PatternExpression  ""
		filter config -userDefinedStat2PatternExpression  ""
		filter config -captureTriggerPatternExpression    ""
		filter config -captureFilterPatternExpression     ""
		filter config -asyncTrigger1PatternExpression     ""
		filter config -asyncTrigger2PatternExpression     ""
		if {[filter set $chasId $card $port]} {
			errorMsg "Error calling filter set $chasId $card $port"
			set ::retCode $::TCL_ERROR
		}
	
		filterPallette setDefault 
		#filterPallette config -DA1  "00 00 00 00 00 00"
		#filterPallette config -DAMask1  "00 00 00 00 00 00"
		#filterPallette config -DA2  "00 00 00 00 00 00"
		#filterPallette config -DAMask2  "00 00 00 00 00 00"
		#filterPallette config -SA1  "00 00 00 00 00 00"
		#filterPallette config -SAMask1  "00 00 00 00 00 00"
		#filterPallette config -SA2  "00 00 00 00 00 00"
		#filterPallette config -SAMask2  "00 00 00 00 00 00"
		#filterPallette config -pattern1  "DE ED EF FE AC CA"
		#filterPallette config -patternMask1  "00 00 00 00 00 00"
		filterPallette config -pattern2                           "BE EF 02 07"
		#filterPallette config -patternMask2 00
		#filterPallette config -pattern3  ""
		#filterPallette config -patternMask3  ""
		#filterPallette config -pattern4  ""
		#filterPallette config -patternMask4  ""
		#filterPallette config -patternOffset1 12
		filterPallette config -patternOffset2                     42
		#filterPallette config -patternOffset3 0
		#filterPallette config -patternOffset4 0
		#filterPallette config -matchType1 matchUser
		#filterPallette config -matchType2 matchUser
		#filterPallette config -matchType3 3
		#filterPallette config -matchType4 3
		#filterPallette config -patternOffsetType1 filterPalletteOffsetStartOfFrame
		#filterPallette config -patternOffsetType2 filterPalletteOffsetStartOfFrame
		#filterPallette config -patternOffsetType3 0
		#filterPallette config -patternOffsetType4 0
		#filterPallette config -gfpErrorCondition gfpErrorsOr
		#filterPallette config -enableGfptHecError true
		#filterPallette config -enableGfpeHecError true
		#filterPallette config -enableGfpPayloadCrcError true
		#filterPallette config -enableGfpBadFcsError true
		#filterPallette config -circuitList  ""
		filterPallette config -range1Min                          64
		filterPallette config -range1Max                          1518
		filterPallette config -range2Min                          64
		filterPallette config -range2Max                          1518
		filterPallette config -range3Min                          64
		filterPallette config -range3Max                          1518
		filterPallette config -range4Min                          64
		filterPallette config -range4Max                          1518
		#filterPallette config -range1MatchMinMaxOnly 0
		#filterPallette config -range2MatchMinMaxOnly 0
		#filterPallette config -range3MatchMinMaxOnly 0
		#filterPallette config -range4MatchMinMaxOnly 0
		if {[filterPallette set $chasId $card $port]} {
			errorMsg "Error calling filterPallette set $chasId $card $port"
			set ::retCode $::TCL_ERROR
		}

		capture setDefault 
		#capture config -fullAction lock
		capture config -sliceSize                          65536
		#capture config -sliceOffset 0
		#capture config -captureMode captureTriggerMode
		#capture config -continuousFilter 0
		#capture config -beforeTriggerFilter captureBeforeTriggerNone
		#capture config -afterTriggerFilter captureAfterTriggerFilter
		#capture config -triggerPosition 1.0
		#capture config -enableSmallPacketCapture false
		#capture config -captureDirection 0
		if {[capture set $chasId $card $port]} {
			errorMsg "Error calling capture set $chasId $card $port"
			set ::retCode $::TCL_ERROR
		}

		txRxPreamble setDefault 
		#txRxPreamble config -txMode preambleModeSFDDetect
		#txRxPreamble config -rxMode preambleSameAsTransmit
		#txRxPreamble config -enableCiscoCDL false
		#txRxPreamble config -enablePreambleView false
		#txRxPreamble config -enableCDLStats false
		#txRxPreamble config -enableIncludePreambleInRxCrc false
		if {[txRxPreamble set $chasId $card $port]} {
			errorMsg "Error calling txRxPreamble set $chasId $card $port"
			set ::retCode $::TCL_ERROR
		}

		streamRegion setDefault 
		streamRegion config -gapControlMode                     streamGapControlAverage
		if {[streamRegion set $chasId $card $port]} {
			errorMsg "Error calling streamRegion set $chasId $card $port"
			set ::retCode $::TCL_ERROR
		}


		ipAddressTable setDefault 
		#ipAddressTable config -defaultGateway  "0.0.0.0"
		if {[ipAddressTable set $chasId $card $port]} {
			errorMsg "Error calling ipAddressTable set $chasId $card $port"
			set ::retCode $::TCL_ERROR
		}


		if {[interfaceTable select $chasId $card $port]} {
			errorMsg "Error calling interfaceTable select $chasId $card $port"
			set ::retCode $::TCL_ERROR
		}

		interfaceTable setDefault 
		#interfaceTable config -dhcpV4RequestRate 0
		#interfaceTable config -dhcpV6RequestRate 0
		#interfaceTable config -dhcpV4MaximumOutstandingRequests 100
		#interfaceTable config -dhcpV6MaximumOutstandingRequests 100
		#interfaceTable config -fcoeRequestRate 500
		#interfaceTable config -fcoeNumRetries 5
		#interfaceTable config -fcoeRetryInterval 2000
		#interfaceTable config -fipVersion fipVersion1
		#interfaceTable config -enableFcfMac false
		#interfaceTable config -fcfMacCollectionTime 1000
		#interfaceTable config -enablePMacInFpma true
		#interfaceTable config -enableNameIdInVLANDiscovery false
		#interfaceTable config -enableTargetLinkLayerAddrOption false
		#interfaceTable config -enableAutoNeighborDiscovery false
		#interfaceTable config -enableAutoArp false
		if {[interfaceTable set]} {
			errorMsg "Error calling interfaceTable set"
			set ::retCode $::TCL_ERROR
		}

		interfaceTable clearAllInterfaces 
		if {[interfaceTable write]} {
			errorMsg "Error calling interfaceTable write"
			set ::retCode $::TCL_ERROR
		}


		protocolServer setDefault 
		#protocolServer config -enableArpResponse false
		#protocolServer config -enablePingResponse false
		if {[protocolServer set $chasId $card $port]} {
			errorMsg "Error calling protocolServer set $chasId $card $port"
			set ::retCode $::TCL_ERROR
		}

		oamPort setDefault 
		#oamPort config -enable false
		oamPort config -macAddress                         "00 00 AB BA DE AD"
		#oamPort config -enableLoopback false
		#oamPort config -enableLinkEvents false
		#oamPort config -maxOamPduSize 1518
		#oamPort config -oui  "00 00 00"
		#oamPort config -vendorSpecificInformation  "00 00 00 00"
		#oamPort config -idleTimer 5
		#oamPort config -enableOptionalTlv false
		#oamPort config -optionalTlvType 254
		#oamPort config -optionalTlvValue  ""
		if {[oamPort set $chasId $card $port]} {
			errorMsg "Error calling oamPort set $chasId $card $port"
			set ::retCode $::TCL_ERROR
		}
	
		ixEnablePortIntrinsicLatencyAdjustment $chasId $card $port true
		#lappend ::portList [list $chasId $card $port]
		if {[ixWritePortsToHardware portList]} {
			clearOwnershipAndLogout
			return "sam debug ===== $::TCL_ERROR"
		}
	}
}
proc set_IXIA_stream_Continous_Packet {{PacketSize 1518} {Style 0} {frame_min 64} {frame_max 1518} {PattemType 5}} {
	# streams start
	#ixPuts "Configuring streams..."
	puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] Configuring streams..."
	ixGlobalSetDefault
	# Samuel tag start
	puts "PacketSize = $PacketSize"
	set frameSize $PacketSize
	set frame_max $frame_max
	set frame_min $frame_min
	set PattemType $PattemType
	puts "Style = $Style"
	set style $Style
	set i 1
	foreach item $::portList {
		scan $item "%d %d %d" chasId card port
		stream setDefault
		stream config -percentPacketRate 100
		if {$i % 2 == 1} {
			set da [expr $i +1]
			set sa_str "00 00 01 00 0$i 00"
			set da_str "00 00 01 00 0$da 00"
			stream config -sa "$sa_str"
			stream config -da "$da_str"
			incr i 1
		} else {
			set da [expr $i -1]
			set sa_str "00 00 01 00 0$i 00"
			set da_str "00 00 01 00 0$da 00"
			stream config -sa "$sa_str"
			stream config -da "$da_str"
			incr i 1
		}
		stream config -framesize $frameSize
		stream config -frameSizeType $style
		stream config -frameSizeMIN $frame_min
		stream config -frameSizeMAX $frame_max
		stream config -patternType $PattemType
		stream config -dataPattern 3
		stream config -pattern {55 55}
		stream config -asyncIntEnable 1
		stream config -dma 0
		stream config -numFrames 100
		
		###samuel add protocol type
		protocol setDefault 
		### ethernetType 0=None, 1=EthernetII
		protocol config -ethernetType 1
		
		if [stream set $chasId $card $port 1] {
			errorMsg "Error setting stream $chasId,$card,$port. -
			$ixErrorInfo"
			puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] Error setting stream $chasId,$card,$port. - $ixErrorInfo"
			set ::retCode $::TCL_ERROR
			break
		}
	}
	# Samuel tag end

	# Dump out now if there were any errors.. maybe you want to throw instead of a return.
	if {$::retCode != $::TCL_OK} {
		clearOwnershipAndLogout
		puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] $::retCode"
		return $::retCode
	}
	# Writes all the configuration on ports in hardware
	# NOTE: This does NOT take link down, so no point in checking link state
	# afterward and no need for any delays
	# Also note that this is an example of a throw instead of a return
	if [ixWriteConfigToHardware ::portList] {
		return -code error
	}
}
proc set_IXIA_stream_Stop_After_Stream {{frameSize 1518}} {
	# streams start
	puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] Configuring streams..."
	#ixPuts "Configuring streams..."
	ixGlobalSetDefault
	# Samuel tag start
	set frameSize $frameSize
	set i 1
	foreach item $::portList {
		scan $item "%d %d %d" chasId card port
		stream setDefault
		stream config -percentPacketRate 100
		
		if {$i % 2 == 1} {
			set da [expr $i +1]
			set sa_str "00 00 01 00 0$i 00"
			set da_str "00 00 01 00 0$da 00"
			stream config -sa "$sa_str"
			stream config -da "$da_str"
			incr i 1
		} else {
			set da [expr $i -1]
			set sa_str "00 00 01 00 0$i 00"
			set da_str "00 00 01 00 0$da 00"
			stream config -sa "$sa_str"
			stream config -da "$da_str"
			incr i 1
		}
		
		stream config -framesize $frameSize
		stream config -frameSizeMIN $frameSize
		stream config -frameSizeMAX $frameSize
		stream config -patternType 5
		stream config -dataPattern 3
		stream config -pattern {55 55}
		stream config -asyncIntEnable 1
		stream config -dma 2
		stream config -numFrames 1000000
		
		###samuel add protocol type
		protocol setDefault 
		### ethernetType 0=None, 1=EthernetII
		protocol config -ethernetType 1
		
		if [stream set $chasId $card $port 1] {
			puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] Error setting stream $chasId,$card,$port. - $ixErrorInfo"
			errorMsg "Error setting stream $chasId,$card,$port. -$ixErrorInfo"
			set ::retCode $::TCL_ERROR
			break
		}
	}
	# Samuel tag end

	# Dump out now if there were any errors.. maybe you want to throw instead of a return.
	if {$::retCode != $::TCL_OK} {
		clearOwnershipAndLogout
		puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] $::retCode"
		return $::retCode
	}
# Writes all the configuration on ports in hardware
# NOTE: This does NOT take link down, so no point in checking link state
# afterward and no need for any delays
# Also note that this is an example of a throw instead of a return
	if [ixWriteConfigToHardware ::portList] {
		return -code error
	}
}
proc Start_Traffic_And_Capture {{RunTime 300000}} {

	foreach item $::portList {
		scan $item "%d %d %d" chasId card port
		puts "$chasId $card $port"
		#set a [stat getLinkState $chasId $card $port]
		#puts $a
		set i 0
		while {[stat getLinkState $chasId $card $port] == "0" && $i<30 } {
			puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] link state is 0\n"
			ixPuts "\nport $port link state is 0.\n"
			after 1000
			incr i 1
		}
		puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] link state is 1\n"
		ixPuts "\nport $port link state is 1.\n"
	}
	set ::link_end [clock seconds]
	puts "link_end = $::link_end"
	set ::duration [expr $::link_end - $::link_start -6]
	puts "link_end - link_start = $::duration"
	



	puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] Start_Traffic_And_Capture = $::portList"
	ixPuts "Start_Traffic_And_Capture = $::portList"
	# Zero all statistic counters on ports
	if [ixClearStats ::portList] {
		return -code error
	}

	after 5000
	
	
	puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] Start capture..."
	ixPuts "Start capture..."
	if [ixStartCapture ::portList] {
		return -code error
	}
	# exec python C:\\Python39\\Scripts\\AutoMation_1\\ras_pi.py link_drop_init
	puts "samuel debug is over"
	
	ixPuts "Start transmit..."
	if [ixStartTransmit ::portList] {
		return -code error
	}
	# Let it transmit for a bit; if this were a real test, we might want to wait for
	# approx. the total transmit time. Since it's not, 1 sec is sufficient for the
	# streams we've created.
	puts "runtime = $RunTime"
	exec tclsh  C:\\Python39\\Scripts\\AutoMation_1\\sam.tcl $::portList $RunTime $::Number &
	after $RunTime

	if [ixStopTransmit ::portList] {
		return -code error
	}
	
	after 5000

	# Checks whether transmission is done on a group of ports
	if {[ixCheckTransmitDone ::portList]} {
		clearOwnershipAndLogout
		return -code error
	} else {
		puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] Transmission is complete."
		ixPuts "Transmission is complete."
	}
	# Stop capture on ports - not really necessary, as any read of capture will
	# automatically stop captureixPuts "Stop capture..."
	if [ixStopCapture ::portList] {
		clearOwnershipAndLogout
		return -code error
	}
	# This api will request stats from all ports in the portList - it's really
	# efficient and the best way to collect stats when you have multiple ports to
	# contend with.
	ixRequestStats ::portList
	
	foreach item $::portList {
		scan $item "%d %d %d" chasId card port
		if {[statList get $chasId $card $port]} {
			puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] Error getting stats for $chasId,$card,$port"
			ixPuts "Error getting stats for $chasId,$card,$port"
			set ::retCode $TCL_ERROR
			break
		}
		# note that if a stat is not supported on a particular port type, the cget
		# will throw so it is best to protect that in the following fashion:
		if [catch {statList cget -scheduledFramesSent} numTxFrames ] {
			set numTxFrames 0
			puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] WARNING: -scheduledFramesSent not supported on $chasId,$card,$port. Value set to 0"
			ixPuts "WARNING: -scheduledFramesSent not supported on
			$chasId,$card,$port. Value set to 0"
		}
		if [catch {statList cget -framesReceived} numRxFrames ] {
			set numTxFrames 0
			puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] WARNING: -scheduledFramesSent not supported on $chasId,$card,$port. Value set to 0"
			ixPuts "WARNING: -scheduledFramesSent not supported on
			$chasId,$card,$port. Value set to 0"
		}
		# if [catch {statList cget -userDefinedStat2} numRxFrames ] {
			# set numRxFrames 0
			# ixPuts "WARNING: -userDefinedStat2 not supported on $chasId,$card,$port.
			# Value set to 0"
		# }
		 # if [captureBuffer get $chasId $card $port 1 $numRxFrames] {
		 # ixPuts "Error getting captureBuffer on $chasId $card $numRxFrames"
         # set ::retCode $::TCL_ERROR
		 # }
		puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] Port: $chasId,$card,$port"
		ixPuts "Port: $chasId,$card,$port"
		puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] Speed: [stat getLineSpeed $chasId $card $port]\t"
		ixPuts -nonewline "Speed: [stat getLineSpeed $chasId $card $port]\t"
		puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] Frames Sent: $numTxFrames\t"
		ixPuts -nonewline "Frames Sent: $numTxFrames\t"
		puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] Frames Rcvd: $numRxFrames"
		ixPuts -nonewline "Frames Rcvd: $numRxFrames\n"
		lappend ::resultQQ [list $port $numTxFrames $numRxFrames]
		#ixPuts "Number of packets captured :[captureBuffer cget -numFrames]\n"
	}
	puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] Sample test complete.\n"
	ixPuts "\nSample test complete.\n"
	clearOwnershipAndLogout
}
proc learning_process {{RunTime 2000}} {
	
	if [ixClearStats ::portList] {
		return -code error
	}
	###
	puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] start listen process"
	ixPuts "Start listen process Transmit..."
	if [ixStartTransmit ::portList] {
		return -code error
	}
	# Let it transmit for a bit; if this were a real test, we might want to wait for
	# approx. the total transmit time. Since it's not, 1 sec is sufficient for the
	# streams we've created.
	puts "runtime = $RunTime"
	after $RunTime
	puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] stop listen process"
	ixPuts "Stop listen process Transmit..."
	if [ixStopTransmit ::portList] {
		return -code error
	}
	
	# Checks whether transmission is done on a group of ports
	if {[ixCheckTransmitDone ::portList]} {
		clearOwnershipAndLogout
		return -code error
	} else {
		puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] Transmission is complete."
		ixPuts "Transmission is complete."
	}
	ixPuts "Clear Stats..."
	if [ixClearStats ::portList] {
		return -code error
	}

}
proc Report_Nomal {} {
		### append $::summary_result 
		### TX, RX part
		set i 0		
		while {$i< [string length $::IXIA_Ports] } {
				set PI_TX [lindex [lindex $::resultQQ $i] 1]
				set PI_RX [lindex [lindex $::resultQQ $i] 2]
				append ::summary_result ",$PI_TX,$PI_RX"
				incr i 1
		}
		
		### LOOPBACK part
		set i 0
		while {$i< [string length $::IXIA_Ports] } {
				append ::summary_result ","
				incr i 1
		}
		
		### nomal part
		set i 0
		while {$i< [string length $::IXIA_Ports] } {
				set j [expr $i +1]
				set PI_TX [lindex [lindex $::resultQQ $i] 1]
				set PI_RX [lindex [lindex $::resultQQ $i] 2]
				set PJ_TX [lindex [lindex $::resultQQ $j] 1]
				set PJ_RX [lindex [lindex $::resultQQ $j] 2]
				set PI_PJ [expr $PI_TX - $PJ_RX]
				set PJ_PI [expr $PJ_TX - $PI_RX]
				append ::summary_result ",$PI_PJ,$PJ_PI"
				
				if { $PI_PJ == 0} {
					puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] times: $::Number port $i to port $j no losing"
					ixPuts "times: $::Number port $i to port $j no losing"
				} else {	
					puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] times: $::Number port $i to port $j has $PI_PJ losing"
					ixPuts "times: $::Number port $i to port $j has $PI_PJ losing"
				}
				if { $PJ_PI == 0} {
					puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] times: $::Number port $j to port $i no losing "
					ixPuts "times: $::Number port $j to port $i no losing "
				} else {	
					puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] times: $::Number port $j to port $i has $PJ_PI losing"
					ixPuts "times: $::Number port $j to port $i has $PJ_PI losing"
				}
				if { $PI_PJ >= 500 || $PJ_PI >= 500 } {
					set debug_flag [open "flag.txt" w+]
					puts $debug_flag "1"
					close $debug_flag
				} elseif {$PI_PJ < 0 || $PJ_PI < 0} {
					set debug_flag [open "flag.txt" w+]
					puts $debug_flag "1"
					close $debug_flag
				} else {
					set debug_flag [open "flag.txt" w+]
					puts $debug_flag "0"
					close $debug_flag
				}
				incr i 2
		}
		
		### PER part
		set i 0
		while {$i< [string length $::IXIA_Ports] } {
				set j [expr $i +1]
				set PI_TX [lindex [lindex $::resultQQ $i] 1]
				set PI_RX [lindex [lindex $::resultQQ $i] 2]
				set PJ_TX [lindex [lindex $::resultQQ $j] 1]
				set PJ_RX [lindex [lindex $::resultQQ $j] 2]
				set PI_PJ [expr [expr $PI_TX - $PJ_RX]*1.0]
				set PJ_PI [expr [expr $PJ_TX - $PI_RX]*1.0]				
				set PI_PER [expr {$PI_PJ / $PI_TX}]
				set PJ_PER [expr {$PJ_PI / $PJ_TX}]
				append ::summary_result ",$PI_PER,$PJ_PER"
				incr i 2
		}
	
	
	
}
proc Report_LOOPBACK {} {
		### append $::summary_result 
		### TX, RX part
		set i 0		
		while {$i< [string length $::IXIA_Ports] } {
				set PI_TX [lindex [lindex $::resultQQ $i] 1]
				set PI_RX [lindex [lindex $::resultQQ $i] 2]
				append ::summary_result ",$PI_TX,$PI_RX"
				incr i 1
		}
		
		### LOOPBACK part
		set i 0
		while {$i< [string length $::IXIA_Ports] } {
				set PI_TX [lindex [lindex $::resultQQ $i] 1]
				set PI_RX [lindex [lindex $::resultQQ $i] 2]
				set PI_LOOPBACK [expr $PI_RX - $PI_TX]
				append ::summary_result ",$PI_LOOPBACK"
				
				if { $PI_LOOPBACK == 0} {
					puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] times: $::Number port $i LOOPBACK no losing"
					ixPuts "times: $::Number port $i LOOPBACK no losing"
				} else {	
					puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] times: $::Number port $i LOOPBACK has $PI_LOOPBACK losing"
					ixPuts "times: $::Number port $i LOOPBACK has $PI_LOOPBACK losing"
				}
				if { $PI_LOOPBACK >= 500} {
					set debug_flag [open "flag.txt" w+]
					puts $debug_flag "1"
					close $debug_flag
				} else {
					set debug_flag [open "flag.txt" w+]
					puts $debug_flag "0"
					close $debug_flag
				}		
				
				incr i 1
		}
		
		### nomal part
		set i 0
		while {$i< [string length $::IXIA_Ports] } {
				append ::summary_result ",,"
				incr i 2
		}
		
		### PER part
		set i 0
		while {$i< [string length $::IXIA_Ports] } {
				set PI_TX [lindex [lindex $::resultQQ $i] 1]
				set PI_RX [lindex [lindex $::resultQQ $i] 2]
				set PI_LOOPPACK [expr [expr $PI_TX - $PI_RX]*1.0]
				set PI_LOOPPACK_PER [expr {$PI_LOOPPACK / $PI_TX}]
				append ::summary_result ",$PI_LOOPPACK_PER"
				incr i 1
		}
	
	
	
}
proc summary {{PacketSize 64} {RunTime 30}} {
	set PacketSize $PacketSize
	set RunTime $RunTime
	set a "Masterslave,Length,Portspeed,Number,LinkUp_duration,PacketSize,RunTime,Temp"
	if {[file exists $::Function_Name\_Summary.csv]==0} {
		set fp1 [open "$::Function_Name\_Summary.csv" w+]
		set i 0
		### TX, RX part
		while {$i< [string length $::IXIA_Ports]} {
				#puts "sam debug TXRX"
				append a ",P$i\_TX,P$i\_RX"
				incr i 1
		}
		
		### LOOPBACK part
		set i 0
		while {$i< [string length $::IXIA_Ports]} {
				#puts "sam debug LOOPBACK"
				append a ",P$i\LOOPBACK"
				incr i 1
		}
		### nomal part
		set i 0
		while {$i< [string length $::IXIA_Ports]} {
				#puts "sam debug Nomal"
				set j [expr $i +1]
				append a ",P$i->P$j,P$j->P$i"
				incr i 2
		}
		### PER part
		set i 0
		while {$i< [string length $::IXIA_Ports]} {
				#puts "sam debug PER"
				append a ",P$i\_PER"
				incr i 1
		}
		puts $fp1 $a
		close $fp1
	} 
	
	if {[file exists $::Function_Name\_Summary.csv]==1} {
		set cable_length ""
		switch $::CableRelay_Port {
			1 {
				set cable_length "100M"
			}
			2 {
				set cable_length "80M"
			}
			3 {
				set cable_length "60M"
			}
			4 {
				set cable_length "50M"
			}
			5 {
				set cable_length "30M"
			}
			6 {
				set cable_length "20M"
			}
			7 {
				set cable_length "10M"
			}
			8 {
				set cable_length "1M"
			}
		}
		set fp1 [open "$::Function_Name\_Summary.csv" a+]
		puts $fp1 "$::MasterSlave,$cable_length,$::PortSpeed,$::Number,$::duration,$PacketSize,$RunTime,$::TestTemp$::summary_result"
		close $fp1
		
	}
	
}
proc getLinkState {} {	
	foreach item $::portList {
		scan $item "%d %d %d" chasId card port
		puts "$chasId $card $port"
		#set a [stat getLinkState $chasId $card $port]
		#puts $a
		set i 0
		while {[stat getLinkState $chasId $card $port] == "0" && $i<30} {
			puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] link state is 0\n"
			ixPuts "\nlink state is 0.\n"
			after 1000
			incr i 1
		}
		while {[stat getLineSpeed $chasId $card $port] != $::speed_Check && $i<30} {### Samqq
			set a [stat getLineSpeed $chasId $card $port]
			puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] port speed is $::speed_Check \n"
			ixPuts "\nlink port speed is $a.\n"
			after 1000
			incr i 1
		}
		puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] link state is 1 \n"
		ixPuts "\nlink state is 1.\n"
		set a [stat getLineSpeed $chasId $card $port]
		puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] port speed is $a \n"
		ixPuts "\nport speed is $a.\n"
	}
}
proc Restart_Auto_Negotiation {} {	
	foreach item $::portList {
		scan $item "%d %d %d" chasId card port
		puts "$chasId $card $port"
		#set a [stat getLinkState $chasId $card $port]
		#puts $a
		if {[port restartAutoNegotiation $chasId $card $port]} {
			puts $::fp "${::log}::notice [clock format [clock seconds] -format {%Y%m%d_%H%M%S}] link state is 1 \n"
			ixPuts "\RestartAutoNegotiation over.\n"
		}
		after 2000 
	}
}


# MadeProcess
if {$::Function_Name == "cableplug"} {
	set ::fp [open "$::Function_Name.txt" a+]
	set ::log [logger::init CablePlug]
	init
	set_IXIA_Hardware
	set ::link_start [clock seconds]
	puts "link_start = $::link_start"
	set_IXIA_stream_Continous_Packet $::Packet_Size 0 64 1518 $::DataPattem_Mode
	#set_IXIA_stream_Stop_After_Stream 1518
	getLinkState
	learning_process
	after 2000
	getLinkState
	Start_Traffic_And_Capture $::DurationMS	
	Report_Nomal
	# #exec python C:\\Python39\\Scripts\\AutoMation_1\\ras_pi.py link_drop_read
	# #exec pscp -pw 12345678 root@192.168.88.81:/root/link_drop.txt link_drop.txt
	# #exec pscp -pw 12345678 root@192.168.88.81:/root/SNR.txt SNR.txt
	summary $::Packet_Size $::DurationMS
	close $::fp 
}
if {$::Function_Name == "powercycle"} {
	set ::fp [open "$::Function_Name.txt" a+]
	set ::log [logger::init PowerCycle]
	init
	set_IXIA_Hardware
	set ::link_start [clock seconds]
	puts "link_start = $::link_start"
	set_IXIA_stream_Continous_Packet $::Packet_Size 0 64 1518 $::DataPattem_Mode
	#set_IXIA_stream_Stop_After_Stream 1518
	getLinkState
	learning_process
	after 2000
	getLinkState
	Start_Traffic_And_Capture $::DurationMS
	Report_Nomal
	summary $::Packet_Size $::DurationMS
	close $::fp 
}
if {$::Function_Name == "forwarding"} {
	set ::fp [open "$::Function_Name.txt" a+]
	set ::log [logger::init Forwarding]
	init
	set_IXIA_Hardware
	set ::link_start [clock seconds]
	puts "link_start = $::link_start"
	# ### packet =64 runtime=5 mins
	if {$::Packet_Size == "random"} {
		set_IXIA_stream_Continous_Packet 64 1 64 1518 $::DataPattem_Mode 
	} else {
		set_IXIA_stream_Continous_Packet $::Packet_Size 0 64 1518 $::DataPattem_Mode 
	}
	getLinkState
	learning_process
	after 2000
	getLinkState
	Start_Traffic_And_Capture $::DurationMS
	#Report_LOOPBACK
	Report_Nomal
	# #exec python C:\\Python39\\Scripts\\AutoMation_1\\ras_pi.py link_drop_read
	# #exec pscp -pw 12345678 root@192.168.88.81:/root/link_drop.txt link_drop.txt
	# #exec pscp -pw 12345678 root@192.168.88.81:/root/SNR.txt SNR.txt
	summary $::Packet_Size $::DurationMS
	close $::fp 
}

if {$::Function_Name == "reset" && $::Packet_Size=="1518"} {
	set ::fp [open "$::Function_Name.txt" a+]
	set ::log [logger::init Reset]
	init
	set_IXIA_Hardware
	set ::link_start [clock seconds]
	puts "link_start = $::link_start"
	set_IXIA_stream_Continous_Packet 1518
	#set_IXIA_stream_Stop_After_Stream 1518
	getLinkState
	learning_process
	after 2000
	getLinkState
	Start_Traffic_And_Capture $::DurationMS
	#Report_LOOPBACK
	Report_Nomal
	summary 1518 $::DurationMS
	close $::fp 
}
if {$::Function_Name == "forwarding" && $::Packet_Size == "reang"} {
	set ::fp [open "$::Function_Name.txt" a+]
	set ::log [logger::init Forwarding]
	init
	#set_IXIA_Hardware
	Restart_Auto_Negotiation
	set ::link_start [clock seconds]
	puts "link_start = $::link_start"
	# ### packet =1518 runtime=5 mins
	set_IXIA_stream_Continous_Packet 64
	getLinkState
	learning_process
	Start_Traffic_And_Capture $::DurationMS
	#Report_LOOPBACK
	Report_Nomal
	summary 64 $::DurationMS
	close $::fp 
}