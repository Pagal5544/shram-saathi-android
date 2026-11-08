# Shram Saathi — UI/UX Design Specification

**Status:** Finalized product UI specification  
**Platform:** Android-first  
**Implementation target:** Kotlin + Jetpack Compose + Material 3  
**Document version:** 1.0  
**Repository:** `Pagal5544/shram-saathi-android`

---

## 1. Product design decisions

| Decision | Final choice |
|---|---|
| Design style | Simple, approachable, low-friction |
| Navigation | Six-item bottom navigation |
| Languages | Hindi + English |
| Discovery | List + Map |
| Account model | One account can use Worker and Hiring roles |
| Default theme | Light |
| Primary platform | Android phones, including low-end devices |

### Product promise

**काम ढूँढ़ना और कामगार ढूँढ़ना — दोनों आसान।**

The UI must be understandable to people with limited digital literacy. Prefer familiar words, clear icons, large touch targets, short forms, visible wage units, and obvious next actions.

---

## 2. Design principles

1. **Task-first home:** The first screen immediately helps the user find work or hire workers.
2. **Role-aware, not role-locked:** One account can switch between Worker and Hiring modes without creating another account.
3. **Progressive forms:** Ask only essential information first; reveal optional details when needed.
4. **Transparent wages:** Always show the unit (per day, per hour, per month, or fixed job).
5. **Local discovery:** Let users switch between list and map; do not expose a worker's exact home address.
6. **Consent before commitment:** A booking is confirmed only after both sides accept the final terms.
7. **Low-network resilience:** Preserve drafts and show useful cached information where safe.
8. **Bilingual consistency:** All visible strings must come from localization resources, not hard-coded screen text.

---

## 3. Brand and visual system

### 3.1 Colors

| Token | Hex | Usage |
|---|---|---|
| Primary Green | `#146B45` | Primary actions, selected navigation, links |
| Primary Green Dark | `#0E5134` | Pressed states, strong emphasis |
| Light Green | `#E9F5ED` | Worker surfaces, success backgrounds |
| Warm Orange | `#F4A62A` | Hiring highlights, urgent labels, attention |
| App Background | `#F7F8F5` | Main screen background |
| Surface | `#FFFFFF` | Cards, sheets, forms |
| Main Text | `#252B28` | Headings and body text |
| Secondary Text | `#66716B` | Supporting information |
| Divider | `#E2E8E3` | Separators and outlines |
| Error | `#B3261E` | Validation and destructive errors |
| Success | `#237A45` | Confirmed and completed states |

Use semantic color tokens rather than raw hex values throughout the implementation. Check text/background contrast before release.

### 3.2 Typography

- Devanagari: Noto Sans Devanagari.
- Latin: Roboto.
- Screen title: 22–24sp, semibold.
- Section title: 18sp, semibold.
- Body: 15–16sp.
- Supporting text: 12–14sp.
- Button label: 15–16sp, medium.
- Avoid long uppercase English labels.
- Support Android font scaling without clipping.

### 3.3 Shape, spacing, and elevation

- Main page horizontal padding: 16dp.
- Standard card radius: 16dp.
- Button radius: 12dp.
- Input radius: 12dp.
- Standard spacing scale: 4, 8, 12, 16, 20, 24, 32dp.
- Prefer subtle borders over heavy shadows.
- Minimum interactive target: 48 × 48dp.
- Use icons with text labels for primary actions.

### 3.4 Components

Create reusable Compose components:

- `PrimaryButton`, `SecondaryButton`, `TextAction`
- `AppTopBar`, `RoleSwitcher`, `BottomNavigationBar`
- `WorkerCard`, `JobCard`, `RequirementCard`
- `WageLabel`, `DistanceLabel`, `AvailabilityChip`
- `SkillChip`, `FilterBottomSheet`, `ListMapSwitcher`
- `FormTextField`, `DropdownField`, `DateField`
- `EmptyState`, `LoadingState`, `ErrorState`
- `ConfirmationDialog`, `ReportBlockSheet`

---

## 4. App navigation

The bottom navigation contains exactly six destinations:

