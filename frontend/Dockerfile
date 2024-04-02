# Use Node.js image with tag "20.11-alpine"
FROM node:20.11-alpine

# Copy source code to the working directory
COPY ./app /app

# Set container workdir directory
WORKDIR /app

# Install dependencies from package.json without optional dependencies
RUN npm install --omit=optional

# Expose port 3000 for access to server
EXPOSE 3000

# Start React development server
CMD ["npm", "start"]