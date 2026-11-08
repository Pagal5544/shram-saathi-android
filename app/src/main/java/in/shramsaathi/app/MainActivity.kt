package com.shramsaathi.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

private val Green = Color(0xFF146B45)
private val LightGreen = Color(0xFFE9F5ED)
private val Orange = Color(0xFFF4A62A)
private val Canvas = Color(0xFFF7F8F5)
private val Ink = Color(0xFF252B28)
private val Muted = Color(0xFF737B76)

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { ShramSaathiTheme { ShramSaathiApp() } }
    }
}

@Composable
private fun ShramSaathiTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = lightColorScheme(
            primary = Green,
            onPrimary = Color.White,
            secondary = Orange,
            background = Canvas,
            surface = Color.White,
            onSurface = Ink,
            onBackground = Ink
        ),
        content = content
    )
}

private enum class AppTab { HOME, JOBS, POST, WORKERS, MESSAGES, PROFILE }
private enum class UserRole { WORKER, HIRING }

@Composable
private fun ShramSaathiApp() {
    var tab by remember { mutableStateOf(AppTab.HOME) }
    var role by remember { mutableStateOf(UserRole.WORKER) }
    var hindi by remember { mutableStateOf(true) }
    var search by remember { mutableStateOf("") }
    var available by remember { mutableStateOf(true) }

    val title = when (tab) {
        AppTab.HOME -> if (role == UserRole.WORKER) "नमस्ते, रामू जी" else "नमस्ते, ठेकेदार जी"
        AppTab.JOBS -> tr("काम खोजें", "Find jobs", hindi)
        AppTab.POST -> tr("नई पोस्ट", "Create post", hindi)
        AppTab.WORKERS -> tr("मज़दूर खोजें", "Find workers", hindi)
        AppTab.MESSAGES -> tr("संदेश", "Messages", hindi)
        AppTab.PROFILE -> tr("मेरी प्रोफ़ाइल", "My profile", hindi)
    }

    Scaffold(
        containerColor = Canvas,
        topBar = {
            Column(Modifier.background(Color.White)) {
                Row(
                    Modifier.fillMaxWidth().padding(horizontal = 18.dp, vertical = 12.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Surface(color = Green, shape = RoundedCornerShape(12.dp), modifier = Modifier.size(42.dp)) {
                        Box(contentAlignment = Alignment.Center) {
                            Icon(Icons.Default.Handshake, contentDescription = null, tint = Color.White)
                        }
                    }
                    Spacer(Modifier.width(10.dp))
                    Column(Modifier.weight(1f)) {
                        Text("Shram Saathi", fontWeight = FontWeight.Bold, fontSize = 18.sp, color = Green)
                        Text(title, fontSize = 12.sp, color = Muted)
                    }
                    TextButton(onClick = { hindi = !hindi }) {
                        Text(if (hindi) "हिंदी" else "EN", color = Green, fontWeight = FontWeight.Bold)
                    }
                    IconButton(onClick = { tab = AppTab.MESSAGES }) {
                        Icon(Icons.Default.NotificationsNone, contentDescription = "Notifications", tint = Ink)
                    }
                }
                Row(
                    Modifier.fillMaxWidth().padding(start = 18.dp, end = 18.dp, bottom = 12.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    RolePill(
                        selected = role == UserRole.WORKER,
                        text = tr("कामगार", "Worker", hindi),
                        modifier = Modifier.weight(1f)
                    ) { role = UserRole.WORKER; tab = AppTab.HOME }
                    Spacer(Modifier.width(8.dp))
                    RolePill(
                        selected = role == UserRole.HIRING,
                        text = tr("काम देने वाले", "Hiring", hindi),
                        modifier = Modifier.weight(1f)
                    ) { role = UserRole.HIRING; tab = AppTab.HOME }
                }
            }
        },
        bottomBar = {
            NavigationBar(containerColor = Color.White, tonalElevation = 8.dp) {
                val navItems = listOf(
                    Triple(AppTab.HOME, Icons.Default.Home, tr("होम", "Home", hindi)),
                    Triple(AppTab.JOBS, Icons.Default.WorkOutline, tr("काम", "Jobs", hindi)),
                    Triple(AppTab.POST, Icons.Default.AddCircle, tr("पोस्ट", "Post", hindi)),
                    Triple(AppTab.WORKERS, Icons.Default.Groups, tr("लोग", "Workers", hindi)),
                    Triple(AppTab.MESSAGES, Icons.Default.ChatBubbleOutline, tr("चैट", "Messages", hindi)),
                    Triple(AppTab.PROFILE, Icons.Default.PersonOutline, tr("प्रोफ़ाइल", "Profile", hindi))
                )
                navItems.forEach { (destination, icon, label) ->
                    NavigationBarItem(
                        selected = tab == destination,
                        onClick = { tab = destination },
                        icon = { Icon(icon, contentDescription = label) },
                        label = { Text(label, fontSize = 9.sp, maxLines = 1) },
                        colors = NavigationBarItemDefaults.colors(
                            selectedIconColor = Green,
                            selectedTextColor = Green,
                            indicatorColor = LightGreen,
                            unselectedIconColor = Muted
                        )
                    )
                }
            }
        }
    ) { padding ->
        Box(Modifier.fillMaxSize().padding(padding)) {
            when (tab) {
                AppTab.HOME -> HomeScreen(role, hindi, available) { available = it }
                AppTab.JOBS -> JobsScreen(hindi, search) { search = it }
                AppTab.POST -> PostScreen(role, hindi)
                AppTab.WORKERS -> WorkersScreen(hindi, search) { search = it }
                AppTab.MESSAGES -> MessagesScreen(hindi)
                AppTab.PROFILE -> ProfileScreen(role, hindi, available)
            }
        }
    }
}

@Composable
private fun RolePill(selected: Boolean, text: String, modifier: Modifier = Modifier, onClick: () -> Unit) {
    Surface(
        modifier = modifier.height(38.dp).clickable(onClick = onClick),
        color = if (selected) Green else Canvas,
        shape = RoundedCornerShape(10.dp),
        border = if (selected) null else androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFE3E8E3))
    ) {
        Box(contentAlignment = Alignment.Center) {
            Text(text, color = if (selected) Color.White else Ink, fontWeight = FontWeight.SemiBold, fontSize = 13.sp)
        }
    }
}

