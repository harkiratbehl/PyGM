// Function
// -param
// -return
// -call
// Jump
// -goto L
// Pointer
// -x=&y
// -x=*y
// -*x=y
// Indexed assignment
// -x = y[i] (done)
// -x[i] = y (done)
// Assignment
// -x = op y

// 1: t1 = a * a
// 2: t2 = a * b
// 3: t3 = 2 * t2
// 4: t4 = t1 + t3
// 5: t5 = b * b
// 6: t6 = t4 + t5
// 7: X = t6

// cases where there is no operator

package main

func main() {
	i := 0

	//if-else
	a := [3]int{1, 2, 3}
	if i >= 2 {
		a[i] = 2
	} else {
		a[i] = 1
	}
	z = a[i]

	//For Loop
	for i = 1; i <= 8; i++ {
		if i <= 4 {
			z = z + 1
		} else {
			z = z + 1
		}
	}

	//Functoin call
	foo()

	//

}

func foo() {
	i := 1
}
