# Shram Saathi — Android Labour Marketplace

> **काम ढूँढ़ना भी आसान, सही मजदूर ढूँढ़ना भी आसान।**

Shram Saathi is a two-way local labour marketplace for India. Workers register their skills, wage expectations and availability to find nearby work. Contractors, businesses and individuals publish requirements and discover suitable nearby workers.

## Project status

**Planning / Blueprint stage.** This repository currently contains product requirements and the technical blueprint. Android and backend implementation will follow the milestones below.

## User roles

- **Worker:** creates a skill profile, sets expected wages and availability, searches jobs, applies and negotiates.
- **Contractor:** posts hiring requirements, searches workers or teams, shortlists applicants and manages bookings.
- **Customer / Employer:** a household, farmer, shop, builder, business or individual who needs work done.
- **Admin / Moderator:** manages categories, reports, moderation and platform operations.

A single verified account may support more than one role. Users can switch dashboards without creating duplicate accounts.

## MVP features

### Worker
- Mobile OTP sign-in.
- Name, optional photo, locality and preferred language.
- Multiple skills with skilled / semi-skilled / unskilled levels.
- Experience, expected wage and wage unit (hour / day / task / month / negotiable).
- Availability calendar and travel radius.
- Nearby jobs, filters, applications and invitations.
- Wage offers, counter-offers and acceptance.
- Booking history, mutual ratings, report and block.

### Contractor / Customer
- Post jobs with category, description, number of workers, skill level, location, dates, duration, hours and wage range.
- Find workers by skill, distance, availability, experience and wage.
- Invite, shortlist and negotiate with workers.
- Hire individuals or request a team.
- Manage active, completed and cancelled bookings.
- Review workers after completed work.

### Two-way matching
- Workers discover jobs matching skill, distance, wage and availability.
- Employers discover workers matching job requirements, budget and dates.
- Matching provides ranked suggestions; it never hires automatically.
- Both parties explicitly agree to the final wage, schedule and scope.

## Initial job categories

Construction (mason, helper, shuttering, bar-bender, tile worker), electrical, plumbing, carpentry, painting, agriculture, loading / packing, cleaning, repair and maintenance, plus admin-configurable categories.

## Main Android screens

1. Splash, language selection and onboarding.
2. Phone login and OTP verification.
3. Role selection and role-aware home.
4. Worker profile, skills and availability.
5. Nearby jobs feed and job details.
6. Nearby workers search and filters.
7. Create / edit job.
8. Applications, invitations and shortlist.
9. Wage offer and negotiation.
10. Booking details and history.
11. Chat / contact preferences.
12. Ratings, reports and support.
13. Notifications, account and privacy settings.

## Proposed technology

| Layer | Technology |
|---|---|
| Android | Kotlin, Jetpack Compose |
| Architecture | MVVM, Repository, Coroutines / Flow |
| Dependency injection | Hilt |
| Networking | Retrofit + OkHttp |
| Local cache | Room + DataStore |
| Backend | Python FastAPI |
| Database | PostgreSQL + PostGIS |
| Push notifications | Firebase Cloud Messaging |
| Maps | OpenStreetMap-compatible provider |
| Media | S3-compatible object storage |
| API docs | OpenAPI / Swagger |

## Planned repository structure

```text
shram-saathi-android/
├── README.md
├── BLUEPRINT.md
├── docs/
│   ├── API_CONTRACT.md
│   ├── DATABASE_SCHEMA.md
│   ├── UX_FLOWS.md
│   └── SECURITY_AND_PRIVACY.md
├── android/       # Kotlin + Jetpack Compose app (planned)
└── backend/       # FastAPI service (planned)
```

## Development roadmap

| Phase | Deliverable |
|---|---|
| 0 | Product definition, UX flows, database and API contracts |
| 1 | Android app shell, navigation, theme and Hindi / English support |
| 2 | OTP authentication, worker and employer profiles |
| 3 | Job posting, worker search, filters and geo-search |
| 4 | Matching, applications, invitations and wage negotiation |
| 5 | Booking confirmation, status, cancellation and history |
| 6 | Ratings, reports, moderation and admin dashboard |
| 7 | Closed pilot in one city / tehsil and reliability improvements |
| 8 | Teams, analytics, payments and regional expansion |

## Trust, safety and privacy principles

- Verify phone numbers with OTP and apply resend / abuse limits.
- Do not expose a worker's exact home or live location publicly.
- Allow manual locality entry; GPS permission is optional.
- Do not require Aadhaar or sensitive identity documents for basic discovery.
- Collect identity documents only when necessary, with consent and secure retention controls.
- Record the agreed wage, unit, schedule and work scope in each booking.
- Confirm a booking only after both parties accept the same current offer.
- Provide report, block, dispute and cancellation flows.
- Ratings are allowed only after a completed booking.
- Do not imply that verification or ratings guarantee safety or work quality.

## Pilot recommendation

Start in one city or tehsil with a focused set of high-demand skills. Onboard workers first, then local contractors and customers. Measure time-to-first-response, successful connections, time-to-hire, cancellation rate, repeat hiring and worker satisfaction before expanding.

## Documentation

- [Product and Technical Blueprint](BLUEPRINT.md)

## License

No open-source license has been selected. Until a license is added, all rights are reserved by the repository owner.
