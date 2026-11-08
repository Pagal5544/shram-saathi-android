# Authentication and profile registration milestone

This milestone uses Firebase Phone Authentication for phone-number proof, while the API issues its own short-lived bearer access token. The backend never receives or verifies an SMS OTP itself.

## Flow

1. Android Firebase Authentication sends the SMS and verifies the OTP.
2. Android obtains a Firebase ID token after successful phone sign-in.
3. Android sends that token to `POST /api/v1/auth/firebase`.
4. The API verifies the Firebase token and independently checks that the Firebase user has a verified phone number.
5. The API creates or loads the local user and returns a short-lived API access token.
6. Android sends `Authorization: Bearer <access_token>` to protected profile endpoints.

## Configuration

Add these values to the backend environment (never commit real values):

- `FIREBASE_SERVICE_ACCOUNT_JSON`: complete Firebase service-account JSON as a single-line JSON string.
- `JWT_SECRET_KEY`: cryptographically random secret of at least 32 characters.
- `ACCESS_TOKEN_MINUTES`: short-lived access-token lifetime (default 30 minutes).

The Firebase project must have Phone Authentication enabled. Add the Android app's SHA-1/SHA-256 fingerprints in Firebase Console and configure the Firebase Android app with its generated `google-services.json`. Firebase phone sign-in sends real SMS and may be subject to Firebase quotas, regional availability, and billing policies. Do not assume SMS is unlimited or always free.

## Endpoints

- `POST /api/v1/auth/firebase` — exchange a Firebase ID token for a Shram Saathi API token.
- `POST /api/v1/profiles/worker` — create/update the authenticated user's worker profile and selected skills.
- `POST /api/v1/profiles/employer` — create/update the authenticated user's hiring profile.

A single user may register both profiles; roles are additive. Public APIs must continue to expose approximate location only.

## Safety notes

- The API accepts Firebase ID tokens only for identity exchange; it does not accept client-supplied phone numbers as proof.
- Local API tokens are signed with a separate backend secret and expire.
- Firebase service-account credentials and JWT signing keys belong in deployment secrets, never source control.
- Rate limiting, refresh-token rotation/revocation, device/session management, abuse controls and a security review are still required before public launch.
- The Android client integration and live Firebase project configuration are not included in this backend-only milestone.
