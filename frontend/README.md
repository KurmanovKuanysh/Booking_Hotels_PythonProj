# Booking — Frontend

Next.js 15 frontend for the Booking hotel reservation system.

## Stack

- **Next.js 15** (App Router)
- **TypeScript** (strict)
- **Tailwind CSS** — custom design tokens (cream/ink/gold palette)
- **TanStack Query v5** — server state
- **Zustand** — auth state (persisted)
- **React Hook Form + Zod** — form validation
- **Axios** — HTTP client with token refresh interceptor

## Setup

```bash
cp .env.local.example .env.local
npm install
npm run dev
```

## Structure

```
app/
  page.tsx              # Landing
  auth/login            # Login
  auth/register         # Register
  hotels/               # Hotel list + detail
  bookings/             # My bookings
  profile/              # User profile
  admin/                # Admin panel (hotels, users, bookings)
components/
  layout/Navbar.tsx
  layout/Footer.tsx
  ui/                   # Button, Input, Badge, Card, Spinner, Stars, Empty
  hotel/HotelCard.tsx
lib/
  api.ts                # Axios instance + interceptors
  services.ts           # All API calls
  utils.ts              # Helpers (format, cn, etc.)
store/auth.ts           # Zustand auth store
types/index.ts          # All TypeScript types
```

## Environment

| Variable | Default |
|---|---|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` |
