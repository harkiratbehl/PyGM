package main

func main() {
	i := 0
	a := [3]int{1, 2, 3}
	if i <= 3 {
		a[i]++
	}
	if i >= 2 {
		a[i]--
	} else {
		a[i] = 1
	}
}
