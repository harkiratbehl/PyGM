package main

import (
	"fmt"
	"os"
	"bufio"
)

func main(){
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("Enter any input: ")
	input, _ := reader.ReadString('\n')
	fmt.Print(input)
}