| Order | Label | Icon concept | Worker mode | Hiring mode |
|---|---|---|---|---|
| 1 | Home | House | Work summary and recommendations | Hiring summary and recommendations |
| 2 | Jobs | Briefcase | Find and manage applications | Manage posted requirements |
| 3 | Post | Plus circle | Post work availability / seek work | Post a worker requirement |
| 4 | Workers | People | Find team members / worker directory where enabled | Discover workers and teams |
| 5 | Messages | Chat bubble | Conversations and offers | Conversations and offers |
| 6 | Profile | Person | Worker profile and settings | Hiring profile and settings |

### Navigation behavior

- Keep the six destinations stable across the main app.
- The Post destination opens a role-aware action sheet if the user has both roles.
- If only one role is active, open the relevant form directly.
- Show a small unread badge on Messages when applicable.
- Preserve each tab's scroll position and filter state when switching tabs.
- Handle Android system Back consistently: close sheet/dialog, return to previous screen, then exit from Home.
- Do not use the bottom bar on full-screen onboarding, OTP, or critical confirmation flows.

### Role switcher

Place a compact role switcher near the Home app bar/profile area:

- `काम ढूँढ़ रहा हूँ` / `Worker`
- `मजदूर ढूँढ़ रहा हूँ` / `Hiring`

Switching role changes Home, Jobs, Workers, and Post behavior. Messages and Profile remain shared, with role-specific details shown where relevant. Never delete or overwrite the other role's profile when switching.

---

## 5. Screen specifications

## 5.1 Splash and language selection

**Splash**
- Shram Saathi logo.
- Short tagline: `काम और कामगार, एक साथ`.
- Minimal loading indicator only when required.

**Language selection**
- Large Hindi and English selection cards.
- Persist the user's choice.
- Allow language changes later in Profile → Settings.
- Do not infer language from phone number or location.

## 5.2 Authentication

1. Enter mobile number with India country code preselected.
2. Request OTP.
3. Verify OTP.
4. Offer resend with a visible countdown and clear error messages.
5. Provide change-number action.
6. Never ask for Aadhaar to access basic discovery.

Phone verification status should be visible without exposing the full number publicly.

## 5.3 Onboarding and role setup

Show two large selectable cards:

- **मुझे काम चाहिए** — Worker
- **मुझे मजदूर चाहिए** — Hiring / Contractor

Allow both roles to be selected. The user can add the second role later from Profile.

Collect minimum profile information first:
- Name
- Preferred language
- Broad locality / area
- Role selection

Ask for optional profile details contextually, not all on one intimidating form.

## 5.4 Worker Home

**Top area**
- Greeting and first name.
- Current locality (editable).
- Notification icon.
- Role switcher.

**Main content**
1. Availability control: Available / Not available.
2. Search jobs action.
3. Recommended jobs based on skills and locality.
4. Nearby jobs preview.
5. My applications and active bookings.
6. Complete-profile reminder when required.

**Primary CTA:** `काम खोजें` / `Find Work`.

Do not show a misleading empty earnings or rating total for a new user. Use a helpful empty state instead.

## 5.5 Hiring Home

**Top area**
- Greeting.
- Locality.
- Notification icon.
- Role switcher.

**Main content**
1. Prominent `मजदूर चाहिए` / `Post Requirement` action.
2. Active requirements and their statuses.
3. New applications.
4. Nearby available workers.
5. Current bookings.
6. Quick action for urgent hiring.

**Primary CTA:** `मजदूर ढूँढ़ें` / `Find Workers`.

## 5.6 Jobs tab

**Worker mode**
- Search field.
- Filters: skill, locality/distance, wage range, wage unit, date, duration, availability.
- Sort: nearest, newest, wage.
- Job cards with job title, wage + unit, distance, required headcount, duration, start date, and Apply action.
- Tabs/filters for All, Applied, Shortlisted, Accepted, Completed.

**Hiring mode**
- List of the user's requirements.
- Status filters: Draft, Open, Reviewing, Partially Filled, Filled, Cancelled, Completed.
- Each card shows role/skill, headcount, location area, wage, start date, and application count.
- Open a requirement to review applicants and edit/cancel when permitted.

## 5.7 Post tab

Open a role-aware action sheet:

