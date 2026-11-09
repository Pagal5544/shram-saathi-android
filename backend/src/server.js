const express = require("express");
const cors = require("cors");
const helmet = require("helmet");
const rateLimit = require("express-rate-limit");
const admin = require("firebase-admin");
const jwt = require("jsonwebtoken");

const app = express();
const PORT = Number(process.env.PORT || 8080);
const PROJECT_ID = process.env.FIREBASE_PROJECT_ID || "shram-saathi-7e9a0";
const JWT_SECRET = process.env.SHRAM_JWT_SECRET;

if (!JWT_SECRET || JWT_SECRET.length < 32) {
  throw new Error("SHRAM_JWT_SECRET is required and must be at least 32 characters");
}

if (!admin.apps.length) {
  const raw = process.env.FIREBASE_SERVICE_ACCOUNT_JSON;
  if (!raw) throw new Error("FIREBASE_SERVICE_ACCOUNT_JSON is required");
  let serviceAccount;
  try { serviceAccount = JSON.parse(raw); }
  catch { throw new Error("FIREBASE_SERVICE_ACCOUNT_JSON must contain valid JSON"); }
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    projectId: PROJECT_ID
  });
}

app.disable("x-powered-by");
app.use(helmet());
app.use(cors({
  origin: process.env.CORS_ORIGIN ? process.env.CORS_ORIGIN.split(",").map(v => v.trim()) : false,
  methods: ["GET", "POST", "OPTIONS"],
  allowedHeaders: ["Content-Type", "Authorization"]
}));
app.use(express.json({ limit: "32kb" }));

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  limit: 30,
  standardHeaders: "draft-7",
  legacyHeaders: false,
  message: { error: "Too many authentication attempts. Please try again later." }
});

app.get("/", (_req, res) => res.json({
  name: "Shram Saathi API",
  status: "ok",
  version: "1.0.0"
}));

app.get("/health", (_req, res) => res.status(200).json({
  status: "healthy",
  service: "shram-saathi-api"
}));

function getFirebaseIdToken(req) {
  const auth = req.get("authorization") || "";
  const match = auth.match(/^Bearer\s+(.+)$/i);
  return match?.[1] || req.body?.firebaseIdToken || req.body?.idToken || null;
}

app.post("/api/v1/auth/firebase", authLimiter, async (req, res) => {
  try {
    const idToken = getFirebaseIdToken(req);
    if (!idToken || typeof idToken !== "string" || idToken.length > 12000) {
      return res.status(400).json({ error: "FIREBASE_ID_TOKEN_REQUIRED", message: "Firebase ID token is required." });
    }

    const decoded = await admin.auth().verifyIdToken(idToken, true);
    if (decoded.aud !== PROJECT_ID || decoded.iss !== `https://securetoken.google.com/${PROJECT_ID}`) {
      return res.status(401).json({ error: "INVALID_FIREBASE_PROJECT", message: "Token was not issued for this Firebase project." });
    }
    if (!decoded.phone_number) {
      return res.status(403).json({ error: "PHONE_NUMBER_REQUIRED", message: "A verified phone number is required." });
    }

    const now = Math.floor(Date.now() / 1000);
    const expiresIn = 60 * 60;
    const accessToken = jwt.sign({
      sub: decoded.uid,
      phone: decoded.phone_number,
      firebaseUid: decoded.uid,
      iss: "shram-saathi-api",
      aud: "shram-saathi-app"
    }, JWT_SECRET, { algorithm: "HS256", expiresIn });

    const user = {
      id: decoded.uid,
      uid: decoded.uid,
      phoneNumber: decoded.phone_number,
      phone_number: decoded.phone_number,
      name: decoded.name || null,
      role: "user"
    };

    return res.status(200).json({
      accessToken,
      token: accessToken,
      tokenType: "Bearer",
      token_type: "Bearer",
      expiresIn,
      expires_in: expiresIn,
      expiresAt: new Date((now + expiresIn) * 1000).toISOString(),
      expires_at: new Date((now + expiresIn) * 1000).toISOString(),
      user
    });
  } catch (error) {
    const code = error?.code || "";
    if (code.startsWith("auth/")) {
      return res.status(401).json({ error: "INVALID_FIREBASE_ID_TOKEN", message: "Firebase session is invalid or expired." });
    }
    console.error("Firebase auth exchange failed:", error);
    return res.status(500).json({ error: "AUTH_EXCHANGE_FAILED", message: "Unable to complete sign-in." });
  }
});

app.use((err, _req, res, _next) => {
  if (err instanceof SyntaxError && "body" in err) {
    return res.status(400).json({ error: "INVALID_JSON", message: "Request body must be valid JSON." });
  }
  console.error("Unhandled API error:", err);
  return res.status(500).json({ error: "INTERNAL_SERVER_ERROR" });
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Shram Saathi API listening on port ${PORT}`);
});