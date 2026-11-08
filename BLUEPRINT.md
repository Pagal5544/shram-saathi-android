# Shram Saathi — Product & Technical Blueprint

**Version:** 1.0  
**Status:** Planning baseline  
**Platform:** Android-first  
**Repository:** Pagal5544/shram-saathi-android

---

## 1. Vision and product definition

Shram Saathi is a two-way local labour marketplace. It connects people who offer labour with people who need work done.

It is more than a job board and more than a worker directory:
- Workers create profiles, publish skills, wage expectations and availability, and discover nearby jobs.
- Contractors and customers publish work requirements and discover nearby workers.
- Either side can initiate an application, invitation or work request.
- Both parties negotiate and explicitly agree to wage, dates, working hours and scope before a booking is confirmed.

### Product outcomes
1. Reduce the time required to find suitable nearby workers.
2. Help workers discover legitimate nearby earning opportunities.
3. Make wage units and work expectations transparent.
4. Support repeat hiring and reputation built from completed work.
5. Start locally, validate the model and expand gradually.

## 2. User roles and permissions

### Worker
- Maintain profile, locality, skills and experience.
- Set wage expectations with an explicit unit: hour, day, task, month or negotiable.
- Set availability and travel radius.
- Browse and filter jobs.
- Apply to jobs and respond to invitations.
- Accept, reject or counter wage offers.
- View bookings and work history.
- Rate an employer after completion.
- Report or block abusive accounts.

### Contractor
- Create and manage multiple job posts.
- Search workers by skill, location, availability, experience and wage.
- Invite workers, review applications and shortlist.
- Negotiate wage and work terms.
- Book individuals or teams.
- Track active and completed work.
- Rate workers after completion and re-invite previous workers.

### Customer / Employer
An individual, household, farmer, shop, builder, business or organisation hiring for a specific need. The customer workflow should be simpler than the contractor workflow while retaining the same transparent agreement and safety controls.

### Multi-role account
A single verified phone account may have Worker, Contractor and Customer roles. Role switching changes dashboard actions; it must not create duplicate accounts for one phone number.

### Admin / Moderator
- Manage categories and skills.
- Review reports and disputes.
- Moderate users and job posts.
- Review optional verification submissions.
- View operational metrics and audit logs.
- Use least-privilege permissions and stronger authentication.

---

## 3. Core user journeys

### 3.1 Worker onboarding
1. Select language.
2. Enter mobile number and verify OTP.
3. Select Worker role.
4. Add display name and locality; profile photo is optional.
5. Select one or more work categories.
6. Set skill level and experience for each skill.
7. Set expected wage and wage unit.
8. Set availability and travel radius.
9. Review profile visibility and privacy settings.
10. Publish profile.

Use progressive onboarding. Minimum initial profile: verified phone, display name, locality and at least one skill. Let the worker add more details later.

### 3.2 Employer posts a job
1. Open Contractor or Customer dashboard.
2. Tap “Post a job”.
3. Select work category and describe the work.
4. Enter number of workers and required skill level.
5. Set work locality / map pin.
6. Enter start date, end date or duration, and working hours.
7. Enter wage range, wage unit and payment frequency.
8. Add optional facilities: food, accommodation, transport and tools.
9. Preview and publish.
10. Receive matching worker suggestions and applications.

### 3.3 Worker applies
1. Browse nearby jobs.
2. Filter by skill, distance, date, wage and duration.
3. Open job details and review employer information.
4. Apply with proposed wage and optional note.
5. Track pending, shortlisted, offered, accepted, declined or withdrawn status.

### 3.4 Employer finds workers
1. Choose skill and work location.
2. Set distance, availability, experience and wage filters.
3. View matching workers in list or map.
4. Open profile and relevant completed-work reviews.
5. Invite worker to a job or send a direct work request.
6. Compare responses and negotiate.
7. Confirm booking after mutual acceptance.

