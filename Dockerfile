# Use the official Go image
FROM golang:1.9

# Set the working directory inside the container
WORKDIR /app

# Copy the Go project files into the container
# This will copy all files and directories inside backend-db
COPY /backend-db/. .   

# Build the Go project
RUN go mod tidy
RUN go mod verify
RUN go build -o main .

# Expose the port your Go Gin application is using
EXPOSE 8080

# Command to run your application
CMD ["./main"]
