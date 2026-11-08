# Shram Saathi Android

Android-first two-way local labour marketplace connecting workers with contractors and customers.

<details>
<summary><strong>Release status: v0.1.0 — UI prototype baseline locked</strong></summary>

- Status: **Frozen baseline / reference build**
- Android package: `com.shramsaathi.app`
- Baseline source commit: `5d19ec153542d55a4832582899430721232dbdb2`
- Verified GitHub Actions run: [#42490089853](https://github.com/Pagal5544/shram-saathi-android/actions/runs/42490089853)
- Build result: **Success**
- Artifact: `shram-saathi-debug-apk`
- Artifact ID: `13621108328`
- Build type: Debug APK (not a Play Store release)

The v0.1.0 baseline is preserved as a reference. Backend development is being carried out separately and does not alter the locked Android UI baseline.

</details>

## Android prototype v0.1.0

This repository includes a native Kotlin + Jetpack Compose prototype.

### Included in this UI build
- Worker / Hiring role switch
- Hindi / English UI text switch
- Six-tab navigation: Home, Jobs, Post, Workers, Messages, Profile
- Worker availability card
- Nearby job cards and worker discovery list
- Demo job/availability posting form
- Profile, inbox and basic marketplace sample data
- Shram Saathi green and orange visual identity

> **Prototype limitation:** The Android UI is not yet connected to live authentication, backend APIs, database persistence, maps, chat, notifications or real applications/bookings. Sample profiles and jobs are demonstration data only.

## Backend foundation

The first FastAPI + PostgreSQL/PostGIS backend scaffold is available on the development branch:

- [Backend source — backend/foundation](https://github.com/Pagal5544/shram-saathi-android/tree/backend/foundation/backend)
- [Backend setup and API notes](https://github.com/Pagal5544/shram-saathi-android/blob/backend/foundation/backend/README.md)
- [Backend CI workflow](https://github.com/Pagal5544/shram-saathi-android/blob/backend/foundation/.github/workflows/backend-ci.yml)

**Status:** Foundation scaffold only. It includes the API service, database configuration, initial marketplace models and health checks. OTP authentication, authorization, API CRUD, migrations, matching, offers, bookings and production deployment are still pending. Do not expose it publicly as a production service.

## Android build

Requirements:
- Android SDK 35
- JDK 17
- Gradle 8.9

From the project root:

```bash
gradle assembleDebug
```

APK output:

```
app/build/outputs/apk/debug/app-debug.apk
```

The Android GitHub Actions workflow builds the debug APK and uploads it as the `shram-saathi-debug-apk` artifact.

## Package

`com.shramsaathi.app`

## Product and UI documentation

- [Product blueprint](BLUEPRINT.md)
- [UI/UX design specification](docs/UI_UX_DESIGN.md)

## Versioning policy

- `v0.1.0` is the locked UI prototype baseline.
- Backend development is isolated on `backend/foundation` until the foundation is reviewed.
- New Android features should be developed on `main` or feature branches.
- Update the README and create a new versioned snapshot when a future baseline is approved.
