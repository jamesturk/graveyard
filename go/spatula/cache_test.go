package spatula

import "testing"

type urltestpair struct {
	in  string
	out string
}

func TestCleanKey(t *testing.T) {
	var tests = []urltestpair{
		// a short URL
		{"http://shorturl",
			"shorturl,06df7035bac677b7713115fc2386aaa65b7533d5"},
		// a long URL
		{"http://anincrediblylongurlthathassomuchgoingoninitwhatarewegiongtodothisisinsane.butreallyitjustkeepsgoingandgoingandgoingandgoingandgoingandgoingandgoingandgoingandgoingandgoingandgoingbasicallyforeverandever",
			"anincrediblylongurlthathassomuchgoingoninitwhatarewegiongtodothisisinsane.butreallyitjustkeepsgoingandgoingandgoingandgoingandgoingandgoingandgoingandgoingandgoingandgoingandgoingbasicallyforeverandev,2293ec83402320ad119b59479b7f295e6aaffeaf"},
		// another similar long url, only hash should change
		{"http://anincrediblylongurlthathassomuchgoingoninitwhatarewegiongtodothisisinsane.butreallyitjustkeepsgoingandgoingandgoingandgoingandgoingandgoingandgoingandgoingandgoingandgoingandgoingbasicallyforeverandever/2",
			"anincrediblylongurlthathassomuchgoingoninitwhatarewegiongtodothisisinsane.butreallyitjustkeepsgoingandgoingandgoingandgoingandgoingandgoingandgoingandgoingandgoingandgoingandgoingbasicallyforeverandev,866af57f4d9d55045eb957209b06cd1a1dcfe052"},
	}
	for _, pair := range tests {
		out := cleanKey(pair.in)
		if out != pair.out {
			t.Error("For", pair.in, "expected", pair.out, "got", out)
		}
	}
}

func TestFileCacheBasics(t *testing.T) {
	fc := &FileCache{}
	fc.Set("cnn", "this is CNN")
	got, err := fc.Get("cnn")
	if err != nil {
		t.Error("Error: ", err)
	}
	if got != "this is CNN" {
		t.Error("Instead of getting back set content, got", got)
	}
}
