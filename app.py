# app.py (VERSI LENGKAP TANPA DATABASE SQL PERSISTEN)

from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta
from functools import wraps # Import wraps untuk decorator

app = Flask(__name__)
# PENTING: GANTI DENGAN KUNCI RAHASIA YANG LEBIH KUAT DAN ACAK DI LINGKUNGAN PRODUKSI!
# Ini digunakan untuk mengamankan sesi (session) dan pesan flash.
# Untuk menghasilkan kunci yang kuat, Anda bisa menggunakan Python console:
# import os
# os.urandom(24)
# Contoh: app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.secret_key = 'super_secret_key_unibba_event_app_12345_ganti_ini_dengan_yang_kuat'

# --- DATA EVENT HARCODED (PENGGANTI DATABASE) ---
# Data ini akan hilang setiap kali server di-restart
events_data = [
    {
        'id': 1,
        'nama': 'Webinar Inovasi Teknologi 2025',
        'deskripsi': 'Bergabunglah dengan para ahli industri untuk membahas tren teknologi terbaru dan inovasi yang akan mengubah masa depan digital.',
        'tanggal': '2025-07-20', # Hari Ini, sesuai tanggal sistem
        'waktu': '10:00',
        'lokasi': 'Online via Zoom',
        'biaya_pendaftaran': 'Gratis',
        'kuota': 200,
        'kontak_person': 'webinar@unibba.ac.id',
        'image_url': 'images/event_webinar.jpg'
    },
    {
        'id': 2,
        'nama': 'Workshop Fotografi Dasar',
        'deskripsi': 'Pelajari teknik dasar fotografi, komposisi, dan editing untuk menghasilkan foto yang menakjubkan dengan kamera atau smartphone Anda.',
        'tanggal': '2025-07-15', # Mendatang
        'waktu': '14:00',
        'lokasi': 'Aula Gedung B UNIBBA',
        'biaya_pendaftaran': 'Rp 50.000',
        'kuota': 30,
        'kontak_person': 'fotografi.club@unibba.ac.id',
        'image_url': 'images/event_workshop.jpg'
    },
    {
        'id': 3,
        'nama': 'Lomba Desain Grafis Kampus',
        'deskripsi': 'Tunjukkan kreativitas Anda dalam lomba desain grafis tahunan. Menangkan hadiah menarik dan pamerkan karya Anda!',
        'tanggal': '2025-08-01', # Mendatang
        'waktu': '09:00',
        'lokasi': 'Lab Komputer UNIBBA',
        'biaya_pendaftaran': 'Gratis',
        'kuota': 50,
        'kontak_person': 'desain_lomba@unibba.ac.id',
        'image_url': 'images/event_design.jpg'
    },
    {
        'id': 4,
        'nama': 'Seminar Karir & Job Fair',
        'deskripsi': 'Dapatkan wawasan dari profesional dan temukan peluang karir dari perusahaan terkemuka di job fair kampus.',
        'tanggal': '2025-06-20', # Sebelumnya
        'waktu': '09:00',
        'lokasi': 'Gedung Serbaguna UNIBBA',
        'biaya_pendaftaran': 'Gratis',
        'kuota': 500,
        'kontak_person': 'pusat_karir@unibba.ac.id',
        'image_url': 'images/event_career.jpg'
    },
    {
        'id': 5,
        'nama': 'Lomba Futsal Antar Fakultas ',
        'deskripsi': 'Tunjukkan sportifitas anda dalam lomba futsal. Menangkan hadiah menarik untuk juara satu!.',
        'tanggal': '2025-06-21', # Sebelumnya
        'waktu': '09:00',
        'lokasi': 'Gedung Serbaguna UNIBBA',
        'biaya_pendaftaran': 'Gratis',
        'kuota': 500,
        'kontak_person': 'sport@unibba.ac.id',
        'image_url': 'images/event_futsal.jpg'
    },
    {
        'id': 6,
        'nama': 'Open House Program Studi / Expo Kampus ',
        'deskripsi': 'Dapatkan wawasan dari profesional dan temukan peluang karir dari perusahaan terkemuka di job fair kampus.',
        'tanggal': '2025-08-20',
        'waktu': '08:00',
        'lokasi': 'Lapangan Depan UNIBBA',
        'biaya_pendaftaran': 'Gratis',
        'kuota': 1000,
        'kontak_person': 'expo@unibba.ac.id',
        'image_url': 'images/expo.jpg'
    },
    {
        'id': 7,
        'nama': 'Bakti Sosial Pada Masyarakat',
        'deskripsi': 'Kegiatan pengabdian yang dilakukan di luar kampus, yaitu mengajar anak-anak desa kertasari terutama bagi yang kurang mampu.',
        'tanggal': '2025-07-30', # Sebelumnya
        'waktu': '09:00',
        'lokasi': 'Lapangan Kertasari',
        'biaya_pendaftaran': 'Gratis',
        'kuota': 100,
        'kontak_person': 'bakti@unibba.ac.id',
        'image_url': 'images/bakti.jpg'
    },
    {
        'id': 8,
        'nama': 'Kampus Hijau / Gerakan Eco-Green',
        'deskripsi': 'Kegiatan menanam pohon di belakang kampus UNIBBA, menciptakan lingkungan hidup yang lebih ramah dan berkelanjutan.',
        'tanggal': '2025-10-30', # Sebelumnya
        'waktu': '08:00',
        'lokasi': 'Belakang kampus UNIBBA',
        'biaya_pendaftaran': 'Gratis',
        'kuota': 300,
        'kontak_person': 'eco_green@unibba.ac.id',
        'image_url': 'images/Eco_Green.jpg'
    },
    {
        'id': 9,
        'nama': 'Campus Music Night UNIBBA',
        'deskripsi': 'Panggung hiburan malam hari menampilkan band kampus, solois, atau cover music dari mahasiswa..',
        'tanggal': '2025-08-10', # Sebelumnya
        'waktu': '19:00',
        'lokasi': 'Lapangan UNIBBA',
        'biaya_pendaftaran': 'Rp 50.000',
        'kuota': 20,
        'kontak_person': 'music@unibba.ac.id',
        'image_url': 'images/music.jpg'
    },
    {
        'id': 10,
        'nama': 'Lomba Film Pendek Mahasiswa',
        'deskripsi': 'Lomba pembuatan film pendek oleh mahasiswa antar kelas dengan tema-tema tertentu.',
        'tanggal': '2025-08-07',
        'waktu': '07:30',
        'lokasi': 'Lapangan UNIBBA',
        'biaya_pendaftaran': 'Rp 50.000',
        'kuota': 25,
        'kontak_person': 'mercu@unibba.ac.id',
        'image_url': 'images/film.jpg'
    },
    {
        'id': 11,
        'nama': 'Festival Cosplay dan Game',
        'deskripsi': 'Event bertema budaya pop Jepang/Korea yang menampilkan cosplay, lomba game, dan bazar merchandise.',
        'tanggal': '2025-02-10',
        'waktu': '07:30',
        'lokasi': 'Lapangan Belakang UNIBBA',
        'biaya_pendaftaran': 'Rp 50.000',
        'kuota': 100,
        'kontak_person': 'cos@unibba.ac.id',
        'image_url': 'images/cosplay.jpg'
    },
    {
        'id': 12,
        'nama': 'Festival Budaya Nusantara',
        'deskripsi': 'Event ini menampilkan keberagaman budaya dari berbagai daerah di Indonesia. Mahasiswa dari berbagai suku menampilkan budaya daerah masing-masing, seperti pakaian adat, makanan khas, dan pertunjukan seni.',
        'tanggal': '2025-10-10',
        'waktu': '07:30',
        'lokasi': 'Lapangan Belakang UNIBBA',
        'biaya_pendaftaran': 'Rp 25.000',
        'kuota': 100,
        'kontak_person': 'bud@unibba.ac.id',
        'image_url': 'images/budaya.jpg'
    }

]

