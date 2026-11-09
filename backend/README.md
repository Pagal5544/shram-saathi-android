# Shram Saathi API

Node.js API for exchanging a verified Firebase Phone Authentication ID token for a Shram Saathi API access token.

## Endpoints

- `GET /` — service information
- `GET /health` — hosting health check
- `POST /api/v1/auth/firebase` — Firebase ID token exchange

The auth endpoint accepts the Firebase ID token in either:
- `Authorization: Bearer <firebase-id-token>`
- JSON body: `{"idToken":"<firebase-id-token>"}` or `{"firebaseIdToken":"<firebase-id-token>"}`

A successful response includes `accessToken`, `token`, `tokenType`, `expiresIn`, `expiresAt`, and a user object. The access token is an HS256 JWT with a one-hour expiry.

## Required environment variables

- `FIREBASE_PROJECT_ID`: `shram-saathi-7e9a0`
- `FIREBASE_SERVICE_ACCOUNT_JSON`: complete Firebase Admin service-account JSON. Create it in Firebase Console > Project settings > Service accounts. Keep it secret; never commit it.
- `SHRAM_JWT_SECRET`: random secret of at least 32 characters. Hosting can generate this.
- `PORT`: supplied by hosting platform (defaults to 8080).
- `CORS_ORIGIN`: optional comma-separated allowed browser origins. Native Android clients do not require browser CORS.

## Deploy on Render

1. Create a new **Blueprint** in Render and connect this repository.
2. Select the `feature/android-firebase-auth` branch and the `backend/render.yaml` blueprint path (or create a Web Service with root directory `backend`).
3. Set `FIREBASE_SERVICE_ACCOUNT_JSON` to the complete service-account JSON in Render's secret environment field.
4. Keep the generated `SHRAM_JWT_SECRET`; deploy the service.
5. Confirm `https://YOUR-SERVICE.onrender.com/health` returns `{"status":"healthy","service":"shram-saathi-api"}`.

## Android configuration

After deployment, configure the Android build property `SHRAM_API_BASE_URL` to the deployed HTTPS origin (without a trailing slash), for example:

```bash
gradle assembleDebug -PSHRAM_API_BASE_URL=https://YOUR-SERVICE.onrender.com
```

For GitHub Actions, store the same origin in repository Actions secret `SHRAM_API_BASE_URL`. Do not put service-account credentials in the Android app or repository.

## Security notes

Firebase Admin verifies token signature, issuer, audience, expiry and revocation. The API only issues a Shram Saathi token when Firebase confirms a verified phone number. Authentication attempts are rate-limited. This initial API does not yet persist user profiles or implement refresh-token rotation, logout revocation, marketplace data, jobs, chat, or payments.
