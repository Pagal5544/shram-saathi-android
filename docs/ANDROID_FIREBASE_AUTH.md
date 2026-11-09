# Android Firebase Phone OTP setup

The Android client now includes a Hindi-first phone number and OTP login screen. After Firebase Phone Authentication succeeds, the app obtains a Firebase ID token and exchanges it with the backend at `POST /api/v1/auth/firebase`. The returned Shram Saathi bearer token is stored locally with its expiry time.

## One-time Firebase Console setup

1. Create or select the Firebase project for Shram Saathi.
2. Add an Android app with package name `com.shramsaathi.app`.
3. Register the app's SHA-1 and SHA-256 signing certificate fingerprints in Firebase project settings. Add release fingerprints before Play Store distribution.
4. In Authentication -> Sign-in method, enable **Phone**.
5. The Android app's `google-services.json` is stored at `app/google-services.json` on this feature branch. It contains Firebase client configuration, not a Firebase Admin private key. Never add a service-account JSON file to the Android app or repository.
6. Configure allowed SMS regions and review Firebase phone-authentication quotas/pricing for the intended region.

For GitHub Actions builds, configure the repository Actions secret `SHRAM_API_BASE_URL` with the deployed HTTPS API origin. Firebase Admin credentials belong only in the backend host's secret environment settings.

## Backend implementation and deployment\n\nThe API source is in [`backend/`](../backend/README.md). It verifies Firebase ID tokens with Firebase Admin and issues a short-lived Shram Saathi access token. Deploy it using the Render blueprint at `backend/render.yaml`, then set the required `FIREBASE_SERVICE_ACCOUNT_JSON` and `SHRAM_JWT_SECRET` environment variables in the hosting dashboard. The service-account JSON must remain private.\n\n## Configure the backend URL

Set the Gradle project property `SHRAM_API_BASE_URL` to the HTTPS base URL of the deployed Shram Saathi API. For both emulator and physical-device testing, use a reachable HTTPS API URL (for example, a temporary HTTPS tunnel to a local development server). Production must always use HTTPS.

Example local invocation:

```bash
gradle assembleDebug -PSHRAM_API_BASE_URL=https://your-https-api-host
```

The app keeps login disabled if Firebase configuration or the API base URL is missing.

## Current limits

- Backend source and a Render deployment blueprint are included. A live URL is available only after the hosting service is created and its Firebase Admin credentials are configured.
- Firebase SMS can be quota-limited or billable depending on region and usage.
- The app stores the short-lived API access token and expiry in private app preferences. Refresh-token rotation and session revocation are not implemented yet.
- Marketplace data and posting screens remain prototype data and are not yet wired to the backend.
