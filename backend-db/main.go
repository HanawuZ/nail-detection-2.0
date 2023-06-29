package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

const uri = "mongodb://localhost:27017"

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

	r.GET("/", func(ctx *gin.Context) {
		ctx.JSON(http.StatusOK, gin.H{
			"hello": "world",
		})
	})

	r.Run()

}

// func main() {
// 	fmt.Println("tell me Hello world")

// 	serverAPI := options.ServerAPI(options.ServerAPIVersion1)
// 	opts := options.Client().ApplyURI(uri).SetServerAPIOptions(serverAPI)

// 	client, err := mongo.Connect(context.TODO(), opts)

// 	if err != nil {
// 		panic(err)
// 	}

// 	defer func() {
// 		if err = client.Disconnect(context.TODO()); err != nil {
// 			panic(err)
// 		}
// 	}()

// 	var result bson.M
// 	if err := client.Database("admin").RunCommand(context.TODO(), bson.D{{
// 		Key: "ping",
// 		Value: 1,
// 	}}).Decode(&result); err != nil {
// 		panic(err)
// 	}
// 	fmt.Println("Pinged your deployment. You successfully connected to MongoDB!")
// }
