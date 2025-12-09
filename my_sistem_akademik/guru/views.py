from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q, Count, Case, When, Value, IntegerField
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, date
from django.contrib import messages
import json

# Import models
from admin_app.models import Pegawai, Jadwal, Kelas 
from siswa.models import Siswa
from .models import Absen, Nilai

def get_guru_from_user(user):
    """Helper: Ambil data Pegawai dari User yang login"""
    try:
        return user.pegawai
    except Pegawai.DoesNotExist:
        return None

# =========================================
# DASHBOARD & JADWAL
# =========================================

@login_required
def dashboard_guru(request):
    """Dashboard utama guru"""
    pegawai = get_guru_from_user(request.user)
    context = {
        'pegawai': pegawai,
        'nama_guru': request.user.first_name or request.user.username,
    }
    return render(request, 'guru/dashboard.html', context)

@login_required
def jadwal_guru(request):
    """Tampilkan jadwal guru dari database"""
    pegawai = get_guru_from_user(request.user)
    
    if not pegawai:
        jadwal_list = []
    else:
        jadwal_list = Jadwal.objects.filter(pegawai=pegawai).order_by('hari', 'jam_mulai')
    
    context = {
        'jadwal_list': jadwal_list,
        'pegawai': pegawai,
    }
    return render(request, 'guru/jadwal_guru.html', context)

# =========================================
# ABSENSI SISWA (FLOW LAMA / UTAMA)
# =========================================

