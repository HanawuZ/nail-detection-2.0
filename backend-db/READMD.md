# Backend & Database of nail detection for collecting data

## first step to run code - you need to install go-lang and set go path

1. download _go Language_ from website ([Golang](https://go.dev/dl/)) - windows load .msi // mac load .pkg

2. set gopath like this video ([GoPath](https://www.youtube.com/watch?v=kjr3mOPv8Sk)) - set all os (if not set gopath will on c drive)

3. if you need to init a new project you can create new folder and use `go mod init github.com/[GithubName]/[GithubProjectName]`

4. if you want a continue form this code can use `go mod tidy` to install all module

5. from 3. in link is mean github url of your project

6. create `main.go` file and you can run everything on this file 

7. if you want to install some module - can use `go get -u [module-name]`

8. let's fun with golang

## if you want to run a database mongo on local you need to read this

1. download docker to local (PC/Notebook) 

2. run docker compose on directory backend-db [`cd backend-db`]

3. run `docker compose up -d`

4. start write code with mongodb

## Build and Deploy
1. Following this link
https://medium.com/@vngauv/from-github-to-gce-automate-deployment-with-github-actions-27e89ba6add8