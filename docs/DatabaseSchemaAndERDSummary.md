# 🗄️ Final Database Schema Summary

## 🎶 Core Music Catalog

| Table                | Description                                         |
| -------------------- | --------------------------------------------------- |
| tracks               | Track details (title, duration, ISRC, lyrics, etc.) |
| albums               | Album grouping for tracks                           |
| artists              | Individual artists and groups                       |
| artist_groups        | Defines artist groups and solo artists              |
| artist_group_members | Mapping of artists to their groups (many-to-many)   |
| track_artists        | Polymorphic: maps artists/groups to tracks          |
| audio_files          | Metadata: format, bitrate, file path                |
| fingerprints         | Audio hashes used for recognition                   |

## 📄 Ownership & Rights

| Table            | Description                               |
| ---------------- | ----------------------------------------- |
| track_ownerships | Polymorphic: who owns what % of the track |
| royalty_shares   | Revenue share among contributors          |

## 📡 Radio Detection & Monitoring

| Table              | Description                                           |
| ------------------ | ----------------------------------------------------- |
| radio_stations     | Station metadata (location, name)                     |
| radio_airplay_logs | Detected plays: station, timestamp, track, confidence |

## 🔔 Trigger Logic

- PostgreSQL AFTER INSERT trigger on radio_airplay_logs
- Sends notification via pg_notify() when a new match is detected
- Can push to:
  - Email/Slack alerts
  - Background job queues
  - Webhook listeners

## 📊 Aggregated Reports

- By Artist: Total airplays, royalties
- By Track: Play counts, exposure
- By Station: Which stations play what, when
- Available via materialized views or reporting endpoints

## 👥 System Actors & Roles

| Actor                 | Role/Responsibilities                                                                                    |
| --------------------- | -------------------------------------------------------------------------------------------------------- |
| Catalog Administrator | - Manages artist, track, and album metadata<br>- Uploads audio files and lyrics                          |
| Rights Holder         | - Assigns ownership/royalty splits<br>- Registers ISRC codes<br>- Views royalty reports                  |
| Radio Monitor         | - Monitors radio matches<br>- Investigates unlicensed usage<br>- Confirms detections                     |
| Developer/Engineer    | - Integrates audio matching engine<br>- Maintains fingerprinting system<br>- Handles backend scalability |
| Business Analyst      | - Generates reports by station/artist/region<br>- Uses aggregated insights for marketing/licensing       |
| Artist/Label          | - May access a dashboard to view plays, revenue, exposure                                                |

## 🎵 Music Catalog ERD (Simplified Overview)

```
[artists]                [artist_groups]
   │                            │
   └──< artist_group_members >──┘

[artists]
   │
   └──< track_artists >── [tracks] ──< [audio_files]
                                 │
                                 └──< [albums]

[tracks] ──< [fingerprints]
    │
    └──< [track_ownerships]
    └──< [royalty_shares]

[tracks] ──< [radio_airplay_logs] >── [radio_stations]
```

**Relationships:**

- Polymorphic Relationships: track_ownerships and royalty_shares can refer to either artists or artist_groups via owner_type / recipient_type.
- Triggers: radio_airplay_logs has a trigger that alerts when a new match is logged.

✅ The SQL schema with all required tables and triggers has been created.

✅ Tech Stack

    Next.js (React framework with server-side rendering and file-based routing)

    TypeScript (strict typing and better developer experience)

    Tailwind CSS (utility-first styling)

    React Query (for data fetching, caching, and server syncing)

    Axios (for HTTP requests via a centralized API service layer)

    React Hook Form (for form and file input handling with validation)

    Context API (for lightweight shared state like theme or auth)

    Redux Toolkit (for complex or deeply shared state, only if necessary)

    ESLint + Prettier (for linting and code formatting)

    Vitest + React Testing Library (or Jest for more mature Next.js testing support)

✅ Best Practices

    Use functional components and React Hooks exclusively (no class components).

    Prefer Context API for lightweight shared state, and Redux Toolkit for global app-wide state.

    Use React Query for all remote data handling (fetching, caching, pagination, etc.).

    Create a centralized API service layer using Axios and expose logic via custom hooks (e.g., useUpload()).

    Use React Hook Form for file upload forms and integrate validation.

    Use FormData for file uploads; support upload progress and error states.

    Ensure all API logic is abstracted away from UI components.

    Structure code using a feature-based folder structure, e.g.:

/features/
/upload/
UploadForm.tsx
useUpload.ts
uploadAPI.ts

Follow a11y best practices: label inputs, use semantic HTML, and ensure keyboard accessibility.

Keep all components small, reusable, and single-purpose.

All code must conform to ESLint and Prettier rules.

Separate business logic from UI logic cleanly.

Write unit tests for logic and integration tests for components (mock API with MSW).

✅ Recommended Project Directory Structure

frontend-app/
├── public/ # Static assets (images, icons, etc.)
├── src/
│ ├── app/ or pages/ # Routing system (use app/ if using Next.js App Router)
│ │ └── index.tsx # Home page
│ │ └── upload/page.tsx # Upload page (if using App Router)
│
│ ├── components/ # Reusable UI components
│ │ └── Button.tsx
│ │ └── FileInput.tsx
│ │ └── Loader.tsx
│
│ ├── features/ # Feature-based folders (recommended for scaling)
│ │ └── upload/
│ │ ├── UploadForm.tsx
│ │ ├── useUpload.ts # Custom React Query hook
│ │ ├── uploadAPI.ts # Axios calls for upload
│ │ └── types.ts # Types/interfaces specific to upload feature
│
│ ├── context/ # React Contexts for shared state
│ │ └── AuthContext.tsx
│
│ ├── hooks/ # Generic reusable hooks
│ │ └── useToast.ts
│ │ └── useIsMounted.ts
│
│ ├── store/ # Redux Toolkit (if needed)
│ │ └── index.ts
│ │ └── uploadSlice.ts
│
│ ├── api/ # Centralized API services using Axios
│ │ ├── axios.ts # Axios instance with interceptors
│ │ └── user.ts # User-related API calls
│
│ ├── utils/ # Utility functions/helpers
│ │ └── fileHelpers.ts
│ │ └── formatters.ts
│
│ ├── styles/ # Global styles (Tailwind setup or other global CSS)
│ │ └── globals.css
│ │ └── tailwind.config.ts
│
│ ├── types/ # Shared TypeScript types
│ │ └── index.ts
│
│ ├── tests/ # Optional: for placing shared test utilities/mocks
│ │ └── mockServer.ts
│
│ └── app.d.ts # TypeScript declarations
│
├── .eslintrc.js # Linting config
├── .prettierrc # Formatting config
├── tsconfig.json # TypeScript config
├── tailwind.config.js # Tailwind config
├── package.json
└── README.md

📌 Notes

    features/: Keeps your code modular and scalable by grouping logic, UI, and data together by domain.

    hooks/: Place shared logic like custom hooks unrelated to any single feature.

    api/: Central place for managing all HTTP requests using Axios with a base config.

    context/ vs store/: Use Context for light state (theme/auth), Redux Toolkit only when the app grows.

    Testing: Optionally group test utilities or mocks in tests/, or colocate .test.tsx files next to components.
