# Planning Poker

The Planning Poker Platform is a web application designed for facilitating planning poker sessions, a technique used in agile project management for estimating work. With intuitive user interfaces and real-time updates, this platform streamlines the planning process for teams.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Usage](#usage)
## Features

- **Room Creation**: Administrators can easily create rooms and generate unique room IDs for participants.
- **Multi-Team Support**: Multiple teams can use the application concurrently, allowing for seamless collaboration.
- **Participant Management**: Participants join rooms by providing their usernames, with the option for administrators to password-protect rooms for added security.
- **Voting Interface**: Participants select from a range of modified Fibonacci sequence cards for voting, with real-time updates and the ability to change votes.
- **Transparency**: Administrators have control over revealing and clearing votes, ensuring transparency and fairness in decision-making.

## Requirements

- **Docker**: Ensure that Docker is installed on your system. You can download and install Docker Desktop from the [official Docker website](https://www.docker.com/).

- **Docker Compose**: Docker Compose is used for orchestrating multi-container Docker applications. It should be included with Docker Desktop installation on most platforms. If not, make sure to install Docker Compose separately following the instructions provided on the [Docker Compose documentation](https://docs.docker.com/compose/install/).

## Getting Started

### Installation

1. **Install Docker and Docker Compose**: If you haven't already, download and install Docker Desktop from the [official Docker website](https://www.docker.com/). Docker Compose is usually included with Docker Desktop, but if not, you can install it separately following the instructions provided on the [Docker Compose documentation](https://docs.docker.com/compose/install/).

2. **Clone the repository**: Clone the repository to your local machine using Git:
    ```bash
    git clone https://gitlab.deployed.pl/rekrutacja/dawid-gurgul-planning-poker.git
    ```

2. **Navigate to the config directory**:
    ```bash
    cd config
    ```

4. **Set Up Environment Variables**: Create a `.env` file in the **config** directory of the project and specify any required environment variables. You can use the provided `.env.sample` file as a template and replace the placeholders with your actual values.

5. **Build Docker containers**: Use Docker Compose to build the Docker containers defined in the `docker-compose.yml` file:
    ```bash
    docker-compose build
    ```

### Usage
1. **Navigate to the config directory**:
    ```bash
    cd config
    ```

2. **Start Docker containers**: Start the Docker containers using Docker Compose:
    ```bash
    docker-compose up
    ```
