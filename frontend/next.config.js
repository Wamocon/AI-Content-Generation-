/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  // Enable standalone output so Docker runner can use server.js
  output: 'standalone',
  
  // Properly expose environment variables to both client and server
  env: {
    // Server-side (for SSR and API routes)
    BACKEND_URL: process.env.BACKEND_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    WS_URL: process.env.WS_URL || process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/ws',
    
    // Client-side (these will be available as process.env.* on client)
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    NEXT_PUBLIC_WS_URL: process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/ws',
  },
  images: {
    unoptimized: true,
  },
  // Remove output: 'export' for development server
  // output: 'export', 
  // Use default .next directory for development
  // distDir: '../app/static/dist',
  trailingSlash: false, // Disable trailing slash for development
  
  // Add webpack configuration for better development experience
  webpack: (config, { dev, isServer }) => {
    if (dev) {
      config.devtool = 'eval-source-map'
      // Fix chunk loading issues
      config.optimization = {
        ...config.optimization,
        splitChunks: {
          chunks: 'all',
          cacheGroups: {
            default: {
              minChunks: 2,
              priority: -20,
              reuseExistingChunk: true,
            },
            vendor: {
              test: /[\\/]node_modules[\\/]/,
              name: 'vendors',
              priority: -10,
              chunks: 'all',
            },
          },
        },
      }
    }
    return config
  },
  
  // Add experimental features for better development
  experimental: {
    optimizePackageImports: ['lucide-react', '@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu'],
    // Fix chunk loading in development
    esmExternals: false,
  },
  
  // Ensure proper network binding for development
  async rewrites() {
    return []
  },
  
  // Development server configuration
  ...(process.env.NODE_ENV === 'development' && {
    compress: false,
    poweredByHeader: false,
    // Fix chunk loading issues
    onDemandEntries: {
      maxInactiveAge: 25 * 1000,
      pagesBufferLength: 2,
    }
  })
}

module.exports = nextConfig
