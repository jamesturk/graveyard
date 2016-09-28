package main

import "golang.org/x/oauth2"
import "github.com/google/go-github/github"
import "gopkg.in/gorp.v1"

type tokenSource struct {
	token *oauth2.Token
}

func (t *tokenSource) Token() (*oauth2.Token, error) {
	return t.token, nil
}

func getGithubClient(db *gorp.DbMap) *github.Client {
	token := getConfig(db).GithubToken
	if token != "" {
		ts := &tokenSource{
			&oauth2.Token{AccessToken: token},
		}
		tc := oauth2.NewClient(oauth2.NoContext, ts)
		return github.NewClient(tc)
	} else {
		return github.NewClient(nil)
	}
}

func updateGithubStatus(gh *github.Client, db *gorp.DbMap) {
	var repos []Repository
	db.Select(&repos, "select * from repositories where LastSync < (date('now', '-1 day'))")

	for _, repo := range repos {
		remote, _, err := gh.Repositories.Get(repo.Owner, repo.Name)
		checkErr(err, "could not get repo from GitHub")

		updateRepoMetadata(&repo, remote)
		_, err = db.Update(&repo)
		checkErr(err, "could not update")
	}
}
