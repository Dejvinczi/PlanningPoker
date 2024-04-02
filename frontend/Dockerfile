# Use Node.js image with tag "20.11-alpine"
FROM node:20.11-alpine

# Set container workdir directory
WORKDIR /app

# Copy source code to the working directory
COPY ./app .

# Install dependencies from package.json without optional dependencies
RUN npm install --omit=optional

# Expose port 3000 for access to server
EXPOSE 3000

# Start React development server
CMD ["npm", "start"]