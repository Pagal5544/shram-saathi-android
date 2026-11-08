package com.shramsaathi.app

import android.app.Activity
import android.content.Context
import android.os.Handler
import android.os.Looper
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Handshake
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.google.firebase.FirebaseApp
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.PhoneAuthOptions
import com.google.firebase.auth.PhoneAuthProvider
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.util.concurrent.TimeUnit

@Composable
fun AuthScreen(onLoginSuccess: () -> Unit) {
    val context = LocalContext.current
    val activity = context as? Activity
    var phone by remember { mutableStateOf("+91") }
    var otp by remember { mutableStateOf("") }
    var verificationId by remember { mutableStateOf<String?>(null) }
    var busy by remember { mutableStateOf(false) }
    var message by remember { mutableStateOf("अपने मोबाइल नंबर से शुरू करें।") }
    var isError by remember { mutableStateOf(false) }
    var firebaseReady by remember { mutableStateOf(false) }

    LaunchedEffect(Unit) {
        firebaseReady = try {
            if (FirebaseApp.getApps(context).isEmpty()) FirebaseApp.initializeApp(context)
            FirebaseApp.getApps(context).isNotEmpty()
        } catch (_: Exception) { false }
        if (!firebaseReady) {
            message = "Firebase सेटअप बाकी है: app/google-services.json जोड़ें।"
            isError = true
        } else if (BuildConfig.API_BASE_URL.isBlank()) {
            message = "Backend URL अभी configure नहीं है।"
            isError = true
        }
    }

    fun completeLogin(credential: com.google.firebase.auth.PhoneAuthCredential) {
        busy = true
        FirebaseAuth.getInstance().signInWithCredential(credential)
            .addOnCompleteListener { task ->
                if (!task.isSuccessful) {
                    busy = false
                    message = task.exception?.localizedMessage ?: "OTP सत्यापन विफल हुआ।"
                    isError = true
                    return@addOnCompleteListener
                }
                val user = task.result?.user
                if (user == null) {
                    busy = false
                    message = "Firebase user नहीं मिला।"
                    isError = true
                    return@addOnCompleteListener
                }
                user.getIdToken(false).addOnCompleteListener { tokenTask ->
                    val idToken = tokenTask.result?.token
                    if (!tokenTask.isSuccessful || idToken.isNullOrBlank()) {
                        busy = false
                        message = "Firebase token प्राप्त नहीं हुआ।"
                        isError = true
                    } else {
                        val apiBase = BuildConfig.API_BASE_URL.trimEnd('/')
                        Thread {
                            try {
                                val body = JSONObject().put("id_token", idToken)
                                    .toString().toRequestBody("application/json".toMediaType())
                                val request = Request.Builder()
                                    .url("$apiBase/api/v1/auth/firebase")
                                    .post(body)
                                    .build()
                                val response = OkHttpClient().newCall(request).execute()
                                val responseText = response.body?.string().orEmpty()
                                if (!response.isSuccessful) {
                                    val detail = try { JSONObject(responseText).optString("detail") } catch (_: Exception) { "" }
                                    throw IllegalStateException(detail.ifBlank { "Backend login failed (\${response.code})" })
                                }
                                val session = JSONObject(responseText)
                                val token = session.getString("access_token")
                                val userId = session.getString("user_id")
                                val expiresIn = session.optLong("expires_in", 1800L)
                                context.getSharedPreferences("shram_auth", Context.MODE_PRIVATE)
                                    .edit()
                                    .putString("access_token", token)
                                    .putString("user_id", userId)
                                    .putLong("expires_at", System.currentTimeMillis() + expiresIn * 1000L)
                                    .apply()
                                Handler(Looper.getMainLooper()).post {
                                    busy = false
                                    message = "लॉगिन सफल।"
                                    isError = false
                                    onLoginSuccess()
                                }
                            } catch (error: Exception) {
                                Handler(Looper.getMainLooper()).post {
                                    busy = false
                                    message = error.localizedMessage ?: "Server से संपर्क नहीं हो पाया।"
                                    isError = true
                                }
                            }
                        }.start()
                    }
                }
            }
    }

    fun sendOtp() {
        val normalized = phone.trim().replace(" ", "")
        if (!normalized.matches(Regex("^\\+[1-9][0-9]{7,14}$"))) {
            message = "देश कोड सहित सही मोबाइल नंबर लिखें, जैसे +919876543210।"
            isError = true
            return
        }
        val currentActivity = activity
        if (!firebaseReady || currentActivity == null) {
            message = "Firebase configuration या Activity उपलब्ध नहीं है।"
            isError = true
            return
        }
        busy = true
        val callbacks = object : PhoneAuthProvider.OnVerificationStateChangedCallbacks() {
            override fun onVerificationCompleted(credential: com.google.firebase.auth.PhoneAuthCredential) {
                completeLogin(credential)
            }

            override fun onVerificationFailed(error: com.google.firebase.FirebaseException) {
                busy = false
                message = error.localizedMessage ?: "OTP भेजना विफल हुआ।"
                isError = true
            }

            override fun onCodeSent(
                id: String,
                token: PhoneAuthProvider.ForceResendingToken
            ) {
                verificationId = id
                busy = false
                message = "OTP भेज दिया गया है। SMS में आया 6 अंकों का कोड भरें।"
                isError = false
            }
        }
        val options = PhoneAuthOptions.newBuilder(FirebaseAuth.getInstance())
            .setPhoneNumber(normalized)
            .setTimeout(60L, TimeUnit.SECONDS)
            .setActivity(currentActivity)
            .setCallbacks(callbacks)
            .build()
        PhoneAuthProvider.verifyPhoneNumber(options)
    }

    Surface(Modifier.fillMaxSize(), color = Color(0xFFF7F8F5)) {
        Column(
            Modifier.fillMaxSize().padding(horizontal = 24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Surface(color = Color(0xFF146B45), shape = RoundedCornerShape(20.dp), modifier = Modifier.size(72.dp)) {
                Box(contentAlignment = Alignment.Center) {
                    Icon(Icons.Default.Handshake, contentDescription = null, tint = Color.White, modifier = Modifier.size(38.dp))
                }
            }
            Spacer(Modifier.height(16.dp))
            Text("Shram Saathi", color = Color(0xFF146B45), fontSize = 26.sp, fontWeight = FontWeight.Bold)
            Text("काम और कामगार — एक भरोसेमंद जगह", color = Color(0xFF737B76), fontSize = 13.sp)
            Spacer(Modifier.height(30.dp))
            Card(colors = CardDefaults.cardColors(containerColor = Color.White), shape = RoundedCornerShape(22.dp)) {
                Column(Modifier.fillMaxWidth().padding(20.dp)) {
                    Text("मोबाइल नंबर से लॉगिन", fontSize = 19.sp, fontWeight = FontWeight.Bold, color = Color(0xFF252B28))
                    Spacer(Modifier.height(6.dp))
                    Text("हम आपके नंबर पर OTP भेजेंगे।", color = Color(0xFF737B76), fontSize = 12.sp)
                    Spacer(Modifier.height(18.dp))
                    OutlinedTextField(
                        value = phone,
                        onValueChange = { phone = it.filter { ch -> ch.isDigit() || ch == '+' }.take(16) },
                        label = { Text("मोबाइल नंबर (+91...)") },
                        modifier = Modifier.fillMaxWidth(),
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Phone),
                        singleLine = true,
                        shape = RoundedCornerShape(12.dp)
                    )
                    if (verificationId != null) {
                        Spacer(Modifier.height(12.dp))
                        OutlinedTextField(
                            value = otp,
                            onValueChange = { otp = it.filter(Char::isDigit).take(6) },
                            label = { Text("6 अंकों का OTP") },
                            modifier = Modifier.fillMaxWidth(),
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.NumberPassword),
                            singleLine = true,
                            shape = RoundedCornerShape(12.dp)
                        )
                    }
                    Spacer(Modifier.height(16.dp))
                    Button(
                        onClick = {
                            if (verificationId == null) sendOtp()
                            else {
                                val id = verificationId
                                if (id != null && otp.length == 6) {
                                    busy = true
                                    completeLogin(PhoneAuthProvider.getCredential(id, otp))
                                } else {
                                    message = "6 अंकों का OTP भरें।"
                                    isError = true
                                }
                            }
                        },
                        enabled = !busy && firebaseReady && BuildConfig.API_BASE_URL.isNotBlank() &&
                            (verificationId == null || otp.length == 6),
                        modifier = Modifier.fillMaxWidth().height(50.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF146B45))
                    ) {
                        if (busy) CircularProgressIndicator(modifier = Modifier.size(20.dp), color = Color.White, strokeWidth = 2.dp)
                        else Text(if (verificationId == null) "OTP भेजें" else "सत्यापित करें और लॉगिन करें", fontWeight = FontWeight.Bold)
                    }
                    if (verificationId != null) {
                        TextButton(
                            onClick = { sendOtp() },
                            enabled = !busy,
                            modifier = Modifier.align(Alignment.CenterHorizontally)
                        ) { Text("OTP दोबारा भेजें", color = Color(0xFF146B45)) }
                    }
                    Spacer(Modifier.height(10.dp))
                    Text(
                        message,
                        color = if (isError) MaterialTheme.colorScheme.error else Color(0xFF146B45),
                        fontSize = 12.sp
                    )
                }
            }
            Spacer(Modifier.height(18.dp))
            Text("जारी रखकर आप OTP आधारित मोबाइल सत्यापन स्वीकार करते हैं।", color = Color(0xFF737B76), fontSize = 11.sp)
        }
    }
}
