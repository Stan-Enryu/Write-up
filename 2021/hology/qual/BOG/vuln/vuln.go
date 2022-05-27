package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"log"
	"math/rand"
	"os"
	"reflect"
	"time"
	"unsafe"
)

type SliceHeader struct {
	Data uintptr
	Len  int
	Cap  int
}

func pole() {
	body, err := ioutil.ReadFile("flag.txt")
	if err != nil {
		log.Fatalf("unable to read file: %v, try run in server", err)
	}
	fmt.Println(string(body))
}

func genrand(a int, b int) int {
	rand.Seed(time.Now().UnixNano())
	var x int = rand.Intn(a-b) + b
	return x
}

func printran(c int, d int) int {
	return (c*5 ^ d)
}

func hint(x int, z int) {
	fmt.Println(printran(x, z))
	fmt.Println(z)
}

func mapz() {
	z := reflect.ValueOf(pole).Pointer()
	fmt.Printf("%x\n", z)
}

var reader = bufio.NewReader(os.Stdin)
var ab int
var xr int

func gen() {
	ab = genrand(323, 0)
	xr = genrand(1024, 0)
}

func main() {
	var inp int
	for {
		fmt.Scan(&inp)

		if inp == 1 {
			gen()
			hint(ab, xr)
		} else {
			break
		}
	}
	mapz()
	data := make([]byte, 256)
	Slice := make([]byte, ab)
	sliceHeader := (*reflect.SliceHeader)(unsafe.Pointer(&Slice))
	DataAdd := uintptr(unsafe.Pointer(&(data[0])))
	sliceHeader.Data = DataAdd

	_, _ = reader.Read(Slice)
}