# --- Simulasi Data Pengguna (Tidak Persisten) ---
users_data = {
    'admin': {'password': 'admin123', 'email': 'admin@unibba.ac.id'},
    'user1': {'password': 'password123', 'email': 'user1@example.com'}
}

# --- Simulasi Data Registrasi (Tidak Persisten) ---
# Format: {event_id: [{'nama': '...', 'email': '...', 'nim': '...', 'username': '...'}]}
# Menambahkan 'username' ke setiap pendaftaran untuk melacak siapa yang mendaftar
registrations_data = {}

# --- DECORATOR UNTUK MEMERLUKAN LOGIN ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Anda harus login untuk mengakses halaman ini.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- FUNGSI AUTENTIKASI ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        flash('Anda sudah login.', 'info')
        return redirect(url_for('beranda'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if username in users_data:
            flash('Username sudah ada. Silakan pilih username lain.', 'error')
        elif any(user_info['email'] == email for user_info in users_data.values()):
            flash('Email ini sudah terdaftar. Silakan gunakan email lain atau login.', 'error')
        else:
            users_data[username] = {'password': password, 'email': email}
            flash('Registrasi berhasil! Silakan login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        flash('Anda sudah login.', 'info')
        return redirect(url_for('beranda'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users_data and users_data[username]['password'] == password:
            session['username'] = username
            flash('Login berhasil!', 'success')
            return redirect(url_for('beranda'))
        else:
            flash('Username atau password salah.', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    flash('Anda telah logout.', 'info')
    return redirect(url_for('login'))


# --- FUNGSI ADMIN/MANAJEMEN EVENT ---
@app.route('/tambah_event', methods=['GET', 'POST'])
@login_required
def tambah_event():
    if session['username'] != 'admin':
        flash('Akses ditolak. Hanya admin yang bisa menambah event.', 'error')
        return redirect(url_for('beranda'))

    if request.method == 'POST':
        nama = request.form['nama']
        deskripsi = request.form['deskripsi']
        tanggal = request.form['tanggal']
        waktu = request.form['waktu']
        lokasi = request.form['lokasi']
        biaya_pendaftaran = request.form['biaya_pendaftaran']
        kuota = int(request.form['kuota'])
        kontak_person = request.form['kontak_person']
        image_url = request.form['image_url']

        new_id = max([e['id'] for e in events_data]) + 1 if events_data else 1
        new_event = {
            'id': new_id,
            'nama': nama,
            'deskripsi': deskripsi,
            'tanggal': tanggal,
            'waktu': waktu,
            'lokasi': lokasi,
            'biaya_pendaftaran': biaya_pendaftaran,
            'kuota': kuota,
            'kontak_person': kontak_person,
            'image_url': image_url
        }
        events_data.append(new_event)
        flash('Event berhasil ditambahkan (sementara)! Akan hilang saat server restart.', 'success')
        return redirect(url_for('beranda'))
    return render_template('tambah_event.html')

# --- FUNGSI PENDAFTARAN PESERTA ---
@app.route('/event/<int:id>/daftar', methods=['GET', 'POST'])
@login_required
def form_pendaftaran(id):
    event = next((e for e in events_data if e['id'] == id), None)

    if event is None:
        flash('Event tidak ditemukan.', 'error')
        return redirect(url_for('beranda'))

    if session['username'] == 'admin':
        flash('Admin tidak dapat mendaftar event.', 'error')
        return redirect(url_for('detail_event', id=id))

    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        nim = request.form['nim']
        current_username = session['username'] # Dapatkan username yang sedang login

        if id not in registrations_data:
            registrations_data[id] = []

        # Periksa duplikasi pendaftaran berdasarkan NIM atau Email
        existing_registration = next((r for r in registrations_data[id] if r['email'] == email or r['nim'] == nim), None)
        if existing_registration:
            flash('Anda atau NIM/Email ini sudah terdaftar untuk event ini (sementara).', 'warning')
            return redirect(url_for('form_pendaftaran', id=id))

        # Periksa kuota
        current_registrations_count = len(registrations_data[id])
        if current_registrations_count >= event['kuota']:
            flash('Maaf, kuota peserta untuk event ini sudah penuh (sementara).', 'error')
            return redirect(url_for('detail_event', id=id))

        # Tambahkan registrasi ke dummy data di memori, termasuk username
        registrations_data[id].append({'nama': nama, 'email': email, 'nim': nim, 'username': current_username})
        flash(f'Pendaftaran untuk event "{event["nama"]}" berhasil (sementara)!', 'success')
        return redirect(url_for('detail_event', id=id))

    return render_template('form_pendaftaran.html', event=event)

@app.route('/event/<int:id>/peserta')
@login_required
def daftar_peserta(id):
    if session['username'] != 'admin':
        flash('Akses ditolak. Hanya admin yang bisa melihat daftar peserta.', 'error')
        return redirect(url_for('beranda'))

    event = next((e for e in events_data if e['id'] == id), None)
    peserta = registrations_data.get(id, [])

    if event is None:
        flash('Event tidak ditemukan.', 'error')
        return redirect(url_for('beranda'))

    return render_template('daftar_peserta.html', event=event, peserta=peserta)


# --- ROUTE UNTUK PROFIL DAN EVENT SAYA ---
@app.route('/profil_saya')
@login_required
def profil_saya():
    current_username = session['username']
    user_info = users_data.get(current_username) # Ambil info pengguna dari data dummy

    if not user_info:
        flash('Informasi profil tidak ditemukan.', 'error')
        return redirect(url_for('dashboard'))

    # Buat objek user agar bisa diakses di template seperti user.username, user.email
    class User:
        def __init__(self, username, email):
            self.username = username
            self.email = email

    user = User(current_username, user_info['email'])
    return render_template('profil_saya.html', user=user)

@app.route('/event_saya')
@login_required
def event_saya():
    current_username = session['username']
    user_registered_event_ids = set() # Menggunakan set untuk menghindari duplikasi ID event

    # Iterasi melalui semua pendaftaran untuk menemukan event yang didaftarkan oleh pengguna ini
    for event_id, registrations in registrations_data.items():
        for reg in registrations:
            if reg.get('username') == current_username:
                user_registered_event_ids.add(event_id)

    # Ambil detail event dari events_data berdasarkan ID yang ditemukan
    registered_events = []
    for event_id in user_registered_event_ids:
        event = next((e for e in events_data if e['id'] == event_id), None)
        if event:
            registered_events.append(event)

    return render_template('event_saya.html', registered_events=registered_events)


# --- ROUTE UTAMA APLIKASI ---
@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('beranda'))

@app.route('/beranda')
@login_required
def beranda():
    all_events = sorted(events_data, key=lambda x: x['tanggal'])

    upcoming_events = []
    ongoing_events = []
    past_events = []
    today = datetime.now().date()

    for event in all_events:
        event_date = datetime.strptime(event['tanggal'], '%Y-%m-%d').date()
        if event_date > today:
            upcoming_events.append(event)
        elif event_date == today:
            ongoing_events.append(event)
        else:
            past_events.append(event)

    return render_template('beranda.html',
                           username=session.get('username'),
                           upcoming_events=upcoming_events,
                           ongoing_events=ongoing_events,
                           past_events=past_events)

@app.route('/tentang')
def tentang():
    return render_template('tentang.html', username=session.get('username'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=session['username'])

@app.route('/event/<int:id>')
@login_required
def detail_event(id):
    event = next((e for e in events_data if e['id'] == id), None)

    if event is None:
        flash('Event tidak ditemukan.', 'error')
        return redirect(url_for('beranda'))
    return render_template('detail_event.html', event=event, username=session.get('username'))

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial_login.html')


if __name__ == '__main__':
    app.run(debug=True)
