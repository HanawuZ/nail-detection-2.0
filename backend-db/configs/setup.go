package configs

import (
	"context"
	"fmt"
	"log"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func ConnectDB() *mongo.Client {
	uri := EnvMongoURI()

	serverAPI := options.ServerAPI(options.ServerAPIVersion1)
	opts := options.Client().ApplyURI(uri).SetServerAPIOptions(serverAPI)

	client, err := mongo.Connect(context.TODO(), opts)

	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Connected to MongoDB")
	return client

}

var DB *mongo.Client = ConnectDB()

func GetColection(client *mongo.Client, collectionName string) *mongo.Collection {
	collection := client.Database("Nail").Collection(collectionName)
	return collection
}
