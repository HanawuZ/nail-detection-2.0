# version of python
FROM python:3.9.12-alpine

COPY /UI-tinker/src/ /app/
# Download Package 
RUN apt-get update -y

# install Dependencies
RUN apt-get install tk -y

# Command to run Tkinter application
CMD [ "/" ]

