source "C:\\Program Files (x86)\\Ixia\\IxOS\\9.20.2700.19\\TclScripts\\bin\\IxiaWish.tcl"
package req IxTclHal
set ::port [lindex $argv 0]
ixLogin IxiaTclUser
set i 0
set clock_start [clock milliseconds]
ixConnectToChassis 192.168.88.88
while {$i <60000} {	
	set a [stat getLinkState 1 2 $port]
	#puts "a= $a"
	if { $a == "0" } {
		#puts "port $port is not ready..."
		after 500
		incr i 1
	} else {
		set fp [open "duration.txt" a+]
		set clock_end [clock milliseconds]
		set tcl_precision 2
		set duration [expr [expr $clock_end - $clock_start]/1000.0]
		puts -nonewline $fp "$::port $duration "
		close $fp
		break
	}
}