### 3.5 Wage negotiation
- Employer sends an offer containing amount, unit, dates, hours and work scope.
- Worker can accept, reject or counter.
- Employer can accept, reject or counter again.
- Every offer is an immutable history record; a counter creates a new offer linked to the previous one.
- Booking is created only when both parties accept the same current offer.
- Store agreed terms as a snapshot on the booking so later profile or job edits cannot silently change the agreement.
- Show wage unit everywhere. Never display an amount without its unit.

### 3.6 Completion and review
1. Booking moves to In Progress.
2. Work completion can be marked by one party and confirmed by the other, with a dispute path.
3. Either party can report an issue before closure.
4. On completion, both parties may leave one review each.
5. Rehire creates a new invitation; previous terms are suggestions, not automatic commitments.

---

## 4. Functional scope

### P0 — MVP
- OTP authentication.
- Role-aware user account.
- Worker and employer profiles.
- Skill catalogue and experience levels.
- Wage expectations and availability.
- Job create, edit, pause, close and expiry.
- Nearby worker and job discovery.
- Filters and sorting.
- Applications and invitations.
- Offers, counter-offers, accept and reject.
- Booking confirmation, status and history.
- Push notifications for important events.
- Report and block.
- Basic admin moderation and audit log.
- Hindi-first UX with English support.

### P1 — Next release
- Worker teams with leader and member consent.
- Favourite workers and rehire.
- Work portfolio photos.
- Attendance and daily work log.
- In-app chat with abuse reporting.
- Verification tiers.
- Dispute workflow and support tickets.
- Demand analytics by locality and skill.

### P2 — Later
- Payment gateway and digital receipts.
- Escrow only after legal, financial and operational review.
- Business subscriptions and featured jobs.
- Voice-assisted onboarding and low-literacy UX.
- IVR / assisted registration.
- Multi-city and multi-state operations.

---

## 5. Job and skill taxonomy

Initial admin-managed categories:
- Construction: mason, helper, shuttering, bar-bender, tile worker.
- Electrical: electrician, wiring assistant.
- Plumbing: plumber, pipe fitter.
- Carpentry: carpenter, furniture installer.
- Painting: painter, polish worker.
- Agriculture: farm labour, harvesting, sowing, irrigation support.
- Loading: loader, packer, warehouse helper.
- Cleaning: home, office and site cleaning.
- Repair and maintenance: mechanic, appliance repair.
- Other: configurable category and skill.

A worker can list multiple skills. A job has one primary skill and may include secondary skills. Category labels must be localizable in Hindi and English.

---

## 6. Matching and ranking

Matching provides explainable recommendations; it never makes an automatic hiring decision.

### 6.1 Hard eligibility filters
- User profile is active and not suspended.
- Worker has the required skill or an explicitly allowed related skill.
- Worker is available for the requested dates.
- Worker is within the selected radius where location data is available.
- Job is open and not expired.
- Worker has no conflicting confirmed booking, unless multiple-shift availability is explicitly supported.

### 6.2 Initial ranking score
Suggested configurable score, to be calibrated during the pilot:
- Skill fit: 0–35 points.
- Distance fit: 0–20 points.
- Availability fit: 0–20 points.
- Wage compatibility: 0–15 points.
- Relevant experience: 0–10 points.

Total: 100 points.

Show understandable reasons such as “matching skill”, “within 5 km”, “available on requested date” and “wage range overlaps”. Do not rank or filter by caste, religion, gender, disability or other protected / sensitive attributes. Do not infer these attributes.

### 6.3 Wage compatibility
- Compare amounts only when wage units match.
- Do not compare ₹/hour with ₹/day unless an explicit conversion rule is supplied.
- Display currency and wage unit consistently.
- If the worker's expectation and employer's budget do not overlap, allow manual negotiation but rank the match lower.

### 6.4 Location and privacy
- Public discovery uses locality or approximate coordinates.
- Never expose exact worker home coordinates or public live tracking.
- Reveal precise job meeting location only to selected parties when appropriate.
- Ask permission before device location access.
- Support manual locality and map-pin entry when GPS is unavailable.

---

## 7. Booking state machine

Suggested lifecycle:

