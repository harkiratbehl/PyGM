package main

func main() {
	var wflg, tflg int = 0, 0
	var dflg int = 0
	var c string
	switch c {
	case "w":
	case "W":
		wflg = 1
		break
	case "t":
	case "T":
		tflg = 1
		break
	case "d":
		dflg = 1
		break
	}
}
