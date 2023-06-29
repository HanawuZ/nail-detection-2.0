package main

import (
	"net/http"

	"github.com/HanawuZ/nail-detection-2.0/configs"
	"github.com/HanawuZ/nail-detection-2.0/routes"
	"github.com/gin-gonic/gin"
)

// const uri = "mongodb://localhost:27017"

func CORSMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "*")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "*")

		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}
		c.Next()

	}
}

func main() {

	r := gin.Default()
	r.Use(CORSMiddleware())

	configs.ConnectDB()

	r.GET("/", func(ctx *gin.Context) {

		ctx.JSON(http.StatusOK, gin.H{
			"hello": "world",
		})
	})

	routes.UserRoute(r)
	routes.NailRoute(r)

	r.Run()

}