```text
Job:
DRAFT -> OPEN -> PAUSED -> OPEN
             -> CLOSED
             -> EXPIRED

Application:
PENDING -> SHORTLISTED -> OFFERED
        -> WITHDRAWN
        -> REJECTED

Offer:
SENT -> COUNTERED -> ACCEPTED
     -> REJECTED
     -> WITHDRAWN
     -> EXPIRED

Booking:
CONFIRMED -> IN_PROGRESS -> COMPLETION_PENDING -> COMPLETED
          -> CANCELLED
          -> DISPUTED
```

Rules:
- Only acceptance of the current offer by both parties can confirm a booking.
- Booking records worker, employer, job, agreed terms and timestamps.
- Overlapping shifts are blocked unless explicit multiple-shift availability rules apply.
- Cancellation reason and actor are recorded.
- Completed bookings become eligible for mutual reviews.
- Validate every state transition on the server; never trust client-supplied status changes.

---

## 8. Logical database design

Use UUID primary keys, UTC timestamps and explicit foreign keys. Use PostgreSQL with PostGIS for geographic queries.

### users
- id (UUID, PK)
- phone_e164 (unique)
- display_name
- preferred_language
- account_status
- created_at, updated_at

### user_roles
- id
- user_id (FK users)
- role (WORKER / CONTRACTOR / CUSTOMER / ADMIN)
- status

### worker_profiles
- user_id (PK/FK users)
- bio
- profile_photo_url
- locality, district, state, postal_code
- approximate_location (PostGIS geography point)
- travel_radius_km
- availability_status
- verification_level
- profile_visibility

### skill_categories
- id
- name
- localized_name
- active

### skills
- id
- category_id (FK skill_categories)
- name
- localized_name
- active

### worker_skills
- id
- worker_id (FK worker_profiles)
- skill_id (FK skills)
- skill_level (SKILLED / SEMI_SKILLED / UNSKILLED)
- experience_months
- expected_min_amount
- expected_max_amount
- wage_unit
- notes

### employer_profiles
- user_id (PK/FK users)
- employer_type (INDIVIDUAL / CONTRACTOR / BUSINESS)
- display_name
- business_name (optional)
- locality and contact preferences
- verification_level

### jobs
- id
- employer_id (FK employer_profiles)
- title, description
- category_id, required_skill_level
- worker_count
- locality, district, state, postal_code
- work_location (PostGIS point, protected)
- start_date, end_date, duration
- start_time, end_time
- wage_min, wage_max, wage_unit
- payment_frequency
- facilities (structured JSON)
- status, published_at, expires_at

### applications
- id
- job_id (FK jobs)
- worker_id (FK worker_profiles)
- proposed_amount, wage_unit
- message
- status
- created_at, updated_at
- Unique constraint for one active application per worker per job.

### invitations
- id
- job_id, worker_id, employer_id
- message
- status
- created_at, expires_at

### offers
- id
- job_id, worker_id, employer_id
- application_id (nullable)
- amount, wage_unit
- start_date, end_date, working_hours
- scope_snapshot
- status
- previous_offer_id (nullable self-reference)
- created_at, expires_at

### bookings
- id
- job_id, worker_id, employer_id
- accepted_offer_id
- agreed_terms_snapshot
- status
- started_at, completed_at, cancelled_at

### reviews
- id
- booking_id
- reviewer_id, reviewee_id
- rating (1–5)
- comment
- created_at
- Unique constraint: one review per reviewer per booking.

### reports
- id
- reporter_id
- target_user_id (nullable)
- job_id (nullable)
- booking_id (nullable)
- reason, details
- status, resolution_notes
- created_at

### notifications
- id
- user_id
- type
- title, body
- data (JSON)
- read_at
- created_at

### audit_logs
- id
- actor_id
- action
- entity_type, entity_id
- metadata (JSON)
- created_at

Add indexes for foreign keys, status, dates and frequent filters. Add GiST indexes for PostGIS columns. Store no OTP in plaintext.

---

## 9. API outline

Base path: `/api/v1`

### Authentication
- `POST /auth/otp/request`
- `POST /auth/otp/verify`
- `POST /auth/logout`
- `POST /auth/refresh`