**Worker actions**
- Set availability.
- Publish a work-seeking profile.
- Optionally post availability for a group/team.

**Hiring actions**
- Post a worker requirement.
- Mark as urgent.
- Save as draft.

### Worker availability form

Required:
- Work category / skills.
- Skilled, semi-skilled, or unskilled.
- Expected wage and unit.
- Availability date.
- Broad locality.

Optional:
- Experience.
- Travel radius.
- Team size.
- Work preferences.

### Hiring requirement form

Required:
- Work category and short description.
- Number of workers.
- Skill level.
- Work locality.
- Start date.
- Duration / work hours.
- Offered wage and unit.

Optional:
- Facilities: food, accommodation, transport.
- Work instructions.
- Photos.
- Urgent flag.

Form behavior:
- Use dropdowns/chips for common choices.
- Use numeric keypad for headcount and wage.
- Show wage unit next to the amount.
- Validate inline and explain how to fix errors.
- Save draft locally when the user leaves a partially completed form.
- Show a preview before publishing.

## 5.8 Workers tab

This tab is primarily for Hiring mode. In Worker mode it can show team discovery / nearby worker directory only if enabled by product rules; otherwise provide a clear route to manage a team profile.

**Search controls**
- Search by skill or work category.
- Locality and distance.
- Skill level.
- Expected wage range and unit.
- Experience.
- Availability date.
- Group/team size.

**List / Map switch**
- Default to List.
- Map is an alternate view, not a separate navigation destination.
- Preserve filters while switching views.
- Map pins represent approximate areas, not exact residences.

**Worker card**
- First name or chosen display name.
- Skills and skill level.
- Experience.
- Expected wage + unit.
- Approximate distance / locality.
- Availability.
- Rating only when there are eligible completed bookings.
- View Profile and Invite actions.

## 5.9 Worker Profile detail

- Profile image optional.
- Display name.
- Verification indicator for phone verification only.
- Skill tags and skill level.
- Experience.
- Wage expectation and unit.
- Availability.
- Work preferences and travel radius.
- Completed booking review summary, if any.
- Invite / Offer action.

Do not display exact home address, personal phone number, or private identity documents publicly.

## 5.10 Job detail

- Job title and description.
- Hiring party display name and available trust signals.
- Locality and approximate distance.
- Number of workers needed.
- Skill level.
- Wage + unit.
- Start date and duration.
- Facilities.
- Apply action.
- Report action.

## 5.11 Messages

- Conversation list with participant, related job/requirement, last message, time, unread count.
- Chat screen with text messages and structured offer cards.
- Support wage proposal, counteroffer, accept, and decline actions.
- Keep booking terms visible in the conversation.
- Do not expose phone numbers automatically; contact sharing should be a deliberate action when allowed.

## 5.12 Booking and negotiation

Use a clear step sequence:

1. Initial interest / application.
2. Offer details.
3. Counteroffer (if needed).
4. Both parties accept the same final terms.
5. Booking confirmed.
6. Work started.
7. Work completed or cancelled with reason.
8. Mutual review after completion.

Always show:
- Wage and unit.
- Headcount.
- Date and duration.
- Work locality.
- Facilities and agreed conditions.

A booking must not become Confirmed until both sides accept the same final terms. Display a confirmation summary before the final action.

## 5.13 Profile and Settings

Shared profile:
- Name and photo.
- Verified phone status.
- Active roles.
- Language.
- Notification preferences.
- Privacy and safety.
- Help and support.
- Terms and privacy policy.
- Logout and account deletion request.

Worker-specific:
- Skills, experience, expected wage, availability, travel radius, work history.

Hiring-specific:
- Hiring display name / business name, locality, posted requirements, hiring history.

---

## 6. List and Map discovery rules

- List is the default because it is easier to read and works better on low-end devices.
- Map view is available through a clear List / Map segmented switch.
- Use approximate area-level coordinates for worker discovery.
- Never show a worker's home pin or exact home address.
- Ask for location permission only when the user opens a location-dependent feature.
- If permission is denied, provide manual locality search.
- Provide a location freshness label where relevant.
- Do not imply that a person is currently at a map pin; the pin is a search-area marker.

---

## 7. Localization

