package routes

import (
	"github.com/HanawuZ/nail-detection-2.0/controllers"
	"github.com/gin-gonic/gin"
)

func NailRoute(router *gin.Engine) {
	router.POST("/nail", controllers.CreateNail)

	router.GET("/nail/:pid", controllers.GetAllNailByID)

	router.GET("/nail", controllers.GetAllNail)
}
