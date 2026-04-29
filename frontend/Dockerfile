# Build stage
FROM node:18-alpine as builder

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the project (if needed)
RUN npm run build 2>/dev/null || true

# Production stage
FROM node:18-alpine

WORKDIR /app

# Install a simple HTTP server for static files
RUN npm install -g serve

# Copy built files from builder
COPY --from=builder /app/dist ./dist/
COPY --from=builder /app/index.html ./dist/index.html
COPY --from=builder /app/style.css ./dist/style.css
COPY --from=builder /app/app.js ./dist/app.js

# Create dist directory if needed
RUN mkdir -p dist

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:3000 || exit 1

# Expose port
EXPOSE 3000

# Environment
ENV NODE_ENV=production

# Start the application
CMD ["serve", "-s", "dist", "-l", "3000"]
