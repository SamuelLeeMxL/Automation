### ::serial_com -> com port (argv 0)
### ::serial_baudrate -> com baudrate (argv 1)
### ::serial_times -> capture times (argv 2)

set ::serial_com [lindex $argv 0]
set ::serial_baudrate [lindex $argv 1]
set ::serial_times [expr [lindex $argv 2] * 1000]
# puts "::serial_com=$::serial_com"
# puts "::serial_baudrate=$::serial_baudrate"
# puts "::serial_times=$::serial_times"

# open com: for reading and writing
# For UNIX'es use the appropriate devices /dev/xxx
set serial [open $::serial_com\: r+]

# setup the baud rate, check it for your configuration
fconfigure $serial -mode "$::serial_baudrate,n,8,1"

# don't block on read, don't buffer output
fconfigure $serial -blocking 0 -buffering none

# Send some AT-command to your modem
puts -nonewline $serial "AT\r"

# Give your modem some time, then read the answer
after $::serial_times
puts "Modem echo: [read $serial]"
close $serial