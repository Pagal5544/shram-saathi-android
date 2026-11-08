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

The v0.1.0 baseline is preserved as a reference. Future development should continue on `main` or a new development branch; do not make feature changes directly to the locked release snapshot.

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

> **Marketplace prototype limitation:** Jobs, worker discovery, posting, chat, maps and bookings still use demo data. A separate feature branch now adds Firebase phone OTP sign-in and the backend token exchange; see [Android Firebase Auth setup](docs/ANDROID_FIREBASE_AUTH.md).

## Build

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

The GitHub Actions workflow builds the debug APK and uploads it as the `shram-saathi-debug-apk` artifact.

## Package

`com.shramsaathi.app`

## Product and UI documentation

- [Product blueprint](BLUEPRINT.md)
- [UI/UX design specification](docs/UI_UX_DESIGN.md)

## Versioning policy

- `v0.1.0` is the locked UI prototype baseline.
- New features and fixes should be developed on `main` or feature branches.
- Update this README and create a new versioned snapshot when a future baseline is approved.
