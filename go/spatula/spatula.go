package spatula

import (
	"github.com/PuerkitoBio/goquery"
	"io/ioutil"
	"net/http"
	"strings"
)

type Page struct {
	Url      string
	Response *http.Response
	Body     string
	Doc      *goquery.Document
}

type Client struct {
	requests_per_minute int
}

func (client *Client) Get(url string) (*Page, error) {
	page := new(Page)
	response, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer response.Body.Close()
	body, err := ioutil.ReadAll(response.Body)
	if err != nil {
		return nil, err
	}
	page.Body = string(body)
	doc, err := goquery.NewDocumentFromReader(strings.NewReader(page.Body))
	if err != nil {
		return nil, err
	}
	page.Url = url
	page.Response = response
	page.Doc = doc

	return page, nil
}
