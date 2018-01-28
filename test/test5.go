package main
import "fmt"
import "time"
func main() {
	
		i := 3
		fmt.Print("switch works, because", i, " is equal to")
		switch i {
		case 1:
			fmt.Println("one")
		case 2:
			fmt.Println("two")
		case 3:
			fmt.Println("three")
		}
}