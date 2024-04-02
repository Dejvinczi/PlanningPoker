# Use Node.js image with tag "20.11-alpine"
FROM node:20.11-alpine

# Set container workdir directory
WORKDIR /app

# Install package.json and package-lock.json files
COPY ./app/package*.json /app/

# Install dependencies from package.json
RUN npm install

# Copy source code to the working directory
COPY ./app /app

# Expose port 3000 for access to server
EXPOSE 3000

# Start React development server
CMD ["npm", "run", "dev"]