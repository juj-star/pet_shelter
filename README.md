### Prerequisites

Before running this project, you'll need to install Docker Desktop on your system. Here are the instructions for each operating system:

- For Mac: [Install Docker Desktop on Mac](https://docs.docker.com/desktop/install/mac-install/)
- For Windows: [Install Docker Desktop on Windows](https://docs.docker.com/desktop/install/windows-install/)
- For Linux: [Install Docker Desktop on Linux](https://docs.docker.com/desktop/install/linux-install/)

Ensure that Docker is running on your machine before proceeding to the next steps.

### Installing

First, clone the repository to your local machine:

```bash
git clone https://github.com/juj-star/pet_shelter.git
```

Change directory to the project:

```bash
cd pet_shelter
```

Build the Docker containers:

```bash
docker-compose build
```

Start Docker containers:

```bash
docker-compose up
```

### Accessing the website

Enter this in your browser's address bar:

[localhost:8000](localhost:8000)

### Stopping the application

You can of course quit docker to stop the containers.  You can also use this docker command:

```bash
docker-compose down
```

### Tips

#### Admin 

The admin username and password is admin:admin

#### Deleting the database

If you would like to delete the database and start fresh, first stop the containers:

```bash
docker-compose down
```

Navigate to the Volumes list in Docker Desktop.  Select and delete the volume named "pet_shelter_mongodb_data".

Rebuild the containers:

```bash
docker-compose build
```

Start the containers again:

```bash
docker-compose up
```

#### Creating test users

To create test users, go to this endpoint:

[localhost:8000/generate_test_users](localhost:8000/generate_test_users)

This will create 10 test users.  The password for all test users is "password".  Be careful while using this endpoint since each time you access it will create 10 users.

#### Syncing up changes being made to the repo

The code changes to the repo is very active at times, to sync up the changes go to the project directory and:

```bash
git pull
```
