
package main

import (
	"fmt"
	"time"
)

func main() {
	start := time.Now()
	t := time.Now()
	elapsed := t.Sub(start)
	i := 1
	for i <= 10 {
		fmt.Println(i)
		i++
	}
}
