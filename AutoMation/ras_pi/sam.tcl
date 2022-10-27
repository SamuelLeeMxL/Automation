source "C:\\Program Files (x86)\\Ixia\\IxOS\\9.00.1900.24\\TclScripts\\bin\\IxiaWish.tcl"

package req IxTclHal
package require logger


set ::hostname "192.168.88.88"
set username "IxiaTclUser"
set ::portList_debug [lindex $argv 0]
set Number [expr [lindex $argv 1]]
set RunNumber [expr $Number/1000]
set index [lindex $argv 2]
#puts $sam_debug $::portList_debug
#puts $sam_debug $RunNumber
ixConnectToTclServer $::hostname
ixLogin $username
ixConnectToChassis $::hostname
set i 0

set sam_debug [open "sam_debug.txt" a+]
puts $sam_debug "===== index : $index ====="
close $sam_debug

while {$i<$RunNumber} {
	set string_status ""
	set sam_debug [open "sam_debug.txt" a+]
	foreach item $::portList_debug {
		scan $item "%d %d %d" chasId card port
		set a [stat getLinkState $chasId $card $port]
		lappend string_status ",$a"
		exec python C:\\Python39\\Scripts\\AutoMation_1\\ras_pi.py SNR
	}
	puts $sam_debug "[clock format [clock seconds] -format {%Y%m%d_%H%M%S}] $string_status"
	close $sam_debug
	after 1000
	incr i 1
}

ixLogout 