@Composable
private fun HomeScreen(role: UserRole, hindi: Boolean, available: Boolean, onAvailability: (Boolean) -> Unit) {
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        item {
            if (role == UserRole.WORKER) {
                AvailabilityCard(hindi, available, onAvailability)
            } else {
                HiringHero(hindi)
            }
        }
        item {
            SectionHeading(
                tr("आपके लिए", "For you", hindi),
                tr("आपकी लोकेशन के आसपास", "Around your location", hindi)
            )
        }
        item {
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                StatCard("12", tr("नए काम", "New jobs", hindi), Icons.Default.Work, Modifier.weight(1f))
                StatCard("4.8 ★", tr("रेटिंग", "Rating", hindi), Icons.Default.Star, Modifier.weight(1f))
                StatCard("3 km", tr("दूरी", "Nearby", hindi), Icons.Default.LocationOn, Modifier.weight(1f))
            }
        }
        item { SectionHeading(tr("नज़दीकी काम", "Nearby jobs", hindi), tr("सभी देखें", "View all", hindi)) }
        items(sampleJobs.take(3)) { JobCard(it, hindi) }
        item {
            Surface(color = LightGreen, shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxWidth()) {
                Row(Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.VerifiedUser, contentDescription = null, tint = Green, modifier = Modifier.size(30.dp))
                    Spacer(Modifier.width(12.dp))
                    Column {
                        Text(tr("अपनी प्रोफ़ाइल पूरी करें", "Complete your profile", hindi), fontWeight = FontWeight.Bold, color = Green)
                        Text(tr("अधिक काम और बेहतर अवसर पाएँ", "Get more work opportunities", hindi), fontSize = 12.sp, color = Muted)
                    }
                }
            }
        }
    }
}

@Composable
private fun AvailabilityCard(hindi: Boolean, available: Boolean, onChange: (Boolean) -> Unit) {
    Surface(color = Green, shape = RoundedCornerShape(20.dp), modifier = Modifier.fillMaxWidth()) {
        Column(Modifier.padding(18.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Column(Modifier.weight(1f)) {
                    Text(tr("आज काम के लिए उपलब्ध हैं?", "Available for work today?", hindi), color = Color.White, fontWeight = FontWeight.Bold, fontSize = 17.sp)
                    Text(tr("ठेकेदार आपको खोज पाएँगे", "Hiring users can find you", hindi), color = Color.White.copy(alpha = .8f), fontSize = 12.sp)
                }
                Switch(checked = available, onCheckedChange = onChange, colors = SwitchDefaults.colors(checkedThumbColor = Green, checkedTrackColor = Color.White))
            }
            Spacer(Modifier.height(12.dp))
            Surface(color = Color.White.copy(alpha = .14f), shape = RoundedCornerShape(10.dp)) {
                Text(
                    if (available) tr("●  आप उपलब्ध हैं", "●  You are available", hindi) else tr("○  अभी उपलब्ध नहीं", "○  Not available now", hindi),
                    color = Color.White, modifier = Modifier.padding(horizontal = 12.dp, vertical = 8.dp), fontSize = 13.sp
                )
            }
        }
    }
}

@Composable
private fun HiringHero(hindi: Boolean) {
    Surface(color = Green, shape = RoundedCornerShape(20.dp), modifier = Modifier.fillMaxWidth()) {
        Column(Modifier.padding(18.dp)) {
            Text(tr("आज कितने लोगों की ज़रूरत है?", "How many workers do you need?", hindi), color = Color.White, fontWeight = FontWeight.Bold, fontSize = 18.sp)
            Text(tr("अपने आसपास भरोसेमंद कामगार खोजें", "Find reliable workers near your site", hindi), color = Color.White.copy(alpha = .82f), fontSize = 13.sp)
            Spacer(Modifier.height(14.dp))
            Button(onClick = {}, colors = ButtonDefaults.buttonColors(containerColor = Orange, contentColor = Ink)) {
                Text(tr("काम की ज़रूरत पोस्ट करें", "Post a requirement", hindi), fontWeight = FontWeight.Bold)
                Spacer(Modifier.width(6.dp))
                Icon(Icons.Default.ArrowForward, contentDescription = null)
            }
        }
    }
}

@Composable
private fun StatCard(value: String, label: String, icon: androidx.compose.ui.graphics.vector.ImageVector, modifier: Modifier = Modifier) {
    Card(modifier = modifier, colors = CardDefaults.cardColors(containerColor = Color.White), shape = RoundedCornerShape(14.dp)) {
        Column(Modifier.padding(12.dp)) {
            Icon(icon, contentDescription = null, tint = Green, modifier = Modifier.size(20.dp))
            Spacer(Modifier.height(8.dp))
            Text(value, fontWeight = FontWeight.Bold, fontSize = 17.sp, color = Ink)
            Text(label, fontSize = 10.sp, color = Muted, maxLines = 1)
        }
    }
}

@Composable
private fun SectionHeading(title: String, action: String) {
    Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
        Text(title, fontWeight = FontWeight.Bold, fontSize = 16.sp, color = Ink, modifier = Modifier.weight(1f))
        Text(action, color = Green, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
    }
}

private data class Job(val title: String, val company: String, val wage: String, val distance: String, val duration: String, val people: String)

private val sampleJobs = listOf(
    Job("राजमिस्त्री", "शर्मा कंस्ट्रक्शन", "₹700 / दिन", "2.1 km", "15 दिन", "3 लोग"),
    Job("हेल्पर", "अग्रवाल बिल्डर्स", "₹450 / दिन", "3.4 km", "7 दिन", "5 लोग"),
    Job("पेंटर", "न्यू कॉलोनी साइट", "₹650 / दिन", "4.0 km", "10 दिन", "2 लोग"),
    Job("इलेक्ट्रिशियन", "सिटी प्रोजेक्ट", "₹800 / दिन", "5.2 km", "20 दिन", "1 व्यक्ति")
)

@Composable
private fun JobCard(job: Job, hindi: Boolean) {
    Card(colors = CardDefaults.cardColors(containerColor = Color.White), shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxWidth()) {
        Column(Modifier.padding(14.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Surface(color = LightGreen, shape = RoundedCornerShape(10.dp), modifier = Modifier.size(44.dp)) {
                    Box(contentAlignment = Alignment.Center) { Icon(Icons.Default.Handyman, contentDescription = null, tint = Green) }
                }
                Spacer(Modifier.width(10.dp))
                Column(Modifier.weight(1f)) {
                    Text(job.title, fontWeight = FontWeight.Bold, fontSize = 15.sp)
                    Text(job.company, color = Muted, fontSize = 12.sp)
                }
                Text(job.wage, color = Green, fontWeight = FontWeight.Bold, fontSize = 14.sp)
            }
            Spacer(Modifier.height(12.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(14.dp)) {
                SmallMeta(Icons.Default.LocationOn, job.distance)
                SmallMeta(Icons.Default.CalendarMonth, job.duration)
                SmallMeta(Icons.Default.Groups, job.people)
            }
            Spacer(Modifier.height(12.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(tr("आज उपलब्ध", "Available today", hindi), color = Green, fontSize = 11.sp, fontWeight = FontWeight.SemiBold, modifier = Modifier.weight(1f))
                Button(onClick = {}, contentPadding = PaddingValues(horizontal = 18.dp, vertical = 6.dp), colors = ButtonDefaults.buttonColors(containerColor = Green)) {
                    Text(tr("आवेदन करें", "Apply", hindi), fontSize = 12.sp)
                }
            }
        }
    }
}

@Composable
private fun SmallMeta(icon: androidx.compose.ui.graphics.vector.ImageVector, text: String) {
    Row(verticalAlignment = Alignment.CenterVertically) {
        Icon(icon, contentDescription = null, tint = Muted, modifier = Modifier.size(13.dp))
        Spacer(Modifier.width(3.dp))
        Text(text, fontSize = 10.sp, color = Muted)
    }
}

@Composable
private fun JobsScreen(hindi: Boolean, search: String, onSearch: (String) -> Unit) {
    Column(Modifier.fillMaxSize().padding(16.dp)) {
        OutlinedTextField(
            value = search, onValueChange = onSearch, modifier = Modifier.fillMaxWidth(),
            placeholder = { Text(tr("काम या हुनर खोजें", "Search work or skill", hindi)) },
            leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) },
            trailingIcon = { Icon(Icons.Default.Tune, contentDescription = null) },
            shape = RoundedCornerShape(14.dp), singleLine = true
        )
        Spacer(Modifier.height(12.dp))
        Text(tr("आपके आसपास उपलब्ध काम", "Available work near you", hindi), fontWeight = FontWeight.Bold, fontSize = 16.sp)
        Spacer(Modifier.height(10.dp))
        LazyColumn(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            items(sampleJobs.filter { it.title.contains(search, true) || it.company.contains(search, true) }) { JobCard(it, hindi) }
        }
    }
}

@Composable
private fun PostScreen(role: UserRole, hindi: Boolean) {
    var work by remember { mutableStateOf("") }
    var wage by remember { mutableStateOf("") }
    var count by remember { mutableStateOf("1") }
    var location by remember { mutableStateOf("Meerut") }
    var duration by remember { mutableStateOf("") }
    Column(Modifier.fillMaxSize().padding(16.dp)) {
        Text(
            if (role == UserRole.WORKER) tr("अपनी उपलब्धता पोस्ट करें", "Post your availability", hindi) else tr("कामगारों की ज़रूरत पोस्ट करें", "Post worker requirement", hindi),
            fontSize = 20.sp, fontWeight = FontWeight.Bold
        )
        Text(tr("कुछ जानकारी भरें ताकि सही लोग आपसे जुड़ सकें।", "Share a few details to connect with the right people.", hindi), color = Muted, fontSize = 12.sp)
        Spacer(Modifier.height(16.dp))
        OutlinedTextField(work, { work = it }, label = { Text(tr("काम / हुनर", "Work / Skill", hindi)) }, modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp))
        Spacer(Modifier.height(10.dp))
        OutlinedTextField(wage, { wage = it }, label = { Text(tr("दिहाड़ी (₹)", "Daily wage (₹)", hindi)) }, modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp))
        Spacer(Modifier.height(10.dp))
        if (role == UserRole.HIRING) {
            OutlinedTextField(count, { count = it }, label = { Text(tr("कितने कामगार चाहिए?", "Number of workers", hindi)) }, modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp))
            Spacer(Modifier.height(10.dp))
        }
        OutlinedTextField(duration, { duration = it }, label = { Text(tr("काम की अवधि", "Work duration", hindi)) }, modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp))
        Spacer(Modifier.height(10.dp))
        OutlinedTextField(location, { location = it }, label = { Text(tr("काम की जगह", "Work location", hindi)) }, modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp))
        Spacer(Modifier.height(18.dp))
        Button(
            onClick = {}, modifier = Modifier.fillMaxWidth().height(50.dp),
            enabled = work.isNotBlank() && wage.isNotBlank(),
            colors = ButtonDefaults.buttonColors(containerColor = Green)
        ) { Text(tr("पोस्ट प्रकाशित करें", "Publish post", hindi), fontWeight = FontWeight.Bold) }
        Text(tr("यह अभी डेमो फॉर्म है; डेटा सर्वर पर सेव नहीं होता।", "Demo form only; data is not saved to a server yet.", hindi), color = Muted, fontSize = 11.sp, modifier = Modifier.padding(top = 10.dp))
    }
}

