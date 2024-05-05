package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"math/big"
	"net"
	"os"
	"strings"
	"sync"
	"time"
)

const (
    SERVER_PORT = "58008"
	SERVER_TYPE = "tcp"
)

var SERVERS []string
var COMPOSITES []string

type FactoringInfo struct {
	IP           string
	CompositeNum string
	StartRange   string
	EndRange     string
	RetryDelay   int // in case the goroutine fails
}

type ResponseInfo struct {
	FactorInfo     FactoringInfo
	ServerResponse string
}

func init() {
	IPFilePath := flag.String("I", "ip.txt", "Path to file for a list of IPs.")
	flag.Parse()
	args := flag.Args()

	if len(args) < 1 {
		fmt.Println("No input file. Please provide path to a list of composite numbers.")
		os.Exit(0)
	}

	COMPOSITES = func() []string {
		input_bytes, err := os.ReadFile(args[0])
		if err != nil {
			fmt.Println(err.Error())
			os.Exit(1)
		}

		input := string(input_bytes)
		return strings.Split(strings.ReplaceAll(strings.TrimSpace(input), "\r\n", "\n"), "\n")
	}()

	SERVERS = func() []string {
		input_bytes, err := os.ReadFile(*IPFilePath)
		if err != nil {
			fmt.Println(err.Error())
			os.Exit(1)
		}

		input := string(input_bytes)
		return strings.Split(strings.ReplaceAll(strings.TrimSpace(input), "\r\n", "\n"), "\n")
	}()

	// Set log stuff
	logfile, err := os.OpenFile("server.log", os.O_WRONLY|os.O_APPEND|os.O_CREATE, 0644)
	if err != nil {
		fmt.Println(err.Error())
		os.Exit(1)
	}
	log.SetOutput(logfile)
	log.SetFlags(log.LstdFlags | log.Lshortfile)
}

func allDigits(s string) bool {
	for _, c := range s {
		if !('0' <= c && c <= '9') {
			return false
		}
	}
	return true
}

func main() {
	// TODO: time taken for each factor
	for _, n := range COMPOSITES {
		if !(len(n) > 0 && allDigits(n)) {
			continue
		}
		log.Printf("FIND: %s", n)
		f := getFactors(n)

		// calculate the other factor
		if f != "0" {
			big_n, p, q := new(big.Int), new(big.Int), new(big.Int)
			big_n.SetString(n, 10)
			p.SetString(f, 10)
			q.Div(big_n, p)
			log.Printf("FOUND: %s -> %s, %d\n\n", n, f, q)
		}

	}
}

func getFactors(n string) string {
	step := big.NewInt(250_000_000)
	startRange := big.NewInt(0)
	responseChan := make(chan ResponseInfo)
	ctx, cancel := context.WithCancel(context.Background())
	wg := sync.WaitGroup{}

	/*
	   defer func() {
	       cancel()
	   }()
	*/

	// create starting worker goroutines for each server
	for _, server := range SERVERS {
		data := FactoringInfo{
			IP:           server,
			CompositeNum: n,
			StartRange:   startRange.String(),
			EndRange:     big.NewInt(0).Add(startRange, step).String(),
			RetryDelay:   4,
		}
		wg.Add(1)
		go testRange(data, responseChan, &wg, ctx)
		startRange.Add(startRange, step)
	}

	serverResponse := ""
	for {
		response := <-responseChan
		data := response.FactorInfo
		if response.ServerResponse == "-1" { // did not find factor
			data.StartRange = startRange.String()
			data.EndRange = big.NewInt(0).Add(startRange, step).String()
			data.RetryDelay = 4
			startRange.Add(startRange, step)
			wg.Add(1)
			go testRange(data, responseChan, &wg, ctx)
		} else if allDigits(response.ServerResponse) && len(response.ServerResponse) > 0 { // found factor
			serverResponse = response.ServerResponse
			break
		} else { // got back an error for some reason or haven't gotten a response
			go func() {
				time.Sleep(time.Duration(data.RetryDelay * int(time.Second)))
				wg.Add(1)
				testRange(data, responseChan, &wg, ctx)
			}()
		}
	}

	log.Println("WAIT: [a factor has been found. waiting for other threads to stop]")
	cancel()
	wg.Wait()
	return serverResponse
}

