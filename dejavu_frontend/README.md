# Dejavu Music Monitoring Frontend

A modern web application for the Dejavu music fingerprinting and radio airplay monitoring system.

## Features

- **Role-based interface**: Different views for catalog administrators, rights holders, radio monitors, etc.
- **Music Catalog Management**: Track, artist, and album management
- **Airplay Monitoring**: View and analyze radio airplay detections
- **Reports**: Generate and view analytics reports
- **Rights Management**: Manage ownership and royalty shares

## Tech Stack

- **Next.js**: React framework with server-side rendering and file-based routing
- **TypeScript**: For type safety and better developer experience
- **Tailwind CSS**: Utility-first styling framework
- **React Query**: For data fetching, caching, and server syncing
- **React Hook Form**: For form handling with validation
- **Context API**: For lightweight shared state management (auth)
- **Axios**: For HTTP requests via a centralized API service layer

## Getting Started

### Prerequisites

- Node.js 16.8.0 or later
- npm or yarn

### Installation

1. Clone the repository

```bash
git clone <repository-url>
cd dejavu_frontend
```

2. Install dependencies

```bash
npm install
# or
yarn install
```

3. Run the development server

```bash
npm run dev
# or
yarn dev
```

4. Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## User Accounts for Testing

For demonstration purposes, you can log in with the following credentials:

- **Catalog Administrator**: Username: `admin`, Password: any value
- **Rights Holder**: Username: `rights`, Password: any value
- **Radio Monitor**: Username: `monitor`, Password: any value
- **Developer/Engineer**: Username: `dev`, Password: any value
- **Business Analyst**: Username: `analyst`, Password: any value
- **Artist**: Username: `artist`, Password: any value

## Project Structure

```
dejavu_frontend/
├── public/                     # Static assets
├── src/
│   ├── app/                    # Next.js app router pages
│   │   ├── login/              # Login page
│   │   ├── dashboard/          # Dashboard page
│   │   ├── tracks/             # Tracks management
│   │   ├── artists/            # Artists management
│   │   ├── albums/             # Albums management
│   │   ├── airplay-logs/       # Airplay logs
│   │   ├── reports/            # Reports and analytics
│   │   └── ...                 # Other pages
│   │
│   ├── components/             # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Input.tsx
│   │   ├── Layout.tsx
│   │   └── SidebarNav.tsx
│   │
│   ├── context/                # React contexts
│   │   └── AuthContext.tsx
│   │
│   ├── hooks/                  # Custom React hooks
│   │
│   ├── api/                    # API integration layer
│   │
│   ├── utils/                  # Utility functions
│   │
│   ├── styles/                 # Global styles
│   │   └── globals.css
│   │
│   └── types/                  # TypeScript types
│       └── index.ts
│
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── README.md
```

## Backend Integration

This frontend is designed to work with a Django backend. For development purposes, it uses mock data for demonstration. When connecting to a real backend, update the API endpoints in the `api` directory.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
