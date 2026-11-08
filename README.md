# Shram Saathi Android

Android-first two-way local labour marketplace connecting workers with contractors and customers.

## Android prototype v0.1.0

This repository includes a native Kotlin + Jetpack Compose prototype.

### Included in this first UI build
- Worker / Hiring role switch
- Hindi / English UI text switch
- Six-tab navigation: Home, Jobs, Post, Workers, Messages, Profile
- Worker availability card
- Nearby job cards and worker discovery list
- Demo job/availability posting form
- Profile, inbox and basic marketplace sample data
- Shram Saathi green and orange visual identity

> This is a UI prototype. Authentication, backend APIs, database persistence, real maps, live chat, notifications and real applications/bookings are not connected yet. Sample profiles and jobs are demonstration data only.

## Build

Requirements:
- Android Studio with Android SDK 35
- JDK 17
- Gradle 8.9 (or use Android Studio's Gradle sync)

Open this repository in Android Studio and run the `app` configuration, or from the project root run:

```bash
gradle assembleDebug
```

APK output:

```
app/build/outputs/apk/debug/app-debug.apk
```

## Package

`in.shramsaathi.app`

## Product and UI documentation

- [Product blueprint](BLUEPRINT.md)
- [UI/UX design specification](docs/UI_UX_DESIGN.md)
