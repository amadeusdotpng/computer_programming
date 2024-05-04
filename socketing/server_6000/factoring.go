package main

import (
	"fmt"
	"log"
	"math/big"
	"net"
	"strings"
	"time"
)

const (
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = "4000"
    SERVER_TYPE = "tcp"
)


func main() {
    redeploy_delay := 4

    for {
        server, err := net.Listen(SERVER_TYPE, SERVER_HOST+":"+SERVER_PORT)
        const msg string = "ERROR: [error listening to "+SERVER_HOST+":"+SERVER_PORT+"]"
        if checkErr(err, msg, nil) {
            time_duration := time.Duration(redeploy_delay * int(time.Second))
            time.Sleep(time_duration)
    
            redeploy_delay *= 2
            continue
        }

        defer server.Close()

        redeploy_delay = 4

        log.Printf("Listening to Port %v...\n", SERVER_PORT)
        for {
            con, err := server.Accept()
            const msg string = "ERROR: [error accepting connection]"
            if checkErr(err, msg, con) { continue }
            
            processClient(con)
            con.Close()
        }
    }
}

// Responsible for reading/writing from/to the connection, converting the read bytes
// into big.Int for factoring, and calling the factor function itself.
// This is also responsible for seeing if the connection is still alive through a heartbeat.
func processClient(connection net.Conn) {
    buffer := make([]byte, 1024)
    mLen, err := connection.Read(buffer)
    errMsg := "ERROR: [error reading from connection]"
    if checkErr(err, errMsg, connection) { return }


    n, start_range, end_range, ok := parseInput(buffer[:mLen], connection)
    if !ok { return }

    log.Printf("STARTING: (%d, %d to %d)\n", n, start_range, end_range)

    // Heartchan; the main motivation for this is so that if the connection
    // suddenly dies, it doesn't have to keep doing work. It can then accept
    // a new connection and do that work instead. 
    // It sends a "PING" message every 4 seconds and expects a "PONG" within
    // those 4 seconds.
    // If no "PONG" message is received, it signals to the factor func that it
    // no longer needs to work.
    heartchan := make(chan bool)

    // Factorchan: this is just a signaling mechanism for the  factor func
    // to tell the heartbeat goroutine that it's done factoring so it no
    // longer has to check if the connection is alive.
    //
    // NOTE: we use the type struct{} because apparently it require no memory
    //       so it's just a little better. We're only using these channels for
    //       signaling mechanisms.
    factorchan := make(chan struct{}) 

    // Heartbeat goroutine
    go func() {
        t := time.NewTicker(10 * time.Second)
        defer t.Stop()
        defer close(heartchan)
        dummy := make([]byte, 4)
        for range t.C {
            select {
            case <-factorchan:
                return
            default:
            }

            connection.Write([]byte("PING"))
            log.Printf("HEARTBEAT_SEND: (%d, %d to %d) -> [sent a pulse to the connection]\n", n, start_range, end_range)

            connection.SetReadDeadline(time.Now().Add(10 * time.Second))
            _, err := connection.Read(dummy)
            if err != nil {
                log.Printf("HEARTBEAT_RECV: (%d, %d to %d) -> [did not receive a pulse from the connection]\n", n, start_range, end_range)
                heartchan<-false
                return
            }

            log.Printf("HEARTBEAT_RECV: (%d, %d to %d) -> [received a pulse from the connection]\n", n, start_range, end_range)
            heartchan<-true
        }
    }()

    f := factor(*n, *start_range, *end_range, heartchan)
    select{
    case factorchan<-struct{}{}:
    default:
        close(factorchan)
    }

    _, err = connection.Write([]byte(f.String()))
    errMsg = fmt.Sprintf("ERROR: (%d, %d to %d) -> [error writing to connection]", n, start_range, end_range)
    if checkErr(err, errMsg, connection) { return }

    if f != nil {
        log.Printf("FINISHED: (%d, %d -> %d)\n", n, start_range, end_range)
    } else {
        log.Printf("UNFINISH: (%d, %d -> %d)\n", n, start_range, end_range)
    }
}

func parseInput(input_bytes []byte, connection net.Conn) (*big.Int, *big.Int, *big.Int, bool) {
    input := func() []string {
        input := strings.TrimSpace(string(input_bytes))
        return strings.Split(input, " ")
    }()

    if len(input) < 3 {
        log.Println("ERROR: [not enough arguments]")
        return nil, nil, nil, false
    }

    n := new(big.Int)
    n, ok := n.SetString(input[0], 10)
    errMsg := "ERROR: [error converting n to big.Int]"
    if checkOk(ok, errMsg, connection) { return nil, nil, nil, false}

    start_range := new(big.Int)
    start_range, ok = start_range.SetString(input[1], 10)
    errMsg = "ERROR: [error converting start_range to big.Int]"
    if checkOk(ok, errMsg, connection) { return nil, nil, nil, false}

    end_range := new(big.Int)
    end_range, ok = end_range.SetString(input[2], 10)
    errMsg = "ERROR: [error converting end_range to big.Int]"
    if checkOk(ok, errMsg, connection) { return nil, nil, nil, false}

    return n, start_range, end_range, true
}

// Checks if some number between 'from' and 'to', left inclusive and right exclusive, is a factor of 'n'.
// If there is a factor, it returns that factor.
// If there isn't a factor, it returns -1
// If the connection breaks in the middle of factoring, it returns nil
func factor(n, from, to big.Int, heartbeat <-chan bool) *big.Int {
    // 0 is never a factor of any number >0. 1 is a trivial factor of any number.
    // We want non-trivial factors.
    if from.Cmp(big.NewInt(2)) == -1 { from = *big.NewInt(2) }

    m := new(big.Int)
    for f := from; f.Cmp(&to) == -1; f.Add(&f, big.NewInt(1)) {
        // If there isn't a pulse, then that means the connection has suddenly died
        // and we don't want to continue working so that we can accept a new connection.
        select {
        case pulse, ok := <- heartbeat:
            if ok {
                if !pulse { return nil }
            }
        default:
        }
        if m := m.Mod(&n, &f); m.Cmp(big.NewInt(0)) == 0 { return &f }
    }
    return big.NewInt(-1)
}

// Checks if there is an error and returns if there is or isn't an error.
// If there is an error, the message is printed out.
// If there is connection, it writes it out to the connection and closes it.
func checkErr(err error, msg string, connection net.Conn) bool {
    if err != nil {
        msg = msg+fmt.Sprintf(" (%s)", err.Error())
        log.Println(msg)
        if connection != nil {
            connection.Write([]byte(msg))
        }
        return true
    }
    return false
}

// Similar to checkErr
func checkOk(ok bool, msg string, connection net.Conn) bool {
    if !ok {
        log.Println(msg)
        if connection != nil {
            connection.Write([]byte(msg))
        }
        return true
    }
    return false
}
