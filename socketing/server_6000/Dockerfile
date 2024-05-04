FROM golang:1.22.2

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Compile the Java program
RUN go build

# Expose port 4000 to the outside once the container has launched
EXPOSE 4000

# Run Program.java when the container launches
CMD ["./factoring"]