func testRange(data FactoringInfo, responseChan chan<- ResponseInfo, wg *sync.WaitGroup, ctx context.Context) {
	// The motivation for this is to ensure that at the end of this function
	// it will ALWAYS send something back to responseChan so that the main
	// goroutine has something to receive after every time a worker goroutine
	// ends.
	response := ""
	errMsg := ""
	factorInfo := fmt.Sprintf("(%s, %s to %s)", data.CompositeNum, data.StartRange, data.EndRange)
	defer func() {
		responseInfo := ResponseInfo{
			FactorInfo:     data,
			ServerResponse: response,
		}

		// This is so that in the event that there are no more readers for responseChan,
		// e.g. anotehr goroutine got done, so getFactors just exists, we ball and go on
		// since it doesn't matter anymore
		select {
		case responseChan <- responseInfo:
		default:
		}
		wg.Done()
	}()

	// Connect to server
	// -----------------
	connection, err := net.Dial(SERVER_TYPE, data.IP+":"+SERVER_PORT)
	errMsg = fmt.Sprintf("ERROR: %s -> [error connecting to %s on port %s]", factorInfo, data.IP, SERVER_PORT)
	if checkErr(err, errMsg) {
		return
	}

	// Send data to server
	// -------------------
	send := fmt.Sprintf("%s %s %s", data.CompositeNum, data.StartRange, data.EndRange)
	_, err = connection.Write([]byte(send))
	log.Printf("DATA_SEND: %s -> [sending data to %s on port %s]\n", factorInfo, data.IP, SERVER_PORT)
	errMsg = fmt.Sprintf("ERROR: %s -> [error writing to %s on port %s]", factorInfo, data.IP, SERVER_PORT)
	if checkErr(err, errMsg) {
		return
	}

	// Handle heartbeats/responses
	// --------------------------------
	mLen := 0
	serverResponse := make([]byte, 1024)
	heartbeatRecv := func() bool {
		connection.SetReadDeadline(time.Now().Add(35 * time.Second))
		mLen, err = connection.Read(serverResponse)
		errMsg = fmt.Sprintf("BEAT_RECV: %s -> [did not receive a pulse from %s on port %s]", factorInfo, data.IP, SERVER_PORT)
		if checkErr(err, errMsg) {
			return false
		}
		if string(serverResponse[:mLen]) == "PING" {
			log.Printf("BEAT_RECV: %s -> [received a pulse from %s on port %s]\n", factorInfo, data.IP, SERVER_PORT)
		}
		select {
		case <-ctx.Done():
			log.Printf("KILL_SIGN: %s -> [killing goroutine for %s on port %s since factor has been found]\n", factorInfo, data.IP, SERVER_PORT)
			return false
		default:
			return true
		}
	}

	// Initializer
	if !heartbeatRecv() {
		return
	}

	for string(serverResponse[:mLen]) == "PING" {
		_, err = connection.Write([]byte("PONG"))
		errMsg = fmt.Sprintf("BEAT_SEND: %s -> [could not send a pulse from %s on port %s]", factorInfo, data.IP, SERVER_PORT)
		if checkErr(err, errMsg) {
			return
		}
		log.Printf("BEAT_SEND: %s -> [sent a pulse to %s on port %s]\n", factorInfo, data.IP, SERVER_PORT)

		if !heartbeatRecv() {
			return
		}
	}

	// return non-heartbeat response through responeChan
	response = string(serverResponse[:mLen])
	log.Printf("DATA_RECV: %s -> %s\n", factorInfo, response)
	return
}

func checkOk(ok bool, msg string) bool {
	if !ok {
		log.Println(msg)
		return true
	}
	return false
}

func checkErr(err error, msg string) bool {
	if err != nil {
		msg = msg + fmt.Sprintf(" (%s)", err.Error())
		log.Println(msg)
		return true
	}
	return false
}
