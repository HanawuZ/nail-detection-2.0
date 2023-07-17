package samples

import (
	// "github.com/HanawuZ/nail-detection-2.0/configs"
	"time"

	. "github.com/HanawuZ/nail-detection-2.0/models"
)

func GetSampleNailData() Nail {
	return Nail{
		PatientID:      "HN1223345",
		PatientName:    "John",
		PatientSurname: "Doe",
		Date:           time.Now(),
		Data:           []float64{12.4, 13.2, 15.2, 18.4, 19.34},
	}
}
