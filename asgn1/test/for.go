package main

import "fmt"

func main() {
	i := 6
	for ; i <= 8 && i >= 6 && i != 7; i++ {
		if i >= 0 {
			fmt.Printf("yes\n")
		} else {
			fmt.Printf("no\n")
		}
	}
}
