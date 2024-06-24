/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://127.0.0.1:5000/:path*', // Proxy to Flask
        has: [
          {
            type: 'query',
            key: 'nextauth',
          },
        ],
      },
    ];
  },
};

export default nextConfig;
