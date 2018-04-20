package main

func ackermann(m int, n int)

func ackermann(m int, n int) int {
    if m == 0 {
        return n + 1
    }
    if n == 0 {
        return ackermann(m-1, 1)
    }
    return ackermann(m-1, ackermann(m, n-1))
}

func main() {
    x := ackermann(3, 4)
    Println("ackermann with input 3 and 4 = ")
    Println(x)
}