@Composable
private fun WorkersScreen(hindi: Boolean, search: String, onSearch: (String) -> Unit) {
    val workers = listOf(
        Triple("मोहन कुमार", "राजमिस्त्री · 6 साल अनुभव", "₹700/दिन"),
        Triple("सलीम अंसारी", "पेंटर · 4 साल अनुभव", "₹650/दिन"),
        Triple("राजेश", "इलेक्ट्रिशियन · 8 साल अनुभव", "₹850/दिन"),
        Triple("दीपक", "हेल्पर · 2 साल अनुभव", "₹450/दिन")
    )
    Column(Modifier.fillMaxSize().padding(16.dp)) {
        OutlinedTextField(search, onSearch, modifier = Modifier.fillMaxWidth(), placeholder = { Text(tr("नाम या हुनर खोजें", "Search name or skill", hindi)) }, leadingIcon = { Icon(Icons.Default.Search, null) }, shape = RoundedCornerShape(14.dp), singleLine = true)
        Spacer(Modifier.height(14.dp))
        Text(tr("आपके पास के कामगार", "Workers near you", hindi), fontWeight = FontWeight.Bold, fontSize = 16.sp)
        Spacer(Modifier.height(10.dp))
        LazyColumn(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            items(workers.filter { it.first.contains(search, true) || it.second.contains(search, true) }) { worker ->
                Card(colors = CardDefaults.cardColors(containerColor = Color.White), shape = RoundedCornerShape(14.dp)) {
                    Row(Modifier.fillMaxWidth().padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
                        Surface(color = LightGreen, shape = CircleShape, modifier = Modifier.size(46.dp)) {
                            Box(contentAlignment = Alignment.Center) { Text(worker.first.take(1), color = Green, fontWeight = FontWeight.Bold, fontSize = 20.sp) }
                        }
                        Spacer(Modifier.width(12.dp))
                        Column(Modifier.weight(1f)) {
                            Text(worker.first, fontWeight = FontWeight.Bold)
                            Text(worker.second, fontSize = 11.sp, color = Muted)
                            Text("●  " + tr("उपलब्ध · 2.5 km दूर", "Available · 2.5 km away", hindi), fontSize = 10.sp, color = Green)
                        }
                        Column(horizontalAlignment = Alignment.End) {
                            Text(worker.third, color = Green, fontWeight = FontWeight.Bold, fontSize = 12.sp)
                            TextButton(onClick = {}) { Text(tr("संपर्क करें", "Contact", hindi), fontSize = 11.sp) }
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun MessagesScreen(hindi: Boolean) {
    val chats = listOf(
        Triple("शर्मा कंस्ट्रक्शन", "कल सुबह 8 बजे साइट पर आ सकते हैं?", "10:42"),
        Triple("अग्रवाल बिल्डर्स", "आपकी ₹700 की पेशकश मिली।", "कल"),
        Triple("न्यू कॉलोनी साइट", "काम की जानकारी भेज दी है।", "सोम")
    )
    Column(Modifier.fillMaxSize().padding(16.dp)) {
        Text(tr("आपकी बातचीत", "Your conversations", hindi), fontWeight = FontWeight.Bold, fontSize = 18.sp)
        Spacer(Modifier.height(12.dp))
        chats.forEach { chat ->
            Row(Modifier.fillMaxWidth().clickable {}.padding(vertical = 12.dp), verticalAlignment = Alignment.CenterVertically) {
                Surface(color = LightGreen, shape = CircleShape, modifier = Modifier.size(48.dp)) {
                    Box(contentAlignment = Alignment.Center) { Icon(Icons.Default.Person, null, tint = Green) }
                }
                Spacer(Modifier.width(12.dp))
                Column(Modifier.weight(1f)) {
                    Text(chat.first, fontWeight = FontWeight.Bold)
                    Text(chat.second, color = Muted, fontSize = 12.sp, maxLines = 1, overflow = TextOverflow.Ellipsis)
                }
                Text(chat.third, color = Muted, fontSize = 10.sp)
            }
            HorizontalDivider(color = Color(0xFFECEFEC))
        }
        Spacer(Modifier.height(10.dp))
        Text(tr("डेमो संदेश सूची — चैट सुविधा अगले चरण में जुड़ेगी।", "Demo inbox — live chat will be added in the next phase.", hindi), color = Muted, fontSize = 11.sp)
    }
}

@Composable
private fun ProfileScreen(role: UserRole, hindi: Boolean, available: Boolean) {
    Column(Modifier.fillMaxSize().padding(16.dp)) {
        Card(colors = CardDefaults.cardColors(containerColor = Color.White), shape = RoundedCornerShape(18.dp)) {
            Row(Modifier.fillMaxWidth().padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                Surface(color = LightGreen, shape = CircleShape, modifier = Modifier.size(62.dp)) {
                    Box(contentAlignment = Alignment.Center) { Icon(Icons.Default.Person, null, tint = Green, modifier = Modifier.size(34.dp)) }
                }
                Spacer(Modifier.width(14.dp))
                Column(Modifier.weight(1f)) {
                    Text("रामू कुमार", fontWeight = FontWeight.Bold, fontSize = 18.sp)
                    Text("Meerut, Uttar Pradesh", color = Muted, fontSize = 12.sp)
                    Text(tr("मोबाइल सत्यापित", "Phone verified", hindi), color = Green, fontSize = 11.sp)
                }
                Icon(Icons.Default.Verified, contentDescription = null, tint = Green)
            }
        }
        Spacer(Modifier.height(14.dp))
        val rows = listOf(
            Icons.Default.Badge to tr("मेरी जानकारी", "Personal details", hindi),
            Icons.Default.Handyman to tr("हुनर और अनुभव", "Skills & experience", hindi),
            Icons.Default.CurrencyRupee to tr("मेरी दिहाड़ी", "My daily wage", hindi),
            Icons.Default.History to tr("काम का इतिहास", "Work history", hindi),
            Icons.Default.Star to tr("रेटिंग और समीक्षा", "Ratings & reviews", hindi),
            Icons.Default.Settings to tr("सेटिंग और भाषा", "Settings & language", hindi),
            Icons.Default.HelpOutline to tr("मदद और शिकायत", "Help & report", hindi)
        )
        rows.forEach { (icon, label) ->
            Row(Modifier.fillMaxWidth().clickable {}.padding(vertical = 13.dp), verticalAlignment = Alignment.CenterVertically) {
                Icon(icon, null, tint = Green)
                Spacer(Modifier.width(14.dp))
                Text(label, modifier = Modifier.weight(1f), fontWeight = FontWeight.Medium)
                Icon(Icons.Default.ChevronRight, null, tint = Muted)
            }
            HorizontalDivider(color = Color(0xFFECEFEC))
        }
        Spacer(Modifier.height(12.dp))
        Text(tr("भूमिका", "Active role", hindi), color = Muted, fontSize = 12.sp)
        Text(if (role == UserRole.WORKER) tr("कामगार", "Worker", hindi) else tr("काम देने वाले", "Hiring", hindi), fontWeight = FontWeight.Bold)
        Text(tr("उपलब्धता: ", "Availability: ", hindi) + if (available) tr("चालू", "On", hindi) else tr("बंद", "Off", hindi), color = Green, fontSize = 12.sp)
    }
}

private fun tr(hi: String, en: String, hindi: Boolean): String = if (hindi) hi else en
