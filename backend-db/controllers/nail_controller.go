package controllers

import (
	"context"
	"net/http"
	"time"

	"github.com/HanawuZ/nail-detection-2.0/configs"
	"github.com/HanawuZ/nail-detection-2.0/models"
	"github.com/HanawuZ/nail-detection-2.0/responses"
	"github.com/gin-gonic/gin"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
)

var nailCollection *mongo.Collection = configs.GetColection(configs.DB, "nails")

func CreateNail(c *gin.Context) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	var nail models.Nail
	defer cancel()

	if err := c.ShouldBindJSON(&nail); err != nil {
		c.JSON(http.StatusBadRequest, responses.NailResponse{
			Status:  http.StatusBadRequest,
			Message: "error",
			Data: map[string]interface{}{
				"data": err.Error(),
			},
		})
		return
	}

	//use the validator library to validate required fields
	if validationErr := Validate.Struct(&nail); validationErr != nil {
		c.JSON(http.StatusBadRequest, responses.UserResponse{Status: http.StatusBadRequest, Message: "error", Data: map[string]interface{}{"data": validationErr.Error()}})
		return
	}

	newNail := models.Nail{
		Id:             primitive.NewObjectID(),
		PatientID:      nail.PatientID,
		PatientName:    nail.PatientName,
		PatientSurname: nail.PatientSurname,
		Age:            nail.Age,
		Date:           time.Now(),
		Data:           nail.Data,
	}

	result, err := nailCollection.InsertOne(ctx, newNail)

	if err != nil {
		c.JSON(http.StatusInternalServerError, responses.UserResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": err.Error()}})
		return
	}

	c.JSON(http.StatusCreated, responses.UserResponse{Status: http.StatusCreated, Message: "success", Data: map[string]interface{}{"data": result}})

}

// find all of data of usersId
func GetAllNailByID(c *gin.Context) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	patientId := c.Param("pid")
	var nails []models.Nail
	defer cancel()

	filter := bson.D{
		{Key: "patientid", Value: patientId},
	}
	// fmt.Println(filter)

	cursor, err := nailCollection.Find(ctx, filter)
	if err != nil {
		panic(err)
	}

	defer cursor.Close(ctx)

	if err = cursor.All(ctx, &nails); err != nil {
		panic(err)
	}

	c.JSON(
		http.StatusOK,
		responses.NailResponse{
			Status:  http.StatusOK,
			Message: "success",
			Data: map[string]interface{}{
				"data": nails,
			},
		},
	)
}

// find all of data of usersId
func GetAllNail(c *gin.Context) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	// patientId := c.Param("pid")
	var nails []models.Nail
	defer cancel()

	filter := bson.D{}
	// fmt.Println(filter)

	cursor, err := nailCollection.Find(ctx, filter)
	if err != nil {
		panic(err)
	}

	defer cursor.Close(ctx)

	if err = cursor.All(ctx, &nails); err != nil {
		panic(err)
	}

	c.JSON(
		http.StatusOK,
		responses.NailResponse{
			Status:  http.StatusOK,
			Message: "success",
			Data: map[string]interface{}{
				"data": nails,
			},
		},
	)
}
