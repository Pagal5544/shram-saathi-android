# Android Firebase Phone OTP setup

The Android client now includes a Hindi-first phone number and OTP login screen. After Firebase Phone Authentication succeeds, the app obtains a Firebase ID token and exchanges it with the backend at `POST /api/v1/auth/firebase`. The returned Shram Saathi bearer token is stored locally with its expiry time.

## One-time Firebase Console setup

1. Create or select the Firebase project for Shram Saathi.
2. Add an Android app with package name `com.shramsaathi.app`.
3. Register the app's SHA-1 and SHA-256 signing certificate fingerprints in Firebase project settings. Add release fingerprints before Play Store distribution.
4. In Authentication -> Sign-in method, enable **Phone**.
5. Download `google-services.json` and place it at `app/google-services.json`. This file is intentionally not committed.
6. Configure allowed SMS regions and review Firebase phone-authentication quotas/pricing for the intended region.

For GitHub Actions builds, add repository Actions secrets named `GOOGLE_SERVICES_JSON` (the complete JSON file contents) and `SHRAM_API_BASE_URL` (the HTTPS backend base URL). The workflow injects the JSON only during the build; it is not committed to Git.

## Configure the backend URL

Set the Gradle project property `SHRAM_API_BASE_URL` to the HTTPS base URL of the deployed Shram Saathi API. For both emulator and physical-device testing, use a reachable HTTPS API URL (for example, a temporary HTTPS tunnel to a local development server). Production must always use HTTPS.

Example local invocation:

```bash
gradle assembleDebug -PSHRAM_API_BASE_URL=https://your-https-api-host
```

The app keeps login disabled if Firebase configuration or the API base URL is missing.

## Current limits

- The backend must already be deployed and reachable; this commit does not provision hosting.
- Firebase SMS can be quota-limited or billable depending on region and usage.
- The app stores the short-lived API access token and expiry in private app preferences. Refresh-token rotation and session revocation are not implemented yet.
- Marketplace data and posting screens remain prototype data and are not yet wired to the backend.