### Account and profiles
- `GET /me`
- `PATCH /me`
- `GET /workers/{worker_id}`
- `PUT /workers/me/profile`
- `PUT /workers/me/skills`
- `PUT /workers/me/availability`
- `PUT /employers/me/profile`

### Discovery
- `GET /workers/nearby`
- `GET /jobs/nearby`
- `GET /skills`
- `GET /categories`
- `GET /matches/jobs-for-me`
- `GET /matches/workers-for-job/{job_id}`

### Jobs and applications
- `POST /jobs`
- `GET /jobs/{job_id}`
- `PATCH /jobs/{job_id}`
- `POST /jobs/{job_id}/pause`
- `POST /jobs/{job_id}/close`
- `POST /jobs/{job_id}/applications`
- `GET /jobs/{job_id}/applications`
- `POST /applications/{application_id}/withdraw`
- `POST /applications/{application_id}/shortlist`
- `POST /invitations`
- `POST /invitations/{invitation_id}/respond`

### Offers and bookings
- `POST /offers`
- `POST /offers/{offer_id}/counter`
- `POST /offers/{offer_id}/accept`
- `POST /offers/{offer_id}/reject`
- `POST /bookings/{booking_id}/start`
- `POST /bookings/{booking_id}/complete`
- `POST /bookings/{booking_id}/cancel`
- `GET /bookings/me`

### Reviews and safety
- `POST /bookings/{booking_id}/reviews`
- `POST /reports`
- `POST /users/{user_id}/block`
- `GET /notifications`
- `POST /notifications/{notification_id}/read`

All endpoints require request validation, authorization, ownership checks and consistent error responses. Never trust a client-supplied user ID to establish ownership.

---

## 10. Android application architecture

Recommended modules:

```text
android/
├── app/
├── core/
│   ├── common/
│   ├── designsystem/
│   ├── model/
│   ├── network/
│   ├── database/
│   └── location/
└── feature/
    ├── auth/
    ├── onboarding/
    ├── home/
    ├── workerprofile/
    ├── employerprofile/
    ├── jobs/
    ├── workers/
    ├── matching/
    ├── negotiation/
    ├── bookings/
    ├── chat/
    ├── reviews/
    └── settings/
```

Recommended stack:
- Kotlin and Jetpack Compose.
- MVVM with ViewModel and StateFlow.
- Repository layer for API and Room data.
- Retrofit + OkHttp for REST.
- Room for cached feeds and saved data.
- DataStore for preferences and non-sensitive settings.
- Hilt for dependency injection.
- Navigation Compose with role-aware destinations.
- WorkManager for deferrable background sync.
- Android Keystore-backed secure token storage; never hardcode secrets.

UX requirements:
- Hindi-first and English-ready localization.
- Large touch targets and readable typography.
- Short forms with save-and-continue.
- Low-bandwidth support and graceful offline states.
- Clear loading, empty, error and permission-denied states.
- Accessibility labels and scalable text.
- Map is optional; manual locality search must work.

---

## 11. Backend architecture

Suggested FastAPI layout:

```text
backend/app/
├── main.py
├── core/          # settings, auth, logging, security
├── api/v1/        # routers
├── models/        # ORM models
├── schemas/       # request and response models
├── services/      # business rules and matching
├── repositories/  # database access
├── workers/       # notifications and background tasks
└── tests/
```

Use SQLAlchemy or SQLModel with Alembic migrations. Keep business rules in services. Use background jobs for notification fan-out and job expiry. Document endpoints with OpenAPI.

---

## 12. Security, privacy and compliance

- OTP provider must enforce rate limits, resend cooldowns and abuse detection.
- Normalize phone numbers to E.164.
- HTTPS for all traffic.
- Short-lived access tokens and rotating refresh tokens.
- Enforce role and ownership authorization on every protected endpoint.
- Store identity documents only when genuinely necessary, with explicit consent, access controls, retention and deletion policy.
- Do not expose exact home location or public live tracking.
- Location permission is optional; manual locality entry is supported.
- Hide private contact details until the relevant connection stage and consent.
- Provide report, block, moderation and appeal paths.
- Validate uploaded file types and sizes; scan uploads where available.
- Audit admin actions and sensitive data access.
- Define retention and deletion policies before public launch.
- Review applicable Indian privacy, consumer, labour, tax and payment requirements with qualified counsel before operating at scale.

