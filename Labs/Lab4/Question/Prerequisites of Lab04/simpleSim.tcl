#Create a simulator object.
set ns [new Simulator]

#Open the NAM trace file
set file1 [open out.nam w]
$ns namtrace-all $file1

#Open the trace file
set file2 [open out.tr w]
$ns trace-all $file2

#Define a 'finish' procedure
proc finish {} {
	global ns file1 file2
	$ns flush-trace
	close $file1
	close $file2
	exec nam out.nam &
	exit 0
}

#Create 2 nodes
set n0 [$ns node]
set n1 [$ns node]

#Create a link between them
$ns duplex-link $n0 $n1 1Mb 10ms DropTail

#Create a UDP agent and attach it to node n0
set udp0 [new Agent/UDP]
$ns attach-agent $n0 $udp0

# Create a CBR traffic source and attach it to udp0
set cbr0 [new Application/Traffic/CBR]
$cbr0 set packetSize_ 500
$cbr0 set interval_ 0.005
$cbr0 attach-agent $udp0

#Create a Null agent (a traffic sink) and attach it to node n1
set null0 [new Agent/Null]
$ns attach-agent $n1 $null0

#Connect the traffic source with the traffic sink
$ns connect $udp0 $null0  

#Schedule events for the CBR agent
$ns at 0.5 "$cbr0 start"
$ns at 1.5 "$cbr0 stop"

#Call the finish procedure after 5 seconds of simulation time
$ns at 2.0 "finish"

#Run the simulation
$ns run
