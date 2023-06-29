package routes

import (
	"github.com/HanawuZ/nail-detection-2.0/controllers"
	"github.com/gin-gonic/gin"
)

func UserRoute(router *gin.Engine) {
	router.POST("/user", controllers.CreateUser())
}
