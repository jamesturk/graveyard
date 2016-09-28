package main

import (
	"fmt"
	"github.com/codegangsta/cli"
	"github.com/google/go-github/github"
	"gopkg.in/gorp.v1"
	"log"
	"os"
	"strconv"
	"strings"
	"time"
)

// update local information using GitHub Repository response
func updateRepoMetadata(repo *Repository, remote *github.Repository) {
	repo.HasIssues = *remote.HasIssues
	repo.HasWiki = *remote.HasWiki
	repo.OpenIssuesCount = *remote.OpenIssuesCount
	repo.ForksCount = *remote.ForksCount
	repo.WatchersCount = *remote.WatchersCount
	repo.UpdatedAt = (*remote.UpdatedAt).Format("2006-01-02")
	repo.LastSync = time.Now()
}

func processConfig(db *gorp.DbMap, args []string) {
	for _, arg := range args {
		pieces := strings.Split(arg, "=")
		if len(pieces) == 2 {
			c := getConfig(db)
			switch strings.ToLower(pieces[0]) {
			case "githubtoken":
				c.GithubToken = pieces[1]
				saveConfig(db, c)
			default:
				log.Fatalln("no such config var", pieces[0])
			}
		} else {
			log.Fatalln("invalid config argument")
		}
	}
}

// start tracking a repository or user's repositories
func track(gh *github.Client, db *gorp.DbMap, owner string, name string) {
	count := 0

	if name != "" {
		r := &Repository{Owner: owner, Name: name}
		saveRepository(db, r)
		count = 1
	} else {
		opt := &github.RepositoryListOptions{
			Type:        "public",
			ListOptions: github.ListOptions{PerPage: 100, Page: 1},
		}

		// loop until we're out of repos
		for {
			repos, _, err := gh.Repositories.List(owner, opt)
			if err != nil {
				checkErr(err, "couldn't get repository list")
			}
			if len(repos) == 0 {
				break
			}
			for _, repo := range repos {
				if !(*repo.Fork) {
					r := &Repository{Owner: owner, Name: *repo.Name}
					updateRepoMetadata(r, &repo)
					saveRepository(db, r)
					count++
				}
			}

			// next page
			opt.ListOptions.Page++
		}
	}
	fmt.Printf("tracked %d new repos\n", count)
}

func status(db *gorp.DbMap) {
	var repos []Repository
	_, err := db.Select(&repos, "select * from repositories order by name")
	checkErr(err, "could not list repositories")

	for _, repo := range repos {
		var issues string
		if repo.HasIssues {
			issues = strconv.Itoa(int(repo.OpenIssuesCount))
		} else {
			issues = " "
		}

		fmt.Printf("%-20s %-3s %-3d %-3d %s\n",
			repo.Name,
			issues,
			repo.ForksCount,
			repo.WatchersCount,
			repo.UpdatedAt,
		)
	}
}

func main() {

	app := cli.NewApp()
	app.Name = "kqu"
	app.Version = "0.0.1"
	app.Usage = "manage everything"

	db := initDB()
	gh := getGithubClient(db)

	app.Commands = []cli.Command{
		{
			Name:  "config",
			Usage: "set config options",
			Action: func(c *cli.Context) {
				processConfig(db, c.Args())
			},
		},
		{
			Name:  "track",
			Usage: "start tracking a repository",
			Action: func(c *cli.Context) {
				if len(c.Args()) == 0 {
					fmt.Println("checkwikis requires a username/org parameter")
					return
				}
				track(gh, db, c.Args()[0], c.Args().Get(1))
			},
		},
		{
			Name:  "status",
			Usage: "check remote status of all projects",
			Action: func(c *cli.Context) {
				updateGithubStatus(gh, db)
				status(db)
			},
		},
	}

	app.Run(os.Args)
}