Languages in the first release:
- Hindi (`hi-IN`)
- English (`en-IN`)

Rules:
- All UI labels, validation, notifications, empty states, and system messages must be localized.
- Keep wage units explicit: `₹/दिन`, `₹/घंटा`, `₹/महीना`, `एकमुश्त`.
- Support mixed Hindi/English user-generated content.
- Do not translate names, phone numbers, or user-written job descriptions automatically.
- Layout must handle longer Hindi labels without truncation.
- Use a language selector in Profile → Settings.

---

## 8. States and feedback

Every data-driven screen must include:

- Loading state: restrained skeletons or progress indicator.
- Empty state: explain why the list is empty and give one useful next action.
- Error state: plain-language message and Retry.
- Offline state: persistent but non-blocking banner.
- Success feedback: clear confirmation after save, apply, offer, or publish.
- Permission-denied state: explain the feature and offer manual alternative.

Avoid blank white screens and technical error codes in user-facing UI.

---

## 9. Accessibility and usability

- Minimum 48dp touch targets.
- Large, readable text with system font scaling.
- Text labels alongside important icons.
- Strong contrast for text and controls.
- Do not communicate status using color alone; include text labels.
- Avoid complex gestures as the only way to perform an action.
- Use plain language and short sentences.
- Provide confirmation for destructive actions.
- Keep forms short and divide long forms into manageable sections.
- Support TalkBack content descriptions and logical focus order.

---

## 10. Safety and privacy UI

- Phone verification is not the same as identity or background verification; label it accurately.
- Exact home address and personal contact details remain private.
- Report and Block actions available from profiles and chats.
- Ratings are enabled only after an eligible completed booking.
- Booking terms require mutual acceptance.
- No public live tracking.
- No Aadhaar requirement for basic discovery.
- Provide clear cancellation and dispute pathways.
- Avoid badges that imply a worker is government-certified or background-checked unless the relevant verification has actually happened.

---

## 11. Notifications

Notification categories:
- New matching job.
- New application.
- Worker invitation.
- New message.
- Wage offer / counteroffer.
- Booking accepted / changed / cancelled.
- Work start and completion reminders.

Notifications should deep-link to the relevant job, profile, conversation, or booking. Users can control non-essential notification categories in Settings.

---

## 12. Android implementation guidance

Recommended UI implementation:
- Kotlin + Jetpack Compose + Material 3.
- Single-activity architecture.
- Navigation Compose.
- ViewModel per feature/screen flow.
- StateFlow for UI state.
- Repository pattern for data.
- Room for appropriate local caching and drafts.
- DataStore for preferences and selected language/role.
- Compose resources for localized strings and drawables.
- Adaptive layouts for compact and larger phones.

Suggested feature packages:

```text
app/
  core/
    design/
    localization/
    navigation/
    common/
  feature/
    onboarding/
    auth/
    home/
    jobs/
    post/
    workers/
    messages/
    booking/
    profile/
    settings/
```

Keep UI state explicit: Loading, Content, Empty, and Error. Do not put networking or business logic directly inside composables.

---

## 13. Screen acceptance checklist

A screen is ready when:

- [ ] Hindi and English layouts both work.
- [ ] Small Android screens do not clip important content.
- [ ] Loading, empty, offline, and error states exist.
- [ ] Primary actions are reachable and have clear labels.
- [ ] Back navigation behaves consistently.
- [ ] Accessibility labels and touch targets are present.
- [ ] Wage amount always has a visible unit.
- [ ] Private location/contact data is not exposed.
- [ ] Role-specific content is correct.
- [ ] UI state survives ordinary navigation and configuration changes.

---

## 14. MVP implementation order

1. Design tokens and reusable components.
2. Splash, language selection, OTP, onboarding.
3. Role-aware six-item navigation.
4. Worker and Hiring Home screens.
5. Jobs list and job detail.
6. Post availability / requirement forms.
7. Workers list, filters, and map/list switch.
8. Profile and settings.
9. Messages and structured offers.
10. Booking lifecycle, ratings, reports, and safety states.

**Implementation boundary:** This document finalizes the UI/UX specification. It does not claim that Android screens or backend functionality have already been implemented.
