package spatula

import (
	"bufio"
	"crypto/sha1"
	"encoding/hex"
	"io"
	"net/http"
	"os"
	"path"
	"regexp"
	"strconv"
	"strings"
)

type Cache interface {
	Get(url string) (string, error)
}

type FileCache struct {
	directory string
}

var (
	PREFIX  = regexp.MustCompile("^\\w+://")
	ILLEGAL = regexp.MustCompile("[?/:|]+")
	HEADER  = regexp.MustCompile("([-\\w]+): (.*)")
)

func cleanKey(key string) string {
	hashbytes := sha1.Sum([]byte(key))
	hash := hex.EncodeToString(hashbytes[:])
	key = PREFIX.ReplaceAllString(key, "")
	key = ILLEGAL.ReplaceAllString(key, ",")
	url_len := 200
	if len(key) < url_len {
		url_len = len(key)
	}
	return key[:url_len] + "," + hash
}

func (client *FileCache) Get(url string) (*http.Response, error) {
	filepath := path.Join(client.directory, cleanKey(url))
	headers := make(map[string]string)

	f, err := os.Open(filepath)
	if err != nil {
		return "", err
	}
	defer f.Close()

	reader := bufio.NewReader(f)
	for {
		line, err := reader.ReadString('\n')
		if err != nil && err != io.EOF {
			return "", err
		}
		match := HEADER.FindAllStringSubmatch(line, -1)
		if len(match) == 1 {
			headers[match[0][1]] = match[0][2]
		} else {
			break
		}
	}
	content, err := reader.ReadString(byte(0))
	if err != nil && err != io.EOF {
		return "", err
	}

	return content, nil
}

func (client *FileCache) Set(url string, page *Page) error {
	filepath := path.Join(client.directory, cleanKey(url))

	f, err := os.Create(filepath)
	if err != nil {
		return err
	}
	defer f.Close()

	writer := bufio.NewWriter(f)
	// maybe only cache if response is 200?
	_, err = writer.WriteString("status: " + response.Status + "\n")
	_, err = writer.WriteString("statuscode: " + strconv.Itoa(response.StatusCode) + "\n")
	for k, v := range response.Header {
		_, err = writer.WriteString(k + ": " + strings.Join(v, ",") + "\n")
	}
	_, err = writer.WriteString("\n")
	_, err = writer.WriteString(body)
	if err != nil {
		return err
	}
	writer.Flush()

	return nil
}