@login_required
def absen_siswa(request):
    pegawai = get_guru_from_user(request.user)

    # Filter data untuk dropdown/tampilan
    jadwal_list = Jadwal.objects.filter(pegawai=pegawai) if pegawai else []

    # Ambil parameter GET
    selected_jadwal = request.GET.get('jadwal')
    selected_kelas = request.GET.get('kelas', '').strip()
    search_siswa = request.GET.get('search', '').strip()

    siswa_list = Siswa.objects.all().order_by('nama')

    # Logic Filter
    if selected_kelas:
        # FIX: Gunakan double underscore (__)
        siswa_list = siswa_list.filter(kelas__icontains=selected_kelas)

    if search_siswa:
        # FIX: Gunakan double underscore (__)
        siswa_list = siswa_list.filter(
            Q(nama__icontains=search_siswa) |
            Q(nis__icontains=search_siswa)
        )

    # Batasi tampilan jika belum ada filter
    if not search_siswa and not selected_kelas:
        siswa_list = siswa_list[:50]

    # Logic POST (Simpan Absen via AJAX/Form)
    if request.method == 'POST':
        # Bulk save via JSON payload
        if request.content_type and 'application/json' in request.content_type:
            try:
                payload = json.loads(request.body.decode('utf-8'))
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'message': 'Payload tidak valid'}, status=400)

            records = payload.get('records', [])
            jadwal_id = payload.get('jadwal_id')
            tanggal_raw = payload.get('tanggal')

            if not jadwal_id:
                return JsonResponse({'success': False, 'message': 'Jadwal wajib diisi'}, status=400)

            if isinstance(tanggal_raw, str):
                try:
                    tanggal = datetime.strptime(tanggal_raw, '%Y-%m-%d').date()
                except Exception:
                    tanggal = timezone.localdate()
            elif isinstance(tanggal_raw, (datetime, date)):
                tanggal = tanggal_raw
            else:
                tanggal = timezone.localdate()

            try:
                jadwal = Jadwal.objects.get(id=jadwal_id, pegawai=pegawai)
            except Jadwal.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Jadwal tidak ditemukan'}, status=404)

            nis_list = [r.get('siswa_id') for r in records if r.get('siswa_id')]
            siswa_map = {s.nis: s for s in Siswa.objects.filter(nis__in=nis_list)}

            # FIX: Gunakan double underscore (__) untuk lookup relasi
            existing_absen = Absen.objects.filter(
                jadwal=jadwal,
                tanggal=tanggal,
                siswa__nis__in=nis_list
            ).select_related('siswa')
            existing_map = {a.siswa.nis: a for a in existing_absen}

            to_update = []
            to_create = []
            now_ts = timezone.now()

            for rec in records:
                nis = rec.get('siswa_id')
                status = rec.get('status')
                keterangan = rec.get('keterangan', '')

                if not nis or not status:
                    continue
                siswa_obj = siswa_map.get(nis)
                if not siswa_obj:
                    continue

                existing = existing_map.get(nis)
                if existing:
                    existing.status = status
                    existing.keterangan = keterangan
                    existing.pegawai = pegawai
                    existing.updated_at = now_ts
                    to_update.append(existing)
                else:
                    to_create.append(Absen(
                        siswa=siswa_obj,
                        pegawai=pegawai,
                        jadwal=jadwal,
                        tanggal=tanggal,
                        status=status,
                        keterangan=keterangan
                    ))

            with transaction.atomic():
                if to_update:
                    Absen.objects.bulk_update(to_update, ['status', 'keterangan', 'pegawai', 'updated_at'])
                if to_create:
                    Absen.objects.bulk_create(to_create)

            return JsonResponse({
                'success': True,
                'updated': len(to_update),
                'created': len(to_create),
                'message': 'Absen berhasil diproses'
            })

        # Fallback single record (kompatibilitas lama)
        siswa_id = request.POST.get('siswa_id')
        jadwal_id = request.POST.get('jadwal_id')
        status = request.POST.get('status')
        tanggal = request.POST.get('tanggal', timezone.localdate())
        keterangan = request.POST.get('keterangan', '')

        try:
            siswa = Siswa.objects.get(nis=siswa_id)
            jadwal = Jadwal.objects.get(id=jadwal_id, pegawai=pegawai)

            Absen.objects.update_or_create(
                siswa=siswa,
                jadwal=jadwal,
                tanggal=tanggal,
                defaults={
                    'pegawai': pegawai,
                    'status': status,
                    'keterangan': keterangan,
                }
            )
            return JsonResponse({'success': True, 'message': 'Absen berhasil disimpan'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    context = {
        'jadwal_list': jadwal_list,
        'siswa_list': siswa_list,
        'pegawai': pegawai,
        'selected_kelas': selected_kelas,
        'selected_jadwal': selected_jadwal,
        'search_siswa': search_siswa,
    }

    return render(request, 'guru/absen.html', context)


# =========================================
# ABSENSI (FLOW BARU - MIRIP INPUT NILAI)
# =========================================

def _hari_case_expression():
    hari_urut = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    return Case(
        *[When(hari=h, then=Value(idx)) for idx, h in enumerate(hari_urut)],
        default=Value(99),
        output_field=IntegerField()
    )


@login_required
def absen_index(request):
    """Daftar jadwal khusus absensi, tampilan mirip index Input Nilai."""
    pegawai = get_guru_from_user(request.user)
    if not pegawai:
        jadwal_list = []
    else:
        jadwal_list = (
            Jadwal.objects.filter(pegawai=pegawai)
            .annotate(hari_order=_hari_case_expression())
            .order_by('hari_order', 'jam_mulai')
        )

    context = {
        'pegawai': pegawai,
        'jadwal_list': jadwal_list,
    }
    return render(request, 'guru/absen_index.html', context)


@login_required
def absen_detail(request, jadwal_id):
    jadwal = get_object_or_404(Jadwal, id=jadwal_id)

    # ======================================================
    # FIX: Penanganan tipe data Kelas (Object vs String)
    # ======================================================
    kelas_obj = jadwal.kelas
    
    if hasattr(kelas_obj, 'nama'):
        # Jika Object (Model Kelas)
        kelas_str = f"{kelas_obj.nama} {kelas_obj.jurusan} {kelas_obj.sub_kelas}"
        siswa_list = Siswa.objects.filter(kelas=kelas_obj).order_by('nama')
    else:
        # Jika String (Legacy/CharField)
        kelas_str = str(kelas_obj)
        # Gunakan double underscore (__) untuk filter contains
        siswa_list = Siswa.objects.filter(kelas__icontains=kelas_str).order_by('nama')

    # Tentukan tanggal absensi
    tanggal_str = request.GET.get("tanggal") or request.POST.get("tanggal")
    if tanggal_str:
        try:
            tanggal = datetime.strptime(tanggal_str, "%Y-%m-%d").date()
        except ValueError:
            tanggal = datetime.today().date()
    else:
        tanggal = datetime.today().date()

    save_summary = None 

    # ============================
    #  POST -> SIMPAN ABSENSI
    # ============================
    if request.method == "POST":
        created = 0
        updated = 0

        # Ambil semua NIS siswa untuk query optimization
        nis_list = list(siswa_list.values_list('nis', flat=True))

        # Ambil absen yang sudah ada untuk hari itu
        # FIX: Gunakan double underscore (__)
        existing_absen = {
            a.siswa.nis: a
            for a in Absen.objects.filter(
                jadwal=jadwal,
                tanggal=tanggal,
                siswa__nis__in=nis_list
            )
        }

        for siswa in siswa_list:
            status = request.POST.get(f"status_{siswa.nis}", "").strip()
            ket = request.POST.get(f"ket_{siswa.nis}", "").strip()

            if not status:
                continue 

            if siswa.nis in existing_absen:
                # update
                ab = existing_absen[siswa.nis]
                ab.status = status
                ab.keterangan = ket
                ab.save()
                updated += 1
            else:
                # create baru
                Absen.objects.create(
                    jadwal=jadwal,
                    siswa=siswa,
                    tanggal=tanggal,
                    status=status,
                    keterangan=ket,
                    pegawai=get_guru_from_user(request.user)
                )
                created += 1

        save_summary = {"created": created, "updated": updated}
        messages.success(request, f"Absensi berhasil: {created} baru, {updated} diperbarui.")

    context = {
        "jadwal": jadwal,
        "kelas_str": kelas_str, # String aman untuk template
        "siswa_list": siswa_list,
        "tanggal": tanggal,
        "save_summary": save_summary
    }

    return render(request, "guru/absen_detail.html", context)


# =========================================
# RIWAYAT ABSENSI
# =========================================

@login_required
def riwayat_absensi(request):
    """
    Dashboard riwayat absensi dengan filter manual.
    """
    pegawai = get_guru_from_user(request.user)
    jadwal_options = Jadwal.objects.filter(pegawai=pegawai).order_by('mata_pelajaran', 'hari') if pegawai else []

    selected_kelas = (request.GET.get('kelas') or '').strip()
    selected_jadwal = (request.GET.get('jadwal') or '').strip()
    tanggal_str = (request.GET.get('tanggal') or '').strip()
    show_flag = request.GET.get('show')

    show_results = bool(show_flag or selected_kelas or selected_jadwal or tanggal_str)

    absen_list = []
    stats_map = {'hadir': 0, 'izin': 0, 'sakit': 0, 'alpa': 0}
    tanggal = None

    if show_results and tanggal_str:
        try:
            tanggal = datetime.strptime(tanggal_str, '%Y-%m-%d').date()
        except Exception:
            tanggal = timezone.localdate()

    if show_results and tanggal:
        # FIX: Gunakan double underscore (__) untuk relasi
        absen_qs = Absen.objects.select_related('siswa', 'jadwal').filter(
            jadwal__pegawai=pegawai,
            tanggal=tanggal
        )

        if selected_kelas:
            # FIX: Gunakan double underscore (__)
            absen_qs = absen_qs.filter(siswa__kelas__icontains=selected_kelas)

        if selected_jadwal:
            absen_qs = absen_qs.filter(jadwal_id=selected_jadwal)

        absen_qs = absen_qs.order_by('siswa__nama')
        absen_list = list(absen_qs)

        stats_raw = absen_qs.values('status').annotate(total=Count('status'))
        stats_map = {item['status']: item['total'] for item in stats_raw}

    context = {
        'pegawai': pegawai,
        'jadwal_options': jadwal_options,
        'selected_kelas': selected_kelas,
        'selected_jadwal': selected_jadwal,
        'tanggal': tanggal_str,
        'show_results': show_results and tanggal,
        'absen_list': absen_list,
        'stat_hadir': stats_map.get('hadir', 0),
        'stat_izin': stats_map.get('izin', 0),
        'stat_sakit': stats_map.get('sakit', 0),
        'stat_alpa': stats_map.get('alpa', 0),
    }

    return render(request, 'guru/riwayat_absensi.html', context)

# =========================================
# INPUT NILAI (Updated)
# =========================================

@login_required
def input_nilai(request):
    """
    Halaman Utama Input Nilai.
    """
    pegawai = get_guru_from_user(request.user)
    
    if not pegawai:
        jadwal_list = []
    else:
        jadwal_list = Jadwal.objects.filter(pegawai=pegawai).order_by('hari', 'jam_mulai')
    
    context = {
        'jadwal_list': jadwal_list,
        'pegawai': pegawai,
    }
    return render(request, 'guru/input_nilai.html', context)


@login_required
def input_nilai_detail(request, jadwal_id):
    """
    Halaman Detail: Menampilkan daftar siswa berdasarkan Jadwal yang dipilih
    dan form input nilai.
    """
    pegawai = get_guru_from_user(request.user)
    jadwal = get_object_or_404(Jadwal, id=jadwal_id, pegawai=pegawai)
    
    # ======================================================
    # FIX: Penanganan tipe data Kelas (Defensif)
    # ======================================================
    kelas_obj = jadwal.kelas
    
    # Default strategy: try object attributes first
    if hasattr(kelas_obj, 'nama'):
        # Jika Object standard
        kelas_str = f"{kelas_obj.nama}"
        # Jika perlu filter spesifik object:
        siswa_list = Siswa.objects.filter(kelas=kelas_obj).order_by('nama')
    elif hasattr(kelas_obj, 'nama_kelas'):
        # Jika Object tapi nama fieldnya 'nama_kelas'
        kelas_str = kelas_obj.nama_kelas
        # Asumsi filter tetap jalan via object
        siswa_list = Siswa.objects.filter(kelas=kelas_obj).order_by('nama')
    else:
        # Fallback String
        kelas_str = str(kelas_obj)
        # Gunakan filter string __icontains
        siswa_list = Siswa.objects.filter(kelas__icontains=kelas_str).order_by('nama')

    # prepare container for existing_nilai
    existing_nilai = {}

    # Fitur Search
    search_siswa = request.GET.get('search', '').strip()
    if search_siswa:
        # FIX: Gunakan double underscore (__)
        siswa_list = siswa_list.filter(
            Q(nama__icontains=search_siswa) | Q(nis__icontains=search_siswa)
        )

    # Ambil nilai terakhir per siswa untuk jadwal ini
    # FIX: Gunakan double underscore (__) untuk lookup siswa__in
    existing_nilai_qs = Nilai.objects.filter(jadwal=jadwal, siswa__in=siswa_list).select_related('siswa').order_by('siswa__nis', '-tanggal')
    for n in existing_nilai_qs:
        nis = n.siswa.nis
        if nis not in existing_nilai:
            existing_nilai[nis] = {
                'nilai': n.nilai,
                'tanggal': n.tanggal,
                'keterangan': n.keterangan,
                'id': n.id,
            }

    # Variabel untuk context
    keterangan_nilai = ''
    tanggal = datetime.now().date()
    nilai_data = {} 

    # Logic Simpan Nilai (POST)
    if request.method == 'POST' and 'simpan_semua' in request.POST:
        keterangan_nilai = request.POST.get('keterangan_nilai', '')
        tanggal_input = request.POST.get('tanggal')
        
        # Validasi Tanggal
        if isinstance(tanggal_input, str) and tanggal_input:
            try:
                tanggal = datetime.strptime(tanggal_input, '%Y-%m-%d').date()
            except ValueError:
                tanggal = datetime.now().date()
        else:
            tanggal = datetime.now().date()

        # Loop melalui POST keys
        for key, value in request.POST.items():
            if not key.startswith('nilai_'):
                continue

            nis = key.split('nilai_', 1)[1]
            nilai_str = value
            if not nilai_str:
                continue

            try:
                siswa = Siswa.objects.get(nis=nis)
            except Siswa.DoesNotExist:
                nilai_data[nis] = 'no_siswa'
                continue

            try:
                nilai_float = float(nilai_str)
                if 0 <= nilai_float <= 100:
                    Nilai.objects.update_or_create(
                        siswa=siswa,
                        jadwal=jadwal,
                        tanggal=tanggal,
                        defaults={
                            'pegawai': pegawai,
                            'nilai': nilai_float,
                            'keterangan': keterangan_nilai,
                        }
                    )
                    nilai_data[nis] = 'ok'
                    existing_nilai[nis] = {
                        'nilai': nilai_float,
                        'tanggal': tanggal,
                        'keterangan': keterangan_nilai,
                    }
                else:
                    nilai_data[nis] = 'invalid'
            except ValueError:
                nilai_data[nis] = 'error'
        
        messages.success(request, "Input nilai berhasil diproses.")

    # Pasang atribut helper pada objek siswa untuk akses di template
    for s in siswa_list:
        s.existing_nilai = existing_nilai.get(s.nis)
        s.save_status = nilai_data.get(s.nis)

    context = {
        'jadwal': jadwal,
        'siswa_list': siswa_list,
        'keterangan_nilai': keterangan_nilai,
        'tanggal': tanggal,
        'nilai_data': nilai_data,
        'search_siswa': search_siswa,
        'kelas_str': kelas_str # Kirim nama kelas string ke template
    }
    
    return render(request, 'guru/input_nilai_detail.html', context)


# =========================================
# REKAP NILAI (Gudang Data & Manajemen)
# =========================================

@login_required
def rekap_nilai(request):
    """
    Halaman Rekap Nilai: Filter by Kelas & Mata Pelajaran/Jadwal.
    """
    pegawai = get_guru_from_user(request.user)
    
    selected_kelas = request.GET.get('kelas', '')
    selected_jadwal = request.GET.get('jadwal', '')
    search_siswa = request.GET.get('search', '').strip()
    
    jadwal_list = Jadwal.objects.filter(pegawai=pegawai).order_by('hari', 'jam_mulai')
    kelas_list = Kelas.objects.all().order_by('nama_kelas')
    
    statistik = None
    nilai_siswa_list = []
    
    if selected_kelas and selected_jadwal:
        try:
            jadwal = Jadwal.objects.get(id=selected_jadwal, pegawai=pegawai)
        except Jadwal.DoesNotExist:
            jadwal = None

        if jadwal:
            # FIX: Gunakan double underscore (__)
            nilai_query = Nilai.objects.filter(
                jadwal=jadwal,
                siswa__kelas__icontains=selected_kelas
            ).select_related('siswa').order_by('-tanggal', 'siswa__nama')
            
            if search_siswa:
                # FIX: Gunakan double underscore (__)
                nilai_query = nilai_query.filter(
                    Q(siswa__nama__icontains=search_siswa) |
                    Q(siswa__nis__icontains=search_siswa)
                )
            
            nilai_siswa_list = list(nilai_query)
            
            if nilai_siswa_list:
                nilai_list = [n.nilai for n in nilai_siswa_list]
                rata_rata = sum(nilai_list) / len(nilai_list)
                nilai_tertinggi = max(nilai_list)
                nilai_terendah = min(nilai_list)
                
                statistik = {
                    'rata_rata': round(rata_rata, 2),
                    'tertinggi': nilai_tertinggi,
                    'terendah': nilai_terendah,
                    'total_siswa': len(nilai_siswa_list)
                }
    
    context = {
        'jadwal_list': jadwal_list,
        'kelas_list': kelas_list,
        'nilai_siswa_list': nilai_siswa_list,
        'statistik': statistik,
        'selected_kelas': selected_kelas,
        'selected_jadwal': selected_jadwal,
        'search_siswa': search_siswa,
        'pegawai': pegawai,
    }
    
    return render(request, 'guru/rekap_nilai.html', context)


@login_required
def update_nilai_ajax(request):
    """
    Handle update nilai via AJAX POST request.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method tidak diizinkan'}, status=405)
    
    pegawai = get_guru_from_user(request.user)
    nilai_id = request.POST.get('nilai_id')
    nilai_baru = request.POST.get('nilai')
    keterangan_baru = request.POST.get('keterangan', '')
    
    try:
        nilai_obj = Nilai.objects.get(id=nilai_id, pegawai=pegawai)
        
        nilai_float = float(nilai_baru)
        if not (0 <= nilai_float <= 100):
            return JsonResponse({'success': False, 'message': 'Nilai harus antara 0-100'})
        
        nilai_obj.nilai = nilai_float
        nilai_obj.keterangan = keterangan_baru
        nilai_obj.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Nilai berhasil diperbarui',
            'nilai': nilai_float,
            'keterangan': keterangan_baru
        })
    
    except Nilai.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Data nilai tidak ditemukan'}, status=404)
    except ValueError:
        return JsonResponse({'success': False, 'message': 'Format nilai tidak valid'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})