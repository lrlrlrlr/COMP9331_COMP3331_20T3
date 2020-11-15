set ns [new Simulator]

#Define different colors for data flows (for NAM)
$ns color 1 Blue
$ns color 2 Red

#Open the Trace file
set file1 [open out.tr w]
$ns trace-all $file1

#Open the NAM trace file
set file2 [open out.nam w]
$ns namtrace-all $file2


#$ns rtproto DV

#Define a 'finish' procedure
proc finish {} {
        global ns file1 file2
        $ns flush-trace
        close $file1
        close $file2
        exec nam out.nam &
        exit 0
}


#Node set multiPath_ 1 

#Create six nodes
set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]

#Create links between the nodes
$ns duplex-link $n0 $n1 0.3Mb 10ms DropTail
$ns duplex-link $n1 $n2 0.6Mb 10ms DropTail
$ns duplex-link $n2 $n3 0.6Mb 10ms DropTail
$ns duplex-link $n1 $n4 0.3Mb 10ms DropTail
$ns duplex-link $n3 $n5 1.0Mb 10ms DropTail
$ns duplex-link $n4 $n5 0.5Mb 10ms DropTail

#Give node position (for NAM)
$ns duplex-link-op $n0 $n1 orient right
$ns duplex-link-op $n1 $n2 orient right
$ns duplex-link-op $n2 $n3 orient up
$ns duplex-link-op $n1 $n4 orient up-left
$ns duplex-link-op $n3 $n5 orient left-up
$ns duplex-link-op $n4 $n5 orient right-up

#Create a UDP agent and attach it to node n0
set udp0 [new Agent/UDP]
$ns attach-agent $n0 $udp0

#Create a UDP agent and attach it to node n2
set udp1 [new Agent/UDP]
$ns attach-agent $n2 $udp1


# Create a CBR traffic source and attach it to udp0
set cbr0 [new Application/Traffic/CBR]
$cbr0 set packetSize_ 500
$cbr0 set interval_ 0.05
$cbr0 attach-agent $udp0

# Create a CBR traffic source and attach it to udp1
set cbr1 [new Application/Traffic/CBR]
$cbr1 set packetSize_ 500
$cbr1 set interval_ 0.05
$cbr1 attach-agent $udp1

#Create a Null agent (a traffic sink) and attach it to node n5
set null0 [new Agent/Null]
$ns attach-agent $n5 $null0

#Connect the traffic source with the traffic sink
$ns connect $udp0 $null0 
$ns connect $udp1 $null0 

#$ns rtmodel-at 1.0 down $n1 $n4
#$ns rtmodel-at 1.2 up $n1 $n4

#$ns cost $n1 $n4 3

#$ns cost $n1 $n4 2
#$ns cost $n3 $n5 3

#Schedule events for the CBR agent
$ns at 0.5 "$cbr0 start"
$ns at 0.6 "$cbr1 start"

$ns at 1.5 "$cbr0 stop"
$ns at 1.6 "$cbr1 stop"


$ns at 2.0 "finish"

$ns run
