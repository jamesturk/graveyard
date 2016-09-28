package main

import (
	"database/sql"
	_ "github.com/mattn/go-sqlite3"
	"gopkg.in/gorp.v1"
	"log"
	"time"
)

// various tables
type Config struct {
	Id          int
	GithubToken string
}

type Repository struct {
	Id int

	// GitHub
	Owner           string
	Name            string
	HasIssues       bool
	HasWiki         bool
	OpenIssuesCount int
	ForksCount      int
	WatchersCount   int
	UpdatedAt       string
	Language        string

	// Travis
	TravisID            int
	LastBuildState      string
	LastBuildFinishedAt string

	// Coveralls
	CoveragePercent int

	// PyPI
	LatestRelease     string
	LatestReleaseTime time.Time
	Wheel             bool

	// meta
	LastSync time.Time
}

// initialize DbMap object, creating it if it doesn't exist
func initDB() *gorp.DbMap {
	db, err := sql.Open("sqlite3", "kqu.db")
	checkErr(err, "could not open kqu.db")

	dbmap := gorp.DbMap{Db: db, Dialect: gorp.SqliteDialect{}}

	dbmap.AddTableWithName(Repository{}, "repositories").SetKeys(true, "Id")
	dbmap.AddTableWithName(Config{}, "config").SetKeys(true, "Id")

	err = dbmap.CreateTablesIfNotExists()
	checkErr(err, "failed to create tables")

	return &dbmap
}

func getConfig(db *gorp.DbMap) *Config {
	var configs []Config
	db.Select(&configs, "select * from config")
	if len(configs) == 0 {
		config := Config{}
		err := db.Insert(&config)
		checkErr(err, "no config table")
		return &config
	} else if len(configs) == 1 {
		return &configs[0]
	} else {
		log.Fatalln("multiple configs?!")
		return nil
	}
}

func saveConfig(db *gorp.DbMap, config *Config) {
	count, err := db.SelectInt("select count(*) from config")
	checkErr(err, "database error")
	if count == 0 {
		err = db.Insert(config)
	} else {
		_, err = db.Update(config)
	}
	checkErr(err, "database error")
}

// get a repository by name
func getRepository(db *gorp.DbMap, name string) *Repository {
	var repos []Repository
	db.Select(&repos, "select * from repositories where LastSync < (date('now', '-1 day'))")

	switch len(repos) {
	case 0:
		log.Fatalln("no such repository:", name)
	case 1:
		return &repos[0]
	default:
		log.Fatalln("multiple repositories w/ name:", name)
	}
	return nil
}

// save repository (creating if it doesn't exist)
func saveRepository(db *gorp.DbMap, repo *Repository) {
	count, err := db.SelectInt("select count(*) from repositories where owner=? and name=?",
		repo.Owner, repo.Name)
	checkErr(err, "database error")
	if count == 0 {
		err = db.Insert(repo)
	} else {
		_, err = db.Update(repo)
	}
	checkErr(err, "database error")
}