---

## 13. Notifications

Push notifications for:
- New matching job.
- New application.
- Employer invitation.
- Application shortlisted or rejected.
- New offer or counter-offer.
- Offer accepted, rejected or expired.
- Booking confirmed, started, completed or cancelled.
- Report and support status updates.

Do not include sensitive personal information in notification text. Let users control non-essential notifications.

---

## 14. Admin and operations

Admin dashboard:
- User and employer lookup.
- Profile and job moderation.
- Category and skill management.
- Reports and disputes queue.
- Optional verification review.
- Booking and cancellation overview.
- Metrics by locality and skill.
- Spam and abuse controls.
- Admin audit log.

Core metrics:
- Registered active workers.
- Active jobs.
- Worker-to-job match rate.
- Median time to first response.
- Median time to confirmed booking.
- Completion and cancellation rates.
- Repeat hiring rate.
- Worker and employer satisfaction.
- Reports per 100 bookings.

---

## 15. Testing strategy

### Android
- Unit tests for ViewModels, validators and wage formatting.
- Repository tests with fake API.
- Compose UI tests for onboarding, job posting, application and offer flows.
- Navigation tests for worker and employer roles.
- Accessibility and low-end device testing.

### Backend
- Unit tests for matching and offer state transitions.
- API tests for authorization and validation.
- Database tests for constraints and PostGIS queries.
- Concurrency tests for offer acceptance and overlapping bookings.
- Security tests for IDOR, rate limits and role escalation.

### Pilot acceptance criteria
- Worker completes onboarding without assistance.
- Employer can publish a job in a few minutes.
- Nearby results respect skill, date, radius and wage filters.
- No booking is confirmed without both parties accepting the same terms.
- A user cannot read or modify another user's private records.
- Exact worker home coordinates never appear in public search.
- Report and block flows work end-to-end.

---

## 16. Delivery roadmap

### Milestone 0 — Foundation
- Finalize name, categories and Hindi copy.
- Confirm pilot geography.
- Agree privacy and verification policy.
- Create wireframes and API/database contracts.

### Milestone 1 — Android shell
- Gradle project and app modules.
- Theme, navigation and localization.
- Login and onboarding UI.

### Milestone 2 — Profiles
- OTP integration.
- Worker and employer profile APIs.
- Skill catalogue and availability.

### Milestone 3 — Marketplace
- Job posting.
- Nearby search and filters.
- Worker discovery.
- Applications and invitations.

### Milestone 4 — Matching and hiring
- Matching score.
- Wage negotiation.
- Booking state machine.
- Notifications.

### Milestone 5 — Trust and pilot
- Ratings, reports, block and admin.
- Security and performance testing.
- Closed pilot in one locality.
- Iterate from real user feedback.

---

## 17. Decisions to confirm before implementation

1. Pilot city / tehsil and initial search radius.
2. Final app name, icon and brand identity.
3. OTP provider and operating budget.
4. Whether chat is in-app or initially uses consent-based phone contact.
5. Whether payments remain off-platform in MVP.
6. Verification levels and evidence requirements.
7. Initial wage categories and localized skill taxonomy.
8. Customer support and dispute operating process.

These decisions do not block product planning, but they should be settled before the related integrations are implemented.

---

## 18. MVP non-goals

- Automatic assignment without worker consent.
- Public display of exact worker location or phone number.
- Guaranteed worker availability.
- Guarantee of quality or background checks based only on a badge.
- Holding money or promising escrow without a compliant provider and legal review.
- AI-only hiring decisions.
- Nationwide launch before a local pilot validates the workflow.

**Guiding rule:** Make the first connection easy, while keeping the final work agreement transparent, voluntary and mutually confirmed.
