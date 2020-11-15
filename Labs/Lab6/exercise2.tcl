#Create a simulator object
>>

#Define different colors
$ns color 1 Blue
$ns color 2 Red
$ns color 3 Yellow


#Open the nam trace file
set namf [open out.nam w]
$ns namtrace-all $namf

set f1 [open tcp1.tr w]
>>

#Define a 'finish' procedure
proc finish {} {
    global ns namf f1 f2
    $ns flush-trace
	#Close the trace amd nam files
    close $namf
	close $f1
	close $f2
	#Execute nam on the trace file
    exec nam out.nam &
    # Execute gnuplot to display the two trace files tcp1.tr and tcp2.tr
    #exec gnuplot throughput.plot &
    exit 0
}

#Create eight nodes
set n0 [$ns node]
>>


#Create links between the nodes
$ns duplex-link $n0 $n1 10Mb 10ms DropTail
>>
# set the correct orientation for all nodes
$ns duplex-link-op $n0 $n1 orient right
>>

#Set Queue limit and Monitor the queue for the link between node 2 and node 4
$ns queue-limit $n2 $n4 10
$ns duplex-link-op $n2 $n4 queuePos 0.5

#Create a TCP agent and attach it to node n0
set tcp1 [new Agent/TCP]
$ns attach-agent $n0 $tcp1

#Sink for traffic at Node n5
set sink1 [new Agent/TCPSink]
$ns attach-agent $n5 $sink1

#Connect
$ns connect $tcp1 $sink1
$tcp1 set fid_ 1

#Setup FTP over TCP connection
set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp1

#Create a TCP agent and attach it to node n3
>>
#Sink for traffic at Node n5
>>
#Connect
>>
#Setup FTP over TCP connection
>>

#Create a TCP agent and attach it to node n7
>>

#Sink for traffic at Node n0
>>

#Connect
>>

#Setup FTP over TCP connection
>>


#Create a TCP agent and attach it to node n7
>>

#Sink for traffic at Node n3
>>

#Connect
>>

#Setup FTP over TCP connection
>>

proc record {} {
>>
        #Get an instance of the simulator
        set ns [Simulator instance]
        #Set the time after which the procedure should be called again
        set time 0.1
        #How many bytes have been received by the traffic sinks at n5?
        set bw1 [$sink1 set bytes_]
>>
	#Get the current time
        set now [$ns now]
        #Calculate the bandwidth (in MBit/s) and write it to the files
        puts $f1 "$now [expr $bw1/$time*8/1000000]"
        puts $f2 "$now [expr $bw2/$time*8/1000000]"
        #Reset the bytes_ values on the traffic sinks
>>
        #Re-schedule the procedure
        $ns at [expr $now+$time] "record"
}


#Schedule events for all the agents
#start recording
>>

#start FTP sessions
$ns at 0.5 "$ftp1 start"
>>

#Stop FTP sessions
>>

#Call the finish procedure after 10 seconds of simulation time
$ns at 10.0 "finish"

#Run the simulation
>>
