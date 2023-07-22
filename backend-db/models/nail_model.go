package models

import (
	"time"

	"go.mongodb.org/mongo-driver/bson/primitive"
)

type Nail struct {
	Id             primitive.ObjectID `json:"id,omitempty"`
	PatientID      string             `json:"pid"`
	PatientName    string             `json:"pname"`
	PatientSurname string             `json:"psurname"`
	Age            uint               `json:"age"`
	Date           time.Time          `json:"date,omitempty"`
	Data           []float64          `json:"data"`
}
