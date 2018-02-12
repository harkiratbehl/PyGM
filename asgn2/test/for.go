package main

import "fmt"

func main() {
	i := 6
	for ; i<= 8; i++ {
			fmt.Printf(i)
	}
}

// int i=0
// LOOP:
// if (i>=9) goto END_FOR
// 	i=i+1
// 	goto LOOP
// END_